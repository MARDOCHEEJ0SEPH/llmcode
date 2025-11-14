"""Node.js and NPM related tools"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, List
from .base import Tool, ToolResult, ToolStatus


class NpmInstallTool(Tool):
    """Tool for installing NPM packages"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory

    @property
    def name(self) -> str:
        return "NpmInstall"

    @property
    def description(self) -> str:
        return "Installs NPM packages. Can install specific packages or run npm install."

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "packages": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of packages to install (empty for npm install)"
                },
                "dev": {
                    "type": "boolean",
                    "description": "Install as dev dependencies"
                },
                "global": {
                    "type": "boolean",
                    "description": "Install globally"
                }
            }
        }

    def execute(self, packages: List[str] = None, dev: bool = False,
                global_install: bool = False) -> ToolResult:
        """Install NPM packages"""
        try:
            if packages:
                cmd = ["npm", "install"]
                if global_install:
                    cmd.append("-g")
                elif dev:
                    cmd.append("--save-dev")
                cmd.extend(packages)
            else:
                cmd = ["npm", "install"]

            result = subprocess.run(
                cmd,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=300
            )

            output = result.stdout
            if result.stderr:
                output += f"\n{result.stderr}"

            status = ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.ERROR

            return ToolResult(
                status=status,
                output=output or "Installation complete",
                metadata={"packages": packages, "dev": dev}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"NPM install error: {str(e)}"
            )


class PackageJsonTool(Tool):
    """Tool for managing package.json"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "PackageJson"

    @property
    def description(self) -> str:
        return "Read or modify package.json file"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["read", "add_script", "add_dependency"],
                    "description": "Action to perform"
                },
                "script_name": {
                    "type": "string",
                    "description": "Name of script (for add_script)"
                },
                "script_command": {
                    "type": "string",
                    "description": "Script command (for add_script)"
                },
                "dependency": {
                    "type": "string",
                    "description": "Dependency name (for add_dependency)"
                },
                "version": {
                    "type": "string",
                    "description": "Dependency version (for add_dependency)"
                }
            },
            "required": ["action"]
        }

    def execute(self, action: str, script_name: str = None,
                script_command: str = None, dependency: str = None,
                version: str = "latest") -> ToolResult:
        """Manage package.json"""
        try:
            pkg_path = Path(self.working_directory) / "package.json"

            if action == "read":
                if not pkg_path.exists():
                    return ToolResult(
                        status=ToolStatus.ERROR,
                        output="",
                        error="package.json not found"
                    )

                with open(pkg_path, 'r') as f:
                    content = f.read()

                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output=content
                )

            # For modification actions, load the file
            if pkg_path.exists():
                with open(pkg_path, 'r') as f:
                    pkg_data = json.load(f)
            else:
                pkg_data = {"name": "app", "version": "1.0.0"}

            if action == "add_script":
                if not script_name or not script_command:
                    return ToolResult(
                        status=ToolStatus.ERROR,
                        output="",
                        error="script_name and script_command required"
                    )

                if "scripts" not in pkg_data:
                    pkg_data["scripts"] = {}

                pkg_data["scripts"][script_name] = script_command

            elif action == "add_dependency":
                if not dependency:
                    return ToolResult(
                        status=ToolStatus.ERROR,
                        output="",
                        error="dependency name required"
                    )

                if "dependencies" not in pkg_data:
                    pkg_data["dependencies"] = {}

                pkg_data["dependencies"][dependency] = version

            # Save modified package.json
            with open(pkg_path, 'w') as f:
                json.dump(pkg_data, f, indent=2)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"package.json updated: {action}",
                metadata={"action": action}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error managing package.json: {str(e)}"
            )


class NpmRunTool(Tool):
    """Tool for running NPM scripts"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory

    @property
    def name(self) -> str:
        return "NpmRun"

    @property
    def description(self) -> str:
        return "Runs NPM scripts defined in package.json"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "script": {
                    "type": "string",
                    "description": "Script name to run (e.g., 'dev', 'build', 'test')"
                },
                "background": {
                    "type": "boolean",
                    "description": "Run in background (for dev servers)"
                }
            },
            "required": ["script"]
        }

    def execute(self, script: str, background: bool = False) -> ToolResult:
        """Run NPM script"""
        try:
            if background:
                # Start in background
                process = subprocess.Popen(
                    ["npm", "run", script],
                    cwd=self.working_directory,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output=f"Started '{script}' in background (PID: {process.pid})",
                    metadata={"pid": process.pid, "script": script}
                )
            else:
                result = subprocess.run(
                    ["npm", "run", script],
                    cwd=self.working_directory,
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                output = result.stdout
                if result.stderr:
                    output += f"\n{result.stderr}"

                status = ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.WARNING

                return ToolResult(
                    status=status,
                    output=output or f"Script '{script}' completed",
                    metadata={"return_code": result.returncode}
                )

        except subprocess.TimeoutExpired:
            return ToolResult(
                status=ToolStatus.WARNING,
                output=f"Script '{script}' timed out (still running)",
                metadata={"timeout": True}
            )
        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error running script: {str(e)}"
            )
