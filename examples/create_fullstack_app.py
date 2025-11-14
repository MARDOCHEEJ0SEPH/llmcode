"""
Example: Create a full-stack application with LLMCode

This example demonstrates how to use LLMCode to create a complete
full-stack application with React frontend, Express backend, MongoDB,
Redis, and Docker support.
"""

from pathlib import Path
from llmcode.config import Config
from llmcode.llm_client import LLMClient
from llmcode.tools.base import ToolRegistry
from llmcode.tools.scaffold_tools import CreateFullStackAppTool, CreateReactAppTool, CreateExpressAppTool
from llmcode.tools.database_tools import MongoDBSetupTool, RedisSetupTool
from llmcode.tools.security_tools import JWTAuthSetupTool, CORSSetupTool
from llmcode.tools.docker_tools import DockerComposeTool
from llmcode.tools.api_tools import APIEndpointGeneratorTool


def create_fullstack_app():
    """Create a complete full-stack application"""

    # Set up configuration
    config = Config()
    config.working_directory = Path.cwd() / "my-fullstack-app"

    # Set up tool registry with all necessary tools
    tool_registry = ToolRegistry()

    # Register scaffolding tools
    tool_registry.register(CreateFullStackAppTool(str(config.working_directory)))
    tool_registry.register(CreateReactAppTool(str(config.working_directory)))
    tool_registry.register(CreateExpressAppTool(str(config.working_directory)))

    # Register database tools
    tool_registry.register(MongoDBSetupTool(str(config.working_directory)))
    tool_registry.register(RedisSetupTool(str(config.working_directory)))

    # Register security tools
    tool_registry.register(JWTAuthSetupTool(str(config.working_directory)))
    tool_registry.register(CORSSetupTool(str(config.working_directory)))

    # Register Docker tools
    tool_registry.register(DockerComposeTool(str(config.working_directory)))

    # Register API tools
    tool_registry.register(APIEndpointGeneratorTool(str(config.working_directory)))

    # Create LLM client
    client = LLMClient(config, tool_registry)

    print("Creating full-stack application...")
    print()

    # Send instruction to create the app
    message = """
    Create a complete full-stack application with the following requirements:

    1. Create a full-stack app structure with React frontend and Express backend
    2. Set up MongoDB for the database
    3. Set up Redis for caching
    4. Add JWT authentication with login/register endpoints
    5. Add CORS configuration for cross-origin requests
    6. Create API endpoints for a "User" resource with CRUD operations
    7. Set up Docker Compose with all services (app, MongoDB, Redis)
    8. Use TypeScript for both frontend and backend

    Please create all necessary files and configurations.
    """

    for event in client.send_message(message):
        if event["type"] == "text":
            print(event["content"], end="", flush=True)
        elif event["type"] == "tool_use":
            print(f"\n\n🔧 Using: {event['tool']}")
        elif event["type"] == "tool_result":
            print(f"✓ {event['tool']} completed")
        elif event["type"] == "error":
            print(f"\n❌ Error: {event['error']}")

    print("\n\n✅ Full-stack application created!")
    print(f"Location: {config.working_directory}")
    print("\nNext steps:")
    print("1. cd my-fullstack-app")
    print("2. npm run install:all")
    print("3. docker-compose up -d")
    print("4. npm run dev")


if __name__ == "__main__":
    create_fullstack_app()
