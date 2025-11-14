# LLMCode - AI-Powered Coding Assistant

A powerful command-line AI coding assistant powered by Claude, designed to help with software development tasks.

## Features

- **Natural Language Coding**: Describe what you want in plain English
- **File Operations**: Read, write, edit files with AI assistance
- **Code Execution**: Run bash commands and scripts
- **Git Integration**: Automatic git awareness and operations
- **Web Capabilities**: Search and fetch web content
- **Agent System**: Complex multi-step task execution
- **Rich CLI**: Beautiful terminal interface with syntax highlighting

## Installation

```bash
# Install dependencies
pip install -e .

# Set up your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Quick Start

```bash
# Start interactive session
llmcode

# Run a single command
llmcode "Create a Python script that prints hello world"

# Work in a specific directory
llmcode --directory /path/to/project
```

## Usage

### Interactive Mode

```bash
llmcode
```

Once in interactive mode, you can:
- Ask questions about your code
- Request file modifications
- Run commands
- Execute complex multi-step tasks

### Example Commands

```
> Create a Python FastAPI application
> Add error handling to app.py
> Run the tests and fix any failures
> Explain what this function does
> Refactor this code to be more efficient
```

## Configuration

Create a `.llmcode.yaml` file in your project root:

```yaml
model: claude-sonnet-4-5-20250929
max_tokens: 8000
temperature: 1.0
```

## Architecture

- **CLI Layer**: User interface and command handling
- **LLM Client**: Anthropic API integration with tool use
- **Tool System**: Extensible tools for various operations
- **Agent Framework**: Complex task orchestration
- **Session Manager**: Conversation and context management

## Tools Available

- **Read**: Read file contents
- **Write**: Create new files
- **Edit**: Modify existing files
- **Bash**: Execute shell commands
- **Glob**: Find files by pattern
- **Grep**: Search file contents
- **WebSearch**: Search the web
- **WebFetch**: Fetch web page content
- **Task**: Launch specialized agents

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .
ruff check .
```

## License

MIT License
