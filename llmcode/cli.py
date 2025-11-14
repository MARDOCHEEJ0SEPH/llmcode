"""CLI interface for LLMCode"""

import sys
import os
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.live import Live
from rich.spinner import Spinner

from .config import load_config, Config
from .llm_client import LLMClient
from .session import Session
from .git_utils import GitRepo
from .tools.base import ToolRegistry
from .tools.file_tools import ReadTool, WriteTool, EditTool
from .tools.bash_tool import BashTool
from .tools.search_tools import GlobTool, GrepTool
from .tools.web_tools import WebSearchTool, WebFetchTool


console = Console()


class LLMCodeCLI:
    """Main CLI application"""

    def __init__(self, config: Config, working_directory: Optional[Path] = None):
        self.config = config
        self.working_directory = working_directory or Path.cwd()

        # Set up tool registry
        self.tool_registry = ToolRegistry()
        self._register_tools()

        # Set up LLM client
        self.llm_client = LLMClient(config, self.tool_registry)

        # Set up session
        self.session = Session(session_dir=config.session_dir)

        # Git info
        self.git_repo = GitRepo(self.working_directory)

    def _register_tools(self):
        """Register all available tools"""
        # File tools
        self.tool_registry.register(ReadTool())
        self.tool_registry.register(WriteTool())
        self.tool_registry.register(EditTool())

        # Bash tool
        self.tool_registry.register(BashTool(str(self.working_directory)))

        # Search tools
        self.tool_registry.register(GlobTool(str(self.working_directory)))
        self.tool_registry.register(GrepTool(str(self.working_directory)))

        # Web tools
        if self.config.serper_api_key:
            self.tool_registry.register(WebSearchTool(self.config.serper_api_key))
        self.tool_registry.register(WebFetchTool())

    def print_welcome(self):
        """Print welcome message"""
        console.print()
        console.print(Panel.fit(
            "[bold blue]LLMCode - AI Coding Assistant[/bold blue]\n"
            f"Working directory: {self.working_directory}\n"
            f"Model: {self.config.default_model}\n"
            "Type 'exit' or 'quit' to exit",
            border_style="blue"
        ))

        # Show git context if available
        if self.git_repo.is_repo:
            git_status = self.git_repo.get_status()
            console.print(f"\n[dim]Git: {git_status.get('branch', 'unknown')} - {git_status.get('status', 'clean')}[/dim]")

        console.print()

    def run_interactive(self):
        """Run interactive session"""
        self.print_welcome()

        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold green]You[/bold green]")

                if not user_input.strip():
                    continue

                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    if self.config.auto_save_sessions:
                        self.session.save(self.llm_client)
                        console.print("\n[dim]Session saved[/dim]")
                    console.print("\n[blue]Goodbye![/blue]\n")
                    break

                # Special commands
                if user_input.lower() == '/clear':
                    self.llm_client.clear_history()
                    console.print("\n[dim]Conversation cleared[/dim]")
                    continue

                if user_input.lower() == '/save':
                    self.session.save(self.llm_client)
                    console.print(f"\n[dim]Session saved: {self.session.session_id}[/dim]")
                    continue

                if user_input.lower() == '/sessions':
                    self._show_sessions()
                    continue

                # Process message
                console.print()
                self._process_message(user_input)

                # Auto-save
                if self.config.auto_save_sessions:
                    self.session.save(self.llm_client)

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"\n[red]Error: {str(e)}[/red]")
                if self.config.verbose:
                    console.print_exception()

    def _process_message(self, user_message: str):
        """Process a user message"""
        console.print("[bold blue]Assistant:[/bold blue]\n")

        current_text = []

        for event in self.llm_client.send_message(user_message):
            if event["type"] == "text":
                current_text.append(event["content"])
                # Print text content
                console.print(event["content"], end="")

            elif event["type"] == "tool_use":
                # Show tool use
                console.print(f"\n\n[dim]🔧 Using tool: {event['tool']}[/dim]")
                if self.config.verbose:
                    console.print(f"[dim]{event['input']}[/dim]")

            elif event["type"] == "tool_result":
                # Show tool result
                status_color = "green" if event["status"] == "success" else "yellow"
                console.print(f"[{status_color}]✓ {event['tool']} completed[/{status_color}]")

                if self.config.verbose and event.get("result"):
                    # Truncate long results
                    result = event["result"]
                    if len(result) > 500:
                        result = result[:500] + "\n... (truncated)"
                    console.print(f"[dim]{result}[/dim]")

            elif event["type"] == "error":
                console.print(f"\n[red]Error: {event['error']}[/red]")

        console.print()  # Final newline

    def _show_sessions(self):
        """Show saved sessions"""
        sessions = Session.list_sessions(self.config.session_dir)

        if not sessions:
            console.print("\n[dim]No saved sessions[/dim]")
            return

        console.print("\n[bold]Saved Sessions:[/bold]\n")
        for session in sessions[:10]:
            console.print(
                f"[blue]{session['session_id']}[/blue] - "
                f"{session.get('message_count', 0)} messages - "
                f"Updated: {session.get('last_updated', 'unknown')}"
            )

    def run_single_command(self, command: str):
        """Run a single command and exit"""
        self._process_message(command)


@click.command()
@click.argument('command', required=False)
@click.option('--directory', '-d', type=click.Path(exists=True), help='Working directory')
@click.option('--model', '-m', help='Model to use')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--session', '-s', help='Session ID to load')
def main(command: Optional[str], directory: Optional[str], model: Optional[str],
         verbose: bool, session: Optional[str]):
    """
    LLMCode - AI-Powered Coding Assistant

    Run without arguments for interactive mode, or provide a command to execute once.
    """

    # Load configuration
    config = load_config()

    # Override config with CLI options
    if directory:
        config.working_directory = Path(directory)
    if model:
        config.default_model = model
    if verbose:
        config.verbose = True

    # Check for API key
    if not config.anthropic_api_key:
        console.print("[red]Error: ANTHROPIC_API_KEY not set[/red]")
        console.print("\nSet your API key:")
        console.print("  export ANTHROPIC_API_KEY='your-key-here'")
        console.print("\nOr create a .env file with:")
        console.print("  ANTHROPIC_API_KEY=your-key-here")
        sys.exit(1)

    # Change to working directory
    os.chdir(config.working_directory)

    # Initialize CLI
    cli = LLMCodeCLI(config, config.working_directory)

    # Load session if specified
    if session:
        cli.session.session_id = session
        cli.session.load(cli.llm_client)
        console.print(f"[dim]Loaded session: {session}[/dim]\n")

    # Run
    if command:
        cli.run_single_command(command)
    else:
        cli.run_interactive()


if __name__ == '__main__':
    main()
