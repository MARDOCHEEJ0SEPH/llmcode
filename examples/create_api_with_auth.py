"""
Example: Create a REST API with Authentication

This example shows how to create a secure REST API with:
- Express.js backend
- MongoDB database
- JWT authentication
- Rate limiting
- CORS configuration
- Swagger documentation
"""

from pathlib import Path
from llmcode.config import Config
from llmcode.llm_client import LLMClient
from llmcode.tools.base import ToolRegistry
from llmcode.tools.scaffold_tools import CreateExpressAppTool
from llmcode.tools.database_tools import MongoDBSetupTool
from llmcode.tools.security_tools import JWTAuthSetupTool, RateLimitSetupTool, CORSSetupTool
from llmcode.tools.api_tools import APIEndpointGeneratorTool, SwaggerSetupTool
from llmcode.tools.node_tools import NpmInstallTool


def create_api_with_auth():
    """Create a REST API with authentication"""

    config = Config()
    config.working_directory = Path.cwd() / "my-api"

    # Set up tools
    tool_registry = ToolRegistry()
    tool_registry.register(CreateExpressAppTool(str(config.working_directory)))
    tool_registry.register(MongoDBSetupTool(str(config.working_directory)))
    tool_registry.register(JWTAuthSetupTool(str(config.working_directory)))
    tool_registry.register(RateLimitSetupTool(str(config.working_directory)))
    tool_registry.register(CORSSetupTool(str(config.working_directory)))
    tool_registry.register(APIEndpointGeneratorTool(str(config.working_directory)))
    tool_registry.register(SwaggerSetupTool(str(config.working_directory)))
    tool_registry.register(NpmInstallTool(str(config.working_directory)))

    client = LLMClient(config, tool_registry)

    print("Creating REST API with authentication...")
    print()

    message = """
    Create a secure REST API with the following:

    1. Express.js backend with TypeScript
    2. MongoDB database integration
    3. JWT authentication system (register, login, protected routes)
    4. Rate limiting middleware (100 requests per 15 minutes)
    5. CORS configuration for frontend access
    6. API endpoints for "Product" resource (name, description, price, stock)
    7. Swagger/OpenAPI documentation
    8. Install all dependencies

    Include proper error handling and validation.
    """

    for event in client.send_message(message):
        if event["type"] == "text":
            print(event["content"], end="", flush=True)
        elif event["type"] == "tool_use":
            print(f"\n\n🔧 {event['tool']}")
        elif event["type"] == "tool_result":
            print(f"✓ Done")

    print("\n\n✅ API created successfully!")
    print("\nTo start the API:")
    print("cd my-api")
    print("npm run dev")
    print("\nAPI Documentation: http://localhost:3000/api-docs")


if __name__ == "__main__":
    create_api_with_auth()
