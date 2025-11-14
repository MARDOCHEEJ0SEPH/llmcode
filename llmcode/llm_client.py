"""Core LLM client for interacting with Anthropic Claude API"""

import anthropic
from typing import List, Dict, Any, Optional, Generator
from .tools.base import ToolRegistry, ToolStatus
from .config import Config


class Message:
    """Represents a conversation message"""

    def __init__(self, role: str, content: Any):
        self.role = role
        self.content = content

    def to_dict(self) -> Dict[str, Any]:
        """Convert to API format"""
        return {"role": self.role, "content": self.content}


class LLMClient:
    """Client for interacting with Claude API with tool support"""

    def __init__(self, config: Config, tool_registry: ToolRegistry):
        self.config = config
        self.tool_registry = tool_registry
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        self.conversation_history: List[Message] = []

    def add_system_prompt(self) -> str:
        """Generate system prompt"""
        return """You are an AI coding assistant similar to Claude Code. You help users with:
- Writing and editing code
- Debugging and fixing issues
- Explaining code and concepts
- Running commands and tests
- Searching and navigating codebases

You have access to various tools for file operations, command execution, and web access.
Always use the appropriate tools to complete tasks effectively.

When using tools:
- Read files before editing them
- Use Bash for running commands
- Use Glob and Grep for searching
- Be thorough and methodical

Provide clear, concise responses and always explain what you're doing."""

    def send_message(
        self,
        user_message: str,
        max_iterations: int = 10
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Send a message and handle tool use iterations

        Yields events:
        - {"type": "text", "content": str}
        - {"type": "tool_use", "tool": str, "input": dict}
        - {"type": "tool_result", "tool": str, "result": str}
        - {"type": "error", "error": str}
        """

        # Add user message
        self.conversation_history.append(Message("user", user_message))

        for iteration in range(max_iterations):
            # Prepare messages for API
            messages = [msg.to_dict() for msg in self.conversation_history]

            try:
                # Call Claude API
                response = self.client.messages.create(
                    model=self.config.default_model,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    system=self.add_system_prompt(),
                    messages=messages,
                    tools=self.tool_registry.to_anthropic_tools()
                )

                # Process response content
                assistant_content = []
                has_tool_use = False

                for block in response.content:
                    if block.type == "text":
                        yield {"type": "text", "content": block.text}
                        assistant_content.append(block.model_dump())

                    elif block.type == "tool_use":
                        has_tool_use = True
                        tool_name = block.name
                        tool_input = block.input

                        yield {
                            "type": "tool_use",
                            "tool": tool_name,
                            "input": tool_input
                        }

                        # Execute tool
                        tool = self.tool_registry.get(tool_name)
                        if tool:
                            result = tool.execute(**tool_input)

                            yield {
                                "type": "tool_result",
                                "tool": tool_name,
                                "result": result.output,
                                "status": result.status.value
                            }

                            # Add tool use to assistant message
                            assistant_content.append(block.model_dump())

                            # Prepare tool result for next iteration
                            if not hasattr(self, '_current_tool_results'):
                                self._current_tool_results = []

                            self._current_tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.output if result.status == ToolStatus.SUCCESS
                                          else f"Error: {result.error}"
                            })
                        else:
                            yield {
                                "type": "error",
                                "error": f"Unknown tool: {tool_name}"
                            }

                # Add assistant message to history
                self.conversation_history.append(Message("assistant", assistant_content))

                # If there were tool uses, add tool results and continue
                if has_tool_use and hasattr(self, '_current_tool_results'):
                    self.conversation_history.append(
                        Message("user", self._current_tool_results)
                    )
                    self._current_tool_results = []
                    continue  # Next iteration

                # No more tool uses, we're done
                if response.stop_reason == "end_turn":
                    break

            except Exception as e:
                yield {"type": "error", "error": str(e)}
                break

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_history(self) -> List[Message]:
        """Get conversation history"""
        return self.conversation_history
