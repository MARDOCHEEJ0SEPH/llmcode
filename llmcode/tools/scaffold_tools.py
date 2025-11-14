"""Project scaffolding and template tools"""

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional
from .base import Tool, ToolResult, ToolStatus


class CreateReactAppTool(Tool):
    """Tool for creating React applications"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "CreateReactApp"

    @property
    def description(self) -> str:
        return "Creates a new React application using create-react-app or Vite"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Application name"
                },
                "template": {
                    "type": "string",
                    "enum": ["vite", "cra", "next"],
                    "description": "Template to use (vite, cra, or next)"
                },
                "typescript": {
                    "type": "boolean",
                    "description": "Use TypeScript"
                }
            },
            "required": ["name"]
        }

    def execute(self, name: str, template: str = "vite",
                typescript: bool = False) -> ToolResult:
        """Create React app"""
        try:
            if template == "vite":
                cmd = ["npm", "create", "vite@latest", name, "--"]
                if typescript:
                    cmd.extend(["--template", "react-ts"])
                else:
                    cmd.extend(["--template", "react"])

            elif template == "next":
                cmd = ["npx", "create-next-app@latest", name]
                if typescript:
                    cmd.append("--typescript")
                cmd.append("--use-npm")

            else:  # cra
                cmd = ["npx", "create-react-app", name]
                if typescript:
                    cmd.append("--template typescript")

            result = subprocess.run(
                cmd,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output=f"React app '{name}' created successfully with {template}",
                    metadata={"name": name, "template": template, "typescript": typescript}
                )
            else:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output=result.stdout,
                    error=result.stderr
                )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error creating React app: {str(e)}"
            )


class CreateVueAppTool(Tool):
    """Tool for creating Vue applications"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "CreateVueApp"

    @property
    def description(self) -> str:
        return "Creates a new Vue.js application"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Application name"
                },
                "typescript": {
                    "type": "boolean",
                    "description": "Use TypeScript"
                }
            },
            "required": ["name"]
        }

    def execute(self, name: str, typescript: bool = False) -> ToolResult:
        """Create Vue app"""
        try:
            cmd = ["npm", "create", "vue@latest", name]

            result = subprocess.run(
                cmd,
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                return ToolResult(
                    status=ToolStatus.SUCCESS,
                    output=f"Vue app '{name}' created successfully",
                    metadata={"name": name, "typescript": typescript}
                )
            else:
                return ToolResult(
                    status=ToolStatus.ERROR,
                    output=result.stdout,
                    error=result.stderr
                )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error creating Vue app: {str(e)}"
            )


class CreateExpressAppTool(Tool):
    """Tool for creating Express.js backend"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "CreateExpressApp"

    @property
    def description(self) -> str:
        return "Creates a new Express.js backend application"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Application name"
                },
                "typescript": {
                    "type": "boolean",
                    "description": "Use TypeScript"
                }
            },
            "required": ["name"]
        }

    def execute(self, name: str, typescript: bool = False) -> ToolResult:
        """Create Express app"""
        try:
            app_path = Path(self.working_directory) / name
            app_path.mkdir(parents=True, exist_ok=True)

            # Create package.json
            package_json = {
                "name": name,
                "version": "1.0.0",
                "description": "Express.js backend",
                "main": "index.js" if not typescript else "dist/index.js",
                "scripts": {
                    "start": "node index.js" if not typescript else "node dist/index.js",
                    "dev": "nodemon index.js" if not typescript else "nodemon src/index.ts"
                },
                "dependencies": {
                    "express": "^4.18.0",
                    "cors": "^2.8.5",
                    "dotenv": "^16.0.0"
                },
                "devDependencies": {
                    "nodemon": "^3.0.0"
                }
            }

            if typescript:
                package_json["scripts"]["build"] = "tsc"
                package_json["devDependencies"]["typescript"] = "^5.0.0"
                package_json["devDependencies"]["@types/express"] = "^4.17.0"
                package_json["devDependencies"]["@types/node"] = "^20.0.0"

            import json
            with open(app_path / "package.json", 'w') as f:
                json.dump(package_json, f, indent=2)

            # Create basic Express server
            if typescript:
                src_path = app_path / "src"
                src_path.mkdir(exist_ok=True)

                server_code = '''import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Express!' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
'''
                with open(src_path / "index.ts", 'w') as f:
                    f.write(server_code)

                # Create tsconfig.json
                tsconfig = {
                    "compilerOptions": {
                        "target": "ES2020",
                        "module": "commonjs",
                        "outDir": "./dist",
                        "rootDir": "./src",
                        "strict": True,
                        "esModuleInterop": True
                    }
                }
                with open(app_path / "tsconfig.json", 'w') as f:
                    json.dump(tsconfig, f, indent=2)
            else:
                server_code = '''const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Hello from Express!' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
'''
                with open(app_path / "index.js", 'w') as f:
                    f.write(server_code)

            # Create .env
            with open(app_path / ".env", 'w') as f:
                f.write("PORT=3000\n")

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"Express app '{name}' created successfully at {app_path}",
                metadata={"name": name, "path": str(app_path)}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error creating Express app: {str(e)}"
            )


class CreateFullStackAppTool(Tool):
    """Tool for creating full-stack applications"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "CreateFullStackApp"

    @property
    def description(self) -> str:
        return "Creates a complete full-stack application with frontend and backend"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Application name"
                },
                "frontend": {
                    "type": "string",
                    "enum": ["react", "vue", "svelte"],
                    "description": "Frontend framework"
                },
                "backend": {
                    "type": "string",
                    "enum": ["express", "fastapi"],
                    "description": "Backend framework"
                },
                "database": {
                    "type": "string",
                    "enum": ["postgresql", "mongodb", "sqlite"],
                    "description": "Database type"
                },
                "typescript": {
                    "type": "boolean",
                    "description": "Use TypeScript"
                }
            },
            "required": ["name"]
        }

    def execute(self, name: str, frontend: str = "react",
                backend: str = "express", database: str = "postgresql",
                typescript: bool = True) -> ToolResult:
        """Create full-stack app"""
        try:
            app_path = Path(self.working_directory) / name
            app_path.mkdir(parents=True, exist_ok=True)

            # Create root package.json
            root_package = {
                "name": name,
                "version": "1.0.0",
                "description": f"Full-stack application with {frontend} and {backend}",
                "scripts": {
                    "install:all": "cd frontend && npm install && cd ../backend && npm install",
                    "dev": "concurrently \"npm run dev:frontend\" \"npm run dev:backend\"",
                    "dev:frontend": "cd frontend && npm run dev",
                    "dev:backend": "cd backend && npm run dev"
                },
                "devDependencies": {
                    "concurrently": "^8.0.0"
                }
            }

            import json
            with open(app_path / "package.json", 'w') as f:
                json.dump(root_package, f, indent=2)

            # Create README
            readme = f"""# {name}

Full-stack application built with:
- Frontend: {frontend.capitalize()}
- Backend: {backend.capitalize()}
- Database: {database.capitalize()}
- TypeScript: {'Yes' if typescript else 'No'}

## Getting Started

### Install dependencies
```bash
npm run install:all
```

### Run development servers
```bash
npm run dev
```

Frontend: http://localhost:5173
Backend: http://localhost:3000

## Project Structure

```
{name}/
├── frontend/     # {frontend.capitalize()} application
├── backend/      # {backend.capitalize()} API
└── README.md
```
"""
            with open(app_path / "README.md", 'w') as f:
                f.write(readme)

            # Create .gitignore
            gitignore = """node_modules/
dist/
.env
.env.local
*.log
.DS_Store
"""
            with open(app_path / ".gitignore", 'w') as f:
                f.write(gitignore)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=f"Full-stack app '{name}' structure created at {app_path}\n"
                       f"Use CreateReactApp/CreateVueApp for frontend and CreateExpressApp for backend",
                metadata={
                    "name": name,
                    "frontend": frontend,
                    "backend": backend,
                    "database": database
                }
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error creating full-stack app: {str(e)}"
            )
