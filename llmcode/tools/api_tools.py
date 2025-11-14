"""API development and testing tools"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, List
from .base import Tool, ToolResult, ToolStatus


class APIEndpointGeneratorTool(Tool):
    """Tool for generating REST API endpoints"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "APIEndpointGenerator"

    @property
    def description(self) -> str:
        return "Generates REST API CRUD endpoints for a resource"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "resource": {
                    "type": "string",
                    "description": "Resource name (e.g., 'user', 'post', 'product')"
                },
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi", "flask"],
                    "description": "Web framework"
                },
                "language": {
                    "type": "string",
                    "enum": ["javascript", "typescript", "python"],
                    "description": "Programming language"
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Resource fields (e.g., ['name', 'email', 'age'])"
                }
            },
            "required": ["resource", "framework", "language"]
        }

    def execute(self, resource: str, framework: str, language: str,
                fields: List[str] = None) -> ToolResult:
        """Generate API endpoints"""
        try:
            project_path = Path(self.working_directory)
            resource_lower = resource.lower()
            resource_cap = resource.capitalize()

            if not fields:
                fields = ["name", "description"]

            if framework == "express":
                is_ts = language == "typescript"
                ext = "ts" if is_ts else "js"

                routes_code = f'''{"import { Router, Request, Response } from 'express';" if is_ts else "const express = require('express');"}
{"import { getDB } from './db';" if is_ts else "const { getDB } = require('./db');"}

const router = {"express.Router()" if not is_ts else "Router()"};

// GET all {resource_lower}s
router.get('/', async (req{"" if is_ts else ""}, res{"" if is_ts else ""}) => {"{"}
  try {"{"}
    const db = getDB();
    const {resource_lower}s = await db.collection('{resource_lower}s').find({"{"}{"}"}).toArray();
    res.json({resource_lower}s);
  {"}"} catch (error) {"{"}
    res.status(500).json({"{"} error: 'Failed to fetch {resource_lower}s' {"}"});
  {"}"}
{"}"});

// GET single {resource_lower} by ID
router.get('/:id', async (req{"" if is_ts else ""}, res{"" if is_ts else ""}) => {"{"}
  try {"{"}
    const db = getDB();
    const {resource_lower} = await db.collection('{resource_lower}s').findOne({"{"} _id: req.params.id {"}"});

    if (!{resource_lower}) {"{"}
      return res.status(404).json({"{"} error: '{resource_cap} not found' {"}"});
    {"}"}

    res.json({resource_lower});
  {"}"} catch (error) {"{"}
    res.status(500).json({"{"} error: 'Failed to fetch {resource_lower}' {"}"});
  {"}"}
{"}"});

// POST create new {resource_lower}
router.post('/', async (req{"" if is_ts else ""}, res{"" if is_ts else ""}) => {"{"}
  try {"{"}
    const db = getDB();
    const new{resource_cap} = {"{"}
      {", ".join([f"      {field}: req.body.{field}" for field in fields])},
      createdAt: new Date(),
      updatedAt: new Date()
    {"}"};

    const result = await db.collection('{resource_lower}s').insertOne(new{resource_cap});
    res.status(201).json({"{"} id: result.insertedId, ...new{resource_cap} {"}"});
  {"}"} catch (error) {"{"}
    res.status(500).json({"{"} error: 'Failed to create {resource_lower}' {"}"});
  {"}"}
{"}"});

// PUT update {resource_lower}
router.put('/:id', async (req{"" if is_ts else ""}, res{"" if is_ts else ""}) => {"{"}
  try {"{"}
    const db = getDB();
    const update = {"{"}
      {", ".join([f"      {field}: req.body.{field}" for field in fields])},
      updatedAt: new Date()
    {"}"};

    const result = await db.collection('{resource_lower}s').updateOne(
      {"{"} _id: req.params.id {"}"},
      {"{"} $set: update {"}"}
    );

    if (result.matchedCount === 0) {"{"}
      return res.status(404).json({"{"} error: '{resource_cap} not found' {"}"});
    {"}"}

    res.json({"{"} message: '{resource_cap} updated successfully' {"}"});
  {"}"} catch (error) {"{"}
    res.status(500).json({"{"} error: 'Failed to update {resource_lower}' {"}"});
  {"}"}
{"}"});

// DELETE {resource_lower}
router.delete('/:id', async (req{"" if is_ts else ""}, res{"" if is_ts else ""}) => {"{"}
  try {"{"}
    const db = getDB();
    const result = await db.collection('{resource_lower}s').deleteOne({"{"} _id: req.params.id {"}"});

    if (result.deletedCount === 0) {"{"}
      return res.status(404).json({"{"} error: '{resource_cap} not found' {"}"});
    {"}"}

    res.json({"{"} message: '{resource_cap} deleted successfully' {"}"});
  {"}"} catch (error) {"{"}
    res.status(500).json({"{"} error: 'Failed to delete {resource_lower}' {"}"});
  {"}"}
{"}"});

{"export default router;" if is_ts else "module.exports = router;"}
'''

                routes_dir = project_path / "routes"
                routes_dir.mkdir(exist_ok=True)

                with open(routes_dir / f"{resource_lower}.{ext}", 'w') as f:
                    f.write(routes_code)

                output = f"API endpoints generated for {resource}!\n"
                output += f"- Created routes/{resource_lower}.{ext}\n"
                output += f"- Endpoints: GET, POST, PUT, DELETE\n"
                output += f"\nAdd to your app:\n"
                output += f"app.use('/api/{resource_lower}s', {resource_lower}Router);"

            elif framework == "fastapi":
                routes_code = f'''"""API endpoints for {resource_cap}"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from db import get_collection

router = APIRouter(prefix="/{resource_lower}s", tags=["{resource_lower}s"])

# Pydantic models
class {resource_cap}Base(BaseModel):
    {chr(10).join([f"    {field}: str" for field in fields])}

class {resource_cap}Create({resource_cap}Base):
    pass

class {resource_cap}Update({resource_cap}Base):
    pass

class {resource_cap}Response({resource_cap}Base):
    id: str
    created_at: datetime
    updated_at: datetime

# GET all {resource_lower}s
@router.get("/", response_model=List[{resource_cap}Response])
async def get_{resource_lower}s():
    collection = get_collection("{resource_lower}s")
    {resource_lower}s = await collection.find({"{"}{"}"}).to_list(100)
    return [{resource_lower}s]

# GET single {resource_lower}
@router.get("/{{"{"}id{"}"}}",response_model={resource_cap}Response)
async def get_{resource_lower}(id: str):
    collection = get_collection("{resource_lower}s")
    {resource_lower} = await collection.find_one({"{"}\"_id\": id{"}"})

    if not {resource_lower}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{resource_cap} not found"
        )

    return {resource_lower}

# POST create {resource_lower}
@router.post("/", response_model={resource_cap}Response, status_code=status.HTTP_201_CREATED)
async def create_{resource_lower}(data: {resource_cap}Create):
    collection = get_collection("{resource_lower}s")

    new_{resource_lower} = {"{"}
        **data.dict(),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    {"}"}

    result = await collection.insert_one(new_{resource_lower})
    new_{resource_lower}["id"] = str(result.inserted_id)

    return new_{resource_lower}

# PUT update {resource_lower}
@router.put("/{{"{"}id{"}"}}",response_model={resource_cap}Response)
async def update_{resource_lower}(id: str, data: {resource_cap}Update):
    collection = get_collection("{resource_lower}s")

    update_data = {"{"}
        **data.dict(),
        "updated_at": datetime.utcnow()
    {"}"}

    result = await collection.update_one(
        {"{"}\"_id\": id{"}"},
        {"{"}\"$set\": update_data{"}"}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{resource_cap} not found"
        )

    {resource_lower} = await collection.find_one({"{"}\"_id\": id{"}"})
    return {resource_lower}

# DELETE {resource_lower}
@router.delete("/{{"{"}id{"}"}}")
async def delete_{resource_lower}(id: str):
    collection = get_collection("{resource_lower}s")
    result = await collection.delete_one({"{"}\"_id\": id{"}"})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="{resource_cap} not found"
        )

    return {"{"}\"message\": \"{resource_cap} deleted successfully\"{"}"}
'''

                routes_dir = project_path / "routes"
                routes_dir.mkdir(exist_ok=True)

                with open(routes_dir / f"{resource_lower}.py", 'w') as f:
                    f.write(routes_code)

                output = f"API endpoints generated for {resource}!\n"
                output += f"- Created routes/{resource_lower}.py\n"
                output += f"- Endpoints: GET, POST, PUT, DELETE\n"
                output += f"\nAdd to your app:\n"
                output += f"from routes.{resource_lower} import router as {resource_lower}_router\n"
                output += f"app.include_router({resource_lower}_router)"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"resource": resource, "framework": framework}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error generating API endpoints: {str(e)}"
            )


class SwaggerSetupTool(Tool):
    """Tool for setting up API documentation with Swagger/OpenAPI"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "SwaggerSetup"

    @property
    def description(self) -> str:
        return "Sets up Swagger/OpenAPI documentation for REST APIs"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi"],
                    "description": "Web framework"
                },
                "title": {
                    "type": "string",
                    "description": "API title"
                },
                "version": {
                    "type": "string",
                    "description": "API version"
                }
            },
            "required": ["framework"]
        }

    def execute(self, framework: str, title: str = "My API",
                version: str = "1.0.0") -> ToolResult:
        """Set up Swagger documentation"""
        try:
            project_path = Path(self.working_directory)

            if framework == "express":
                swagger_code = f'''const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {"{"}
  definition: {"{"}
    openapi: '3.0.0',
    info: {"{"}
      title: '{title}',
      version: '{version}',
      description: 'API documentation',
    {"}"},
    servers: [
      {"{"}
        url: process.env.API_URL || 'http://localhost:3000',
        description: 'Development server',
      {"}"},
    ],
  {"}"},
  apis: ['./routes/*.js', './routes/*.ts'],
{"}"};

const specs = swaggerJsdoc(options);

function setupSwagger(app) {"{"}
  app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));
  console.log('Swagger docs available at /api-docs');
{"}"}

module.exports = setupSwagger;
'''

                with open(project_path / "swagger.js", 'w') as f:
                    f.write(swagger_code)

                # Update package.json
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)

                    if "dependencies" not in pkg_data:
                        pkg_data["dependencies"] = {}

                    pkg_data["dependencies"]["swagger-jsdoc"] = "^6.2.0"
                    pkg_data["dependencies"]["swagger-ui-express"] = "^5.0.0"

                    with open(pkg_file, 'w') as f:
                        json.dump(pkg_data, f, indent=2)

                output = "Swagger documentation setup complete!\n"
                output += "- Created swagger.js\n"
                output += "- Updated package.json\n"
                output += "\nUsage:\n"
                output += "const setupSwagger = require('./swagger');\n"
                output += "setupSwagger(app);\n"
                output += "\nDocs available at: http://localhost:3000/api-docs"

            elif framework == "fastapi":
                output = "FastAPI includes Swagger docs by default!\n"
                output += "\nDocs available at:\n"
                output += "- Swagger UI: http://localhost:8000/docs\n"
                output += "- ReDoc: http://localhost:8000/redoc\n"
                output += "\nTo customize, update your FastAPI app:\n"
                output += f"app = FastAPI(title='{title}', version='{version}')"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"framework": framework}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up Swagger: {str(e)}"
            )
