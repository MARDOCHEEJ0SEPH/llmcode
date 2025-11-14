"""
Basic usage example for LLMCode

This demonstrates how to use LLMCode programmatically.
"""

from pathlib import Path
from llmcode.config import Config
from llmcode.llm_client import LLMClient
from llmcode.tools.base import ToolRegistry
from llmcode.tools.file_tools import ReadTool, WriteTool, EditTool
from llmcode.tools.bash_tool import BashTool


def main():
    """Example of using LLMCode programmatically"""

    # Set up configuration
    config = Config()
    config.working_directory = Path.cwd()

    # Set up tool registry
    tool_registry = ToolRegistry()
    tool_registry.register(ReadTool())
    tool_registry.register(WriteTool())
    tool_registry.register(EditTool())
    tool_registry.register(BashTool())

    # Create LLM client
    client = LLMClient(config, tool_registry)

    # Send a message
    print("Sending message to AI assistant...")
    print()

    for event in client.send_message("Create a Python file called hello.py that prints 'Hello, World!'"):
        if event["type"] == "text":
            print(event["content"], end="", flush=True)
        elif event["type"] == "tool_use":
            print(f"\n[Using tool: {event['tool']}]", flush=True)
        elif event["type"] == "tool_result":
            print(f"[Tool completed: {event['tool']}]", flush=True)
        elif event["type"] == "error":
            print(f"\nError: {event['error']}", flush=True)

    print("\n\nDone!")


if __name__ == "__main__":
    main()
