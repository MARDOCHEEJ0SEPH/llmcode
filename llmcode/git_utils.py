"""Git repository utilities"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess


class GitRepo:
    """Git repository information and operations"""

    def __init__(self, path: Optional[Path] = None):
        self.path = path or Path.cwd()
        self.is_repo = self._check_is_repo()

    def _check_is_repo(self) -> bool:
        """Check if directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get git repository status"""
        if not self.is_repo:
            return {"is_repo": False}

        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.path,
                capture_output=True,
                text=True,
                timeout=5
            )
            branch = branch_result.stdout.strip()

            # Get status
            status_result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.path,
                capture_output=True,
                text=True,
                timeout=5
            )
            status = status_result.stdout.strip()

            # Get recent commits
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=self.path,
                capture_output=True,
                text=True,
                timeout=5
            )
            recent_commits = log_result.stdout.strip()

            # Check for changes
            has_changes = bool(status)

            return {
                "is_repo": True,
                "branch": branch,
                "status": status if status else "(clean)",
                "recent_commits": recent_commits,
                "has_changes": has_changes
            }

        except Exception as e:
            return {
                "is_repo": True,
                "error": str(e)
            }

    def get_context_message(self) -> str:
        """Get git context for LLM"""
        status = self.get_status()

        if not status.get("is_repo"):
            return "Not a git repository"

        if "error" in status:
            return f"Git error: {status['error']}"

        message = f"Git Repository Context:\n"
        message += f"Current branch: {status.get('branch', 'unknown')}\n"
        message += f"Status:\n{status.get('status', 'clean')}\n"

        if status.get('recent_commits'):
            message += f"\nRecent commits:\n{status['recent_commits']}\n"

        return message
