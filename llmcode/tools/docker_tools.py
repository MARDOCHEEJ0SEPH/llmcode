"""Docker and containerization tools"""

import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, List
from .base import Tool, ToolResult, ToolStatus


class DockerfileGeneratorTool(Tool):
    """Tool for generating Dockerfiles"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "DockerfileGenerator"

    @property
    def description(self) -> str:
        return "Generates Dockerfile for applications (Node.js, Python, etc.)"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "app_type": {
                    "type": "string",
                    "enum": ["node", "python", "go", "java"],
                    "description": "Application type"
                },
                "framework": {
                    "type": "string",
                    "description": "Framework name (e.g., 'express', 'react', 'fastapi')"
                },
                "port": {
                    "type": "integer",
                    "description": "Application port"
                }
            },
            "required": ["app_type"]
        }

    def execute(self, app_type: str, framework: str = None,
                port: int = 3000) -> ToolResult:
        """Generate Dockerfile"""
        try:
            project_path = Path(self.working_directory)

            if app_type == "node":
                dockerfile = f'''FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Build if needed (for TypeScript/React/etc)
{"RUN npm run build" if framework in ["react", "next", "vue"] else "# No build step"}

# Expose port
EXPOSE {port}

# Start application
CMD ["npm", "start"]
'''

            elif app_type == "python":
                dockerfile = f'''FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE {port}

# Start application
CMD ["{"uvicorn" if framework == "fastapi" else "python"}", "{"main:app --host 0.0.0.0" if framework == "fastapi" else "app.py"}"]
'''

            elif app_type == "go":
                dockerfile = f'''FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build application
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Final stage
FROM alpine:latest

WORKDIR /app

COPY --from=builder /app/main .

EXPOSE {port}

CMD ["./main"]
'''

            elif app_type == "java":
                dockerfile = f'''FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copy pom.xml
COPY pom.xml .
RUN mvn dependency:go-offline

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests

# Final stage
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY --from=builder /app/target/*.jar app.jar

EXPOSE {port}

CMD ["java", "-jar", "app.jar"]
'''

            # Write Dockerfile
            dockerfile_path = project_path / "Dockerfile"
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile)

            # Create .dockerignore
            dockerignore = '''node_modules
npm-debug.log
.env
.env.local
.git
.gitignore
README.md
.DS_Store
dist
build
.vscode
.idea
__pycache__
*.pyc
*.log
coverage
.pytest_cache
'''

            dockerignore_path = project_path / ".dockerignore"
            with open(dockerignore_path, 'w') as f:
                f.write(dockerignore)

            output = f"Dockerfile generated for {app_type} application!\n"
            output += f"- Created Dockerfile\n"
            output += f"- Created .dockerignore\n"
            output += f"\nBuild: docker build -t myapp .\n"
            output += f"Run: docker run -p {port}:{port} myapp"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"app_type": app_type, "port": port}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error generating Dockerfile: {str(e)}"
            )


class DockerComposeTool(Tool):
    """Tool for generating docker-compose.yml"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "DockerCompose"

    @property
    def description(self) -> str:
        return "Generates docker-compose.yml for multi-service applications"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "services": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["app", "postgres", "mongodb", "redis", "nginx"]
                    },
                    "description": "Services to include"
                },
                "app_port": {
                    "type": "integer",
                    "description": "Application port"
                }
            },
            "required": ["services"]
        }

    def execute(self, services: List[str], app_port: int = 3000) -> ToolResult:
        """Generate docker-compose.yml"""
        try:
            project_path = Path(self.working_directory)

            compose = {
                "version": "3.8",
                "services": {}
            }

            if "app" in services:
                compose["services"]["app"] = {
                    "build": ".",
                    "ports": [f"{app_port}:{app_port}"],
                    "environment": [
                        "NODE_ENV=production" if app_port == 3000 else "ENV=production"
                    ],
                    "depends_on": []
                }

                # Add database to depends_on
                if "postgres" in services:
                    compose["services"]["app"]["depends_on"].append("postgres")
                if "mongodb" in services:
                    compose["services"]["app"]["depends_on"].append("mongodb")
                if "redis" in services:
                    compose["services"]["app"]["depends_on"].append("redis")

            if "postgres" in services:
                compose["services"]["postgres"] = {
                    "image": "postgres:15-alpine",
                    "environment": [
                        "POSTGRES_USER=postgres",
                        "POSTGRES_PASSWORD=postgres",
                        "POSTGRES_DB=myapp"
                    ],
                    "ports": ["5432:5432"],
                    "volumes": ["postgres_data:/var/lib/postgresql/data"]
                }

            if "mongodb" in services:
                compose["services"]["mongodb"] = {
                    "image": "mongo:7-jammy",
                    "environment": [
                        "MONGO_INITDB_ROOT_USERNAME=admin",
                        "MONGO_INITDB_ROOT_PASSWORD=admin"
                    ],
                    "ports": ["27017:27017"],
                    "volumes": ["mongodb_data:/data/db"]
                }

            if "redis" in services:
                compose["services"]["redis"] = {
                    "image": "redis:7-alpine",
                    "ports": ["6379:6379"],
                    "volumes": ["redis_data:/data"]
                }

            if "nginx" in services:
                compose["services"]["nginx"] = {
                    "image": "nginx:alpine",
                    "ports": ["80:80"],
                    "volumes": ["./nginx.conf:/etc/nginx/nginx.conf:ro"],
                    "depends_on": ["app"]
                }

            # Add volumes section
            volumes = {}
            if "postgres" in services:
                volumes["postgres_data"] = {}
            if "mongodb" in services:
                volumes["mongodb_data"] = {}
            if "redis" in services:
                volumes["redis_data"] = {}

            if volumes:
                compose["volumes"] = volumes

            # Write docker-compose.yml
            import yaml
            compose_path = project_path / "docker-compose.yml"

            # Manual YAML formatting for better readability
            compose_yaml = "version: '3.8'\n\nservices:\n"

            for service_name, service_config in compose["services"].items():
                compose_yaml += f"  {service_name}:\n"
                for key, value in service_config.items():
                    if isinstance(value, list):
                        compose_yaml += f"    {key}:\n"
                        for item in value:
                            compose_yaml += f"      - {item}\n"
                    elif isinstance(value, dict):
                        compose_yaml += f"    {key}:\n"
                        for k, v in value.items():
                            compose_yaml += f"      {k}: {v}\n"
                    else:
                        compose_yaml += f"    {key}: {value}\n"
                compose_yaml += "\n"

            if volumes:
                compose_yaml += "volumes:\n"
                for volume_name in volumes.keys():
                    compose_yaml += f"  {volume_name}:\n"

            with open(compose_path, 'w') as f:
                f.write(compose_yaml)

            # Create nginx.conf if nginx is included
            if "nginx" in services:
                nginx_conf = f'''events {{
  worker_connections 1024;
}}

http {{
  upstream app {{
    server app:{app_port};
  }}

  server {{
    listen 80;

    location / {{
      proxy_pass http://app;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
  }}
}}
'''
                with open(project_path / "nginx.conf", 'w') as f:
                    f.write(nginx_conf)

            output = "docker-compose.yml generated!\n"
            output += f"Services: {', '.join(services)}\n"
            output += "\nStart all services: docker-compose up -d\n"
            output += "Stop all services: docker-compose down\n"
            output += "View logs: docker-compose logs -f"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"services": services}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error generating docker-compose.yml: {str(e)}"
            )


class DockerCommandTool(Tool):
    """Tool for running Docker commands"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory

    @property
    def name(self) -> str:
        return "DockerCommand"

    @property
    def description(self) -> str:
        return "Execute Docker commands (build, run, ps, logs, etc.)"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Docker command to execute"
                },
                "compose": {
                    "type": "boolean",
                    "description": "Use docker-compose instead of docker"
                }
            },
            "required": ["command"]
        }

    def execute(self, command: str, compose: bool = False) -> ToolResult:
        """Execute Docker command"""
        try:
            prefix = "docker-compose" if compose else "docker"
            full_command = f"{prefix} {command}"

            result = subprocess.run(
                full_command,
                shell=True,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=120
            )

            output = result.stdout
            if result.stderr:
                output += f"\n{result.stderr}"

            status = ToolStatus.SUCCESS if result.returncode == 0 else ToolStatus.WARNING

            return ToolResult(
                status=status,
                output=output or "Command completed",
                metadata={"command": full_command, "return_code": result.returncode}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error executing Docker command: {str(e)}"
            )
