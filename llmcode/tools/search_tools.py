"""File search tools"""

import glob
import re
import os
from pathlib import Path
from typing import Any, Dict, Optional, List
from .base import Tool, ToolResult, ToolStatus


class GlobTool(Tool):
    """Tool for finding files using glob patterns"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or os.getcwd()

    @property
    def name(self) -> str:
        return "Glob"

    @property
    def description(self) -> str:
        return "Finds files matching a glob pattern (e.g., '**/*.py', 'src/**/*.js')"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to match files"
                },
                "path": {
                    "type": "string",
                    "description": "Directory to search in (optional)"
                }
            },
            "required": ["pattern"]
        }

    def execute(self, pattern: str, path: Optional[str] = None) -> ToolResult:
        """Find files matching pattern"""
        try:
            search_path = Path(path) if path else Path(self.working_directory)

            if not search_path.exists():
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output="",
                    error=f"Path does not exist: {search_path}"
                )

            matches = list(search_path.glob(pattern))
            matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)

            if not matches:
                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output="No files found matching pattern",
                    metadata={"count": 0}
                )

            output_lines = [str(match.relative_to(search_path)) for match in matches[:100]]
            if len(matches) > 100:
                output_lines.append(f"\n... and {len(matches) - 100} more files")

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output="\n".join(output_lines),
                metadata={"count": len(matches)}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error searching files: {str(e)}"
            )


class GrepTool(Tool):
    """Tool for searching file contents"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or os.getcwd()

    @property
    def name(self) -> str:
        return "Grep"

    @property
    def description(self) -> str:
        return "Searches for a pattern in file contents using regex"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Regex pattern to search for"
                },
                "path": {
                    "type": "string",
                    "description": "File or directory to search in"
                },
                "glob": {
                    "type": "string",
                    "description": "Glob pattern to filter files (e.g., '*.py')"
                },
                "case_insensitive": {
                    "type": "boolean",
                    "description": "Case insensitive search"
                }
            },
            "required": ["pattern"]
        }

    def execute(self, pattern: str, path: Optional[str] = None,
                glob_pattern: Optional[str] = None,
                case_insensitive: bool = False) -> ToolResult:
        """Search for pattern in files"""
        try:
            search_path = Path(path) if path else Path(self.working_directory)

            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)

            matches: List[str] = []
            files_searched = 0

            # Get files to search
            if search_path.is_file():
                files = [search_path]
            elif glob_pattern:
                files = list(search_path.glob(glob_pattern))
            else:
                files = list(search_path.rglob("*"))
                files = [f for f in files if f.is_file()]

            for file_path in files[:1000]:  # Limit to 1000 files
                if not file_path.is_file():
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        files_searched += 1
                        for line_num, line in enumerate(f, 1):
                            if regex.search(line):
                                rel_path = file_path.relative_to(self.working_directory)
                                matches.append(f"{rel_path}:{line_num}:{line.rstrip()}")
                                if len(matches) >= 100:  # Limit results
                                    break
                    if len(matches) >= 100:
                        break
                except:
                    continue

            if not matches:
                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output=f"No matches found (searched {files_searched} files)",
                    metadata={"matches": 0, "files_searched": files_searched}
                )

            output = "\n".join(matches)
            if len(matches) >= 100:
                output += "\n... (results truncated)"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"matches": len(matches), "files_searched": files_searched}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error searching: {str(e)}"
            )
