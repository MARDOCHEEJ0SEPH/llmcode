"""
Example: Docker Deployment Setup

This example demonstrates how to set up Docker containerization
for an application with multiple services.
"""

from pathlib import Path
from llmcode.config import Config
from llmcode.llm_client import LLMClient
from llmcode.tools.base import ToolRegistry
from llmcode.tools.docker_tools import DockerfileGeneratorTool, DockerComposeTool, DockerCommandTool


def setup_docker_deployment():
    """Set up Docker deployment for an application"""

    config = Config()
    config.working_directory = Path.cwd()

    tool_registry = ToolRegistry()
    tool_registry.register(DockerfileGeneratorTool(str(config.working_directory)))
    tool_registry.register(DockerComposeTool(str(config.working_directory)))
    tool_registry.register(DockerCommandTool(str(config.working_directory)))

    client = LLMClient(config, tool_registry)

    print("Setting up Docker deployment...")
    print()

    message = """
    Set up Docker deployment for this application:

    1. Generate a Dockerfile for a Node.js Express application on port 3000
    2. Create docker-compose.yml with:
       - Application service
       - PostgreSQL database
       - Redis cache
       - Nginx reverse proxy
    3. Build the Docker image
    4. Show how to start all services

    Make it production-ready with proper configuration.
    """

    for event in client.send_message(message):
        if event["type"] == "text":
            print(event["content"], end="", flush=True)
        elif event["type"] == "tool_use":
            print(f"\n\n🔧 {event['tool']}")
        elif event["type"] == "tool_result":
            print(f"✓ Completed")

    print("\n\n✅ Docker setup complete!")
    print("\nStart services: docker-compose up -d")
    print("View logs: docker-compose logs -f")
    print("Stop services: docker-compose down")


if __name__ == "__main__":
    setup_docker_deployment()
