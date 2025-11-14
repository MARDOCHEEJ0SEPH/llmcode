"""Tool system for LLMCode"""

from .base import Tool, ToolResult
from .file_tools import ReadTool, WriteTool, EditTool
from .bash_tool import BashTool
from .search_tools import GlobTool, GrepTool
from .web_tools import WebSearchTool, WebFetchTool
from .node_tools import NpmInstallTool, PackageJsonTool, NpmRunTool
from .scaffold_tools import (
    CreateReactAppTool,
    CreateVueAppTool,
    CreateExpressAppTool,
    CreateFullStackAppTool
)
from .database_tools import MongoDBSetupTool, RedisSetupTool, PostgreSQLSetupTool
from .docker_tools import DockerfileGeneratorTool, DockerComposeTool, DockerCommandTool
from .security_tools import JWTAuthSetupTool, RateLimitSetupTool, CORSSetupTool
from .api_tools import APIEndpointGeneratorTool, SwaggerSetupTool

__all__ = [
    "Tool",
    "ToolResult",
    # File tools
    "ReadTool",
    "WriteTool",
    "EditTool",
    # System tools
    "BashTool",
    "GlobTool",
    "GrepTool",
    # Web tools
    "WebSearchTool",
    "WebFetchTool",
    # Node.js tools
    "NpmInstallTool",
    "PackageJsonTool",
    "NpmRunTool",
    # Scaffolding tools
    "CreateReactAppTool",
    "CreateVueAppTool",
    "CreateExpressAppTool",
    "CreateFullStackAppTool",
    # Database tools
    "MongoDBSetupTool",
    "RedisSetupTool",
    "PostgreSQLSetupTool",
    # Docker tools
    "DockerfileGeneratorTool",
    "DockerComposeTool",
    "DockerCommandTool",
    # Security tools
    "JWTAuthSetupTool",
    "RateLimitSetupTool",
    "CORSSetupTool",
    # API tools
    "APIEndpointGeneratorTool",
    "SwaggerSetupTool",
]
