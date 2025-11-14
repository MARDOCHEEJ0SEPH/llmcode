"""File operation tools"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from .base import Tool, ToolResult, ToolStatus


class ReadTool(Tool):
    """Tool for reading file contents"""

    @property
    def name(self) -> str:
        return "Read"

    @property
    def description(self) -> str:
        return "Reads a file from the filesystem. Returns file contents with line numbers."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file to read"
                },
                "offset": {
                    "type": "integer",
                    "description": "Line number to start reading from (optional)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of lines to read (optional)"
                }
            },
            "required": ["file_path"]
        }

    def execute(self, file_path: str, offset: int = 0, limit: Optional[int] = None) -> ToolResult:
        """Read file contents"""
        try:
            path = Path(file_path)

            if not path.exists():
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"File not found: {file_path}"
                )

            if not path.is_file():
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Path is not a file: {file_path}"
                )

            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Apply offset and limit
            start = offset
            end = len(lines) if limit is None else start + limit
            selected_lines = lines[start:end]

            # Add line numbers
            output_lines = [
                f"{i + start + 1:6d}\t{line.rstrip()}"
                for i, line in enumerate(selected_lines)
            ]

            output = "\n".join(output_lines)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={
                    "total_lines": len(lines),
                    "lines_read": len(selected_lines)
                }
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error reading file: {str(e)}"
            )


class WriteTool(Tool):
    """Tool for writing files"""

    @property
    def name(self) -> str:
        return "Write"

    @property
    def description(self) -> str:
        return "Writes content to a file. Creates new file or overwrites existing file."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }

    def execute(self, file_path: str, content: str) -> ToolResult:
        """Write content to file"""
        try:
            path = Path(file_path)

            # Create parent directories if they don't exist
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"File written successfully: {file_path}",
                metadata={
                    "bytes_written": len(content.encode('utf-8')),
                    "lines_written": len(content.splitlines())
                }
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error writing file: {str(e)}"
            )


class EditTool(Tool):
    """Tool for editing existing files"""

    @property
    def name(self) -> str:
        return "Edit"

    @property
    def description(self) -> str:
        return "Edits a file by replacing old_string with new_string. The old_string must match exactly."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file to edit"
                },
                "old_string": {
                    "type": "string",
                    "description": "The exact string to replace"
                },
                "new_string": {
                    "type": "string",
                    "description": "The replacement string"
                },
                "replace_all": {
                    "type": "boolean",
                    "description": "Replace all occurrences (default: false)"
                }
            },
            "required": ["file_path", "old_string", "new_string"]
        }

    def execute(self, file_path: str, old_string: str, new_string: str,
                replace_all: bool = False) -> ToolResult:
        """Edit file by replacing text"""
        try:
            path = Path(file_path)

            if not path.exists():
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"File not found: {file_path}"
                )

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_string not in content:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"String not found in file: {old_string[:100]}..."
                )

            # Check if replacement is ambiguous
            if not replace_all and content.count(old_string) > 1:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"String appears {content.count(old_string)} times. Use replace_all=true or provide more context."
                )

            # Perform replacement
            if replace_all:
                new_content = content.replace(old_string, new_string)
                replacements = content.count(old_string)
            else:
                new_content = content.replace(old_string, new_string, 1)
                replacements = 1

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"File edited successfully. Made {replacements} replacement(s).",
                metadata={"replacements": replacements}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error editing file: {str(e)}"
            )
