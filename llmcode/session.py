"""Session management for LLMCode"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from .llm_client import LLMClient, Message


class Session:
    """Manages a conversation session"""

    def __init__(self, session_id: Optional[str] = None, session_dir: Optional[Path] = None):
        self.session_id = session_id or self._generate_session_id()
        self.session_dir = session_dir or Path.home() / ".llmcode_sessions"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.session_file = self.session_dir / f"{self.session_id}.json"
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }

    def _generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def save(self, llm_client: LLMClient) -> None:
        """Save session to disk"""
        history = llm_client.get_history()

        # Convert messages to serializable format
        messages = []
        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        self.metadata["last_updated"] = datetime.now().isoformat()
        self.metadata["message_count"] = len(messages)

        data = {
            "session_id": self.session_id,
            "metadata": self.metadata,
            "messages": messages
        }

        with open(self.session_file, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self, llm_client: LLMClient) -> None:
        """Load session from disk"""
        if not self.session_file.exists():
            return

        with open(self.session_file, 'r') as f:
            data = json.load(f)

        self.metadata = data.get("metadata", {})

        # Restore conversation history
        llm_client.conversation_history = []
        for msg_data in data.get("messages", []):
            llm_client.conversation_history.append(
                Message(msg_data["role"], msg_data["content"])
            )

    @staticmethod
    def list_sessions(session_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
        """List all saved sessions"""
        session_dir = session_dir or Path.home() / ".llmcode_sessions"

        if not session_dir.exists():
            return []

        sessions = []
        for session_file in session_dir.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    data = json.load(f)
                    sessions.append({
                        "session_id": data.get("session_id"),
                        "created_at": data.get("metadata", {}).get("created_at"),
                        "last_updated": data.get("metadata", {}).get("last_updated"),
                        "message_count": data.get("metadata", {}).get("message_count", 0)
                    })
            except:
                continue

        return sorted(sessions, key=lambda x: x.get("last_updated", ""), reverse=True)
