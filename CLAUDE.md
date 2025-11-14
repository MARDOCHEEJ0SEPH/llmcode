# CLAUDE.md - AI Assistant Guide for LLMCode

This document provides comprehensive information about the LLMCode codebase for AI assistants to effectively understand and work with this project.

## Project Overview

**LLMCode** is an AI-powered coding assistant similar to Claude Code. It's a Python-based command-line tool that integrates with the Anthropic Claude API to provide intelligent coding assistance through natural language interactions.

### Key Features

- Natural language interface for coding tasks
- Extensible tool system for file operations, command execution, and web access
- Session management and conversation history
- Git repository awareness
- Rich CLI with syntax highlighting and formatting
- Web search and fetch capabilities

## Architecture

### System Components

```
┌─────────────────────────────────────────────────┐
│                CLI Interface                     │
│              (llmcode/cli.py)                    │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│             LLM Client                           │
│         (llmcode/llm_client.py)                  │
│  - Manages conversation with Claude API          │
│  - Handles tool use iterations                   │
│  - Streams responses                             │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│            Tool Registry                         │
│         (llmcode/tools/base.py)                  │
│  - Manages available tools                       │
│  - Converts tools to Anthropic format            │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────┐    ┌──────────────────┐
│  File Tools  │    │   Other Tools    │
│  - Read      │    │   - Bash         │
│  - Write     │    │   - Glob         │
│  - Edit      │    │   - Grep         │
└──────────────┘    │   - WebSearch    │
                    │   - WebFetch     │
                    └──────────────────┘
```

### Core Modules

#### 1. `llmcode/cli.py` - Command Line Interface
- **Purpose**: Main entry point for the application
- **Key Classes**: `LLMCodeCLI`
- **Features**:
  - Interactive REPL mode
  - Single command execution
  - Rich terminal formatting with syntax highlighting
  - Session management commands (`/save`, `/clear`, `/sessions`)
  - Git status display

#### 2. `llmcode/llm_client.py` - LLM Client
- **Purpose**: Manages communication with Anthropic Claude API
- **Key Classes**: `LLMClient`, `Message`
- **Features**:
  - Streaming responses with tool use
  - Tool execution iteration (up to 10 iterations)
  - Conversation history management
  - Event-based API for different response types:
    - `text`: Text content from Claude
    - `tool_use`: Claude requesting to use a tool
    - `tool_result`: Result from tool execution
    - `error`: Error occurred

#### 3. `llmcode/tools/` - Tool System
- **Purpose**: Extensible tool framework for various operations
- **Key Classes**: `Tool`, `ToolResult`, `ToolRegistry`

**Available Tools**:

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `Read` | Read file contents | `file_path`, `offset`, `limit` | File contents with line numbers |
| `Write` | Create/overwrite files | `file_path`, `content` | Success message |
| `Edit` | Modify existing files | `file_path`, `old_string`, `new_string`, `replace_all` | Success with replacement count |
| `Bash` | Execute shell commands | `command`, `timeout` | Command output (stdout/stderr) |
| `Glob` | Find files by pattern | `pattern`, `path` | List of matching files |
| `Grep` | Search file contents | `pattern`, `path`, `glob`, `case_insensitive` | Matching lines with file:line:content |
| `WebSearch` | Search the web | `query` | Search results (requires API key) |
| `WebFetch` | Fetch web page | `url` | Page content |

#### 4. `llmcode/session.py` - Session Management
- **Purpose**: Save and restore conversation sessions
- **Features**:
  - Auto-save functionality
  - Session listing
  - JSON-based storage in `~/.llmcode_sessions/`

#### 5. `llmcode/config.py` - Configuration
- **Purpose**: Application configuration management
- **Uses**: Pydantic Settings for environment-based config
- **Configuration Sources**:
  1. Environment variables
  2. `.env` file
  3. Default values

**Key Configuration Options**:
```python
ANTHROPIC_API_KEY    # Required: Anthropic API key
DEFAULT_MODEL        # Model to use (default: claude-sonnet-4-5-20250929)
MAX_TOKENS          # Max response tokens (default: 8000)
TEMPERATURE         # Sampling temperature (default: 1.0)
SERPER_API_KEY      # Optional: For web search
```

#### 6. `llmcode/git_utils.py` - Git Integration
- **Purpose**: Git repository awareness and operations
- **Features**:
  - Detect if working directory is a git repo
  - Get current branch and status
  - Show recent commits
  - Provide git context to LLM

## Project Structure

```
llmcode/
├── llmcode/                 # Main package
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # CLI interface
│   ├── llm_client.py       # LLM client
│   ├── session.py          # Session management
│   ├── config.py           # Configuration
│   ├── git_utils.py        # Git utilities
│   └── tools/              # Tool system
│       ├── __init__.py
│       ├── base.py         # Base tool classes
│       ├── file_tools.py   # Read, Write, Edit
│       ├── bash_tool.py    # Bash execution
│       ├── search_tools.py # Glob, Grep
│       └── web_tools.py    # Web search/fetch
├── examples/               # Usage examples
│   ├── basic_usage.py      # Programmatic usage
│   └── custom_tool.py      # Custom tool example
├── tests/                  # Test suite
│   └── test_tools.py       # Tool tests
├── pyproject.toml          # Project metadata and dependencies
├── setup.sh                # Setup script
├── README.md               # User documentation
├── CLAUDE.md               # This file - AI assistant guide
├── .env.example            # Environment variable template
└── .gitignore              # Git ignore rules
```

## Development Workflows

### Adding a New Tool

1. Create a new class inheriting from `Tool` in appropriate file
2. Implement required properties:
   - `name`: Tool name (must be unique)
   - `description`: What the tool does
   - `input_schema`: JSON schema for input parameters
3. Implement `execute(**kwargs)` method
4. Return a `ToolResult` with status and output
5. Register the tool in `LLMCodeCLI._register_tools()`

**Example**:
```python
from llmcode.tools.base import Tool, ToolResult, ToolStatus

class MyTool(Tool):
    @property
    def name(self) -> str:
        return "MyTool"

    @property
    def description(self) -> str:
        return "Does something useful"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "param": {"type": "string", "description": "A parameter"}
            },
            "required": ["param"]
        }

    def execute(self, param: str) -> ToolResult:
        try:
            # Do something
            return ToolResult(
                status=ToolStatus.SUCCESS,
                output="Result here"
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=str(e)
            )
```

### Making Code Changes

1. **Reading Code**: Use the `Read` tool to view files
2. **Editing Code**: Prefer `Edit` tool over `Write` for existing files
3. **Testing**: Run tests with `Bash` tool: `pytest tests/`
4. **Formatting**: Use `black .` and `ruff check .`

### Testing Strategy

- **Unit Tests**: In `tests/` directory using pytest
- **Tool Tests**: Test each tool's execute method
- **Integration Tests**: Test LLM client with mock responses
- **Manual Testing**: Use interactive mode for end-to-end testing

## Key Conventions

### Code Style

- **Formatting**: Black with 100 character line length
- **Linting**: Ruff for additional checks
- **Type Hints**: Use type hints for all function signatures
- **Docstrings**: Google-style docstrings for classes and functions

### Error Handling

- Tools should catch exceptions and return `ToolResult` with `ToolStatus.ERROR`
- Include helpful error messages in `ToolResult.error`
- Don't let exceptions propagate from tool execution

### Tool Design Principles

1. **Single Responsibility**: Each tool does one thing well
2. **Clear Inputs**: Well-defined input schemas
3. **Informative Output**: Return useful information
4. **Error Messages**: Provide actionable error messages
5. **Metadata**: Include relevant metadata in results

### File Operations

- **Paths**: Always use absolute paths
- **Line Numbers**: Read tool returns 1-indexed line numbers
- **Encoding**: Default to UTF-8 with error handling
- **Truncation**: Limit output for very large files/results

## Common Patterns

### Tool Execution Flow

```python
# 1. User sends message
user_message = "Create a Python file"

# 2. LLM client processes message
for event in llm_client.send_message(user_message):
    # 3. Claude returns text or requests tool use
    if event["type"] == "tool_use":
        tool = tool_registry.get(event["tool"])
        result = tool.execute(**event["input"])
        # 4. Tool result sent back to Claude
        # 5. Claude continues or returns final response
```

### Session Management

```python
# Auto-save after each interaction
if config.auto_save_sessions:
    session.save(llm_client)

# Load previous session
session = Session(session_id="20241114_123456")
session.load(llm_client)
```

### Configuration Loading

```python
# Loads from environment and .env file
config = load_config()

# Access configuration
api_key = config.anthropic_api_key
model = config.default_model
```

## Environment Setup

### Requirements

- Python 3.8+
- Anthropic API key
- Optional: Serper API key for web search

### Installation

```bash
# Clone repository
git clone <repo-url>
cd llmcode

# Run setup script
bash setup.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Configure API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### Running

```bash
# Interactive mode
llmcode

# Single command
llmcode "Create a Python script that prints hello world"

# Specify working directory
llmcode --directory /path/to/project

# Verbose mode
llmcode --verbose

# Load session
llmcode --session 20241114_123456
```

## API Reference

### LLMClient

```python
class LLMClient:
    def __init__(self, config: Config, tool_registry: ToolRegistry)

    def send_message(self, user_message: str, max_iterations: int = 10) -> Generator[Dict[str, Any], None, None]
        """
        Yields events:
        - {"type": "text", "content": str}
        - {"type": "tool_use", "tool": str, "input": dict}
        - {"type": "tool_result", "tool": str, "result": str, "status": str}
        - {"type": "error", "error": str}
        """

    def clear_history(self) -> None
    def get_history(self) -> List[Message]
```

### Tool

```python
class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str

    @property
    @abstractmethod
    def description(self) -> str

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult

    def to_anthropic_tool(self) -> Dict[str, Any]
```

### ToolResult

```python
@dataclass
class ToolResult:
    status: ToolStatus  # SUCCESS, ERROR, WARNING
    output: str
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
```

## Debugging Tips

1. **Enable Verbose Mode**: Use `--verbose` flag to see detailed tool execution
2. **Check Sessions**: Saved sessions in `~/.llmcode_sessions/` contain full conversation history
3. **API Errors**: Check API key and rate limits if seeing authentication errors
4. **Tool Failures**: Tool results include error messages and metadata for debugging

## Extension Points

### Custom Tools
Create new tools by inheriting from `Tool` class (see examples/custom_tool.py)

### Custom System Prompt
Modify `LLMClient.add_system_prompt()` to customize AI behavior

### Additional Output Formats
Extend CLI to support different output formats (JSON, markdown files, etc.)

### Agent System
Future: Implement specialized agents for complex multi-step tasks

## Performance Considerations

- **Token Usage**: Large tool outputs consume tokens; truncate when necessary
- **Tool Iterations**: Limited to 10 iterations to prevent infinite loops
- **File Reading**: Offset and limit parameters for large files
- **Search Results**: Capped at 100 results to prevent overwhelming responses
- **Timeouts**: Bash tool has 120s default timeout

## Security Considerations

- **Command Execution**: Bash tool executes arbitrary commands - use in trusted environments only
- **File Access**: Tools have full filesystem access based on user permissions
- **API Keys**: Never commit API keys; use environment variables
- **Web Requests**: WebFetch follows redirects and can access any URL

## Future Enhancements

Potential areas for expansion:
- [ ] Specialized agent system for complex tasks
- [ ] Code analysis and linting tools
- [ ] Database query tools
- [ ] Docker/container integration
- [ ] IDE integration (VS Code extension)
- [ ] Multi-file editing capabilities
- [ ] Syntax-aware code transformations
- [ ] Git operations (commit, push, PR creation)
- [ ] Test generation and execution
- [ ] Documentation generation

## Troubleshooting

### Common Issues

**Issue**: "ANTHROPIC_API_KEY not set"
- **Solution**: Set environment variable or create .env file

**Issue**: Tool execution timeout
- **Solution**: Increase timeout parameter or optimize command

**Issue**: File not found errors
- **Solution**: Ensure using absolute paths, check working directory

**Issue**: Import errors
- **Solution**: Install in development mode with `pip install -e .`

## Contributing Guidelines

When modifying this codebase:

1. **Test Changes**: Add tests for new functionality
2. **Document**: Update this CLAUDE.md and README.md
3. **Format Code**: Run `black .` before committing
4. **Type Check**: Ensure type hints are present and correct
5. **Tool Schema**: Keep input_schema accurate for tool changes

## Resources

- Anthropic API Docs: https://docs.anthropic.com/
- Tool Use Guide: https://docs.anthropic.com/claude/docs/tool-use
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- Rich Documentation: https://rich.readthedocs.io/

---

**Last Updated**: 2024-11-14
**Version**: 0.1.0
**Maintainers**: LLMCode Team
