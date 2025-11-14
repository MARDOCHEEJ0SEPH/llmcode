"""Bash command execution tool"""

import subprocess
import os
from typing import Any, Dict, Optional
from .base import Tool, ToolResult, ToolStatus


class BashTool(Tool):
    """Tool for executing bash commands"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or os.getcwd()

    @property
    def name(self) -> str:
        return "Bash"

    @property
    def description(self) -> str:
        return "Executes bash commands in a shell. Returns stdout and stderr."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to execute"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds (default: 120)"
                }
            },
            "required": ["command"]
        }

    def execute(self, command: str, timeout: int = 120) -> ToolResult:
        """Execute bash command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.working_directory
            )

            output = result.stdout
            if result.stderr:
                output += f"\n[STDERR]\n{result.stderr}"

            status = ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.WARNING

            return ToolResult(
                status=status,
                output=output or "(no output)",
                metadata={
                    "return_code": result.returncode,
                    "command": command
                }
            )

        except subprocess.TimeoutExpired:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Command timed out after {timeout} seconds"
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error executing command: {str(e)}"
            )
