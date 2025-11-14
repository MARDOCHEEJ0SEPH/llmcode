"""
Example of creating a custom tool for LLMCode
"""

from typing import Any, Dict
from llmcode.tools.base import Tool, ToolResult, ToolStatus


class CalculatorTool(Tool):
    """Example custom tool that performs calculations"""

    @property
    def name(self) -> str:
        return "Calculator"

    @property
    def description(self) -> str:
        return "Performs basic mathematical calculations. Supports +, -, *, /"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2')"
                }
            },
            "required": ["expression"]
        }

    def execute(self, expression: str) -> ToolResult:
        """Execute calculation"""
        try:
            # Evaluate the expression safely
            # In production, use a safer evaluation method
            result = eval(expression, {"__builtins__": {}}, {})

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"{expression} = {result}",
                metadata={"result": result}
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Calculation error: {str(e)}"
            )


def main():
    """Example of using a custom tool"""
    from llmcode.config import Config
    from llmcode.llm_client import LLMClient
    from llmcode.tools.base import ToolRegistry

    # Set up configuration
    config = Config()

    # Create tool registry and add custom tool
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())

    # Create LLM client
    client = LLMClient(config, tool_registry)

    # Use the custom tool
    for event in client.send_message("What is 42 * 137?"):
        if event["type"] == "text":
            print(event["content"], end="", flush=True)
        elif event["type"] == "tool_use":
            print(f"\n[Using {event['tool']}]")
        elif event["type"] == "tool_result":
            print(f"Result: {event['result']}")

    print("\n")


if __name__ == "__main__":
    main()
