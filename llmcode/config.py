"""Configuration management for LLMCode"""

import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration"""

    # API Configuration
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")

    # Model Configuration
    default_model: str = Field(
        default="claude-sonnet-4-5-20250929",
        env="DEFAULT_MODEL"
    )
    max_tokens: int = Field(default=8000, env="MAX_TOKENS")
    temperature: float = Field(default=1.0, env="TEMPERATURE")

    # Web Search (optional)
    serper_api_key: Optional[str] = Field(default=None, env="SERPER_API_KEY")

    # Paths
    working_directory: Path = Field(default_factory=Path.cwd)
    session_dir: Path = Field(default_factory=lambda: Path.home() / ".llmcode_sessions")

    # CLI Settings
    verbose: bool = Field(default=False)
    auto_save_sessions: bool = Field(default=True)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def load_config(env_file: Optional[str] = None) -> Config:
    """Load configuration from environment and .env file"""
    if env_file and os.path.exists(env_file):
        return Config(_env_file=env_file)
    return Config()
