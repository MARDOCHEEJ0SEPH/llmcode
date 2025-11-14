"""Database integration tools for MongoDB, PostgreSQL, Redis, etc."""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, List
from .base import Tool, ToolResult, ToolStatus


class MongoDBSetupTool(Tool):
    """Tool for setting up MongoDB in a project"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "MongoDBSetup"

    @property
    def description(self) -> str:
        return "Sets up MongoDB integration with connection code and configuration"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["javascript", "typescript", "python"],
                    "description": "Programming language"
                },
                "connection_string": {
                    "type": "string",
                    "description": "MongoDB connection string (optional, will use env var)"
                }
            },
            "required": ["language"]
        }

    def execute(self, language: str, connection_string: str = None) -> ToolResult:
        """Set up MongoDB integration"""
        try:
            project_path = Path(self.working_directory)

            if language in ["javascript", "typescript"]:
                # Create MongoDB connection file
                is_ts = language == "typescript"
                ext = "ts" if is_ts else "js"

                db_code = f'''{"import { MongoClient } from 'mongodb';" if is_ts else "const { MongoClient } = require('mongodb');"}
{"import dotenv from 'dotenv';" if is_ts else "const dotenv = require('dotenv');"}
dotenv.config();

const connectionString = process.env.MONGODB_URI || 'mongodb://localhost:27017';
const client = new MongoClient(connectionString);

let db{"" if is_ts else ""};

export async function connectDB() {"{"}
  try {"{"}
    await client.connect();
    db = client.db(process.env.DB_NAME || 'myapp');
    console.log('Connected to MongoDB');
    return db;
  {"}"} catch (error) {"{"}
    console.error('MongoDB connection error:', error);
    throw error;
  {"}"}
{"}"}

export function getDB() {"{"}
  if (!db) {"{"}
    throw new Error('Database not connected. Call connectDB first.');
  {"}"}
  return db;
{"}"}

export async function closeDB() {"{"}
  await client.close();
{"}"}
'''

                db_file = project_path / f"db.{ext}"
                with open(db_file, 'w') as f:
                    f.write(db_code)

                # Update or create .env
                env_file = project_path / ".env"
                env_content = ""
                if env_file.exists():
                    env_content = env_file.read_text()

                if "MONGODB_URI" not in env_content:
                    env_content += f"\nMONGODB_URI={connection_string or 'mongodb://localhost:27017'}\n"
                    env_content += "DB_NAME=myapp\n"

                with open(env_file, 'w') as f:
                    f.write(env_content)

                # Update package.json to add mongodb
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)

                    if "dependencies" not in pkg_data:
                        pkg_data["dependencies"] = {}

                    pkg_data["dependencies"]["mongodb"] = "^6.3.0"

                    with open(pkg_file, 'w') as f:
                        json.dump(pkg_data, f, indent=2)

                output = f"MongoDB setup complete!\n"
                output += f"- Created db.{ext} with connection code\n"
                output += f"- Updated .env with MONGODB_URI\n"
                output += f"- Added mongodb to package.json\n"
                output += f"\nRun: npm install"

            elif language == "python":
                # Create MongoDB connection file
                db_code = '''"""MongoDB database connection"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(connection_string)
db = client[os.getenv("DB_NAME", "myapp")]

def get_db():
    """Get database instance"""
    return db

def get_collection(name):
    """Get collection by name"""
    return db[name]
'''

                db_file = project_path / "db.py"
                with open(db_file, 'w') as f:
                    f.write(db_code)

                # Update requirements.txt
                req_file = project_path / "requirements.txt"
                requirements = []
                if req_file.exists():
                    requirements = req_file.read_text().splitlines()

                if "pymongo" not in str(requirements):
                    requirements.append("pymongo>=4.6.0")
                if "python-dotenv" not in str(requirements):
                    requirements.append("python-dotenv>=1.0.0")

                with open(req_file, 'w') as f:
                    f.write("\n".join(requirements))

                # Update .env
                env_file = project_path / ".env"
                env_content = ""
                if env_file.exists():
                    env_content = env_file.read_text()

                if "MONGODB_URI" not in env_content:
                    env_content += f"\nMONGODB_URI={connection_string or 'mongodb://localhost:27017'}\n"
                    env_content += "DB_NAME=myapp\n"

                with open(env_file, 'w') as f:
                    f.write(env_content)

                output = f"MongoDB setup complete!\n"
                output += f"- Created db.py with connection code\n"
                output += f"- Updated .env with MONGODB_URI\n"
                output += f"- Added pymongo to requirements.txt\n"
                output += f"\nRun: pip install -r requirements.txt"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"language": language}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up MongoDB: {str(e)}"
            )


class RedisSetupTool(Tool):
    """Tool for setting up Redis in a project"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "RedisSetup"

    @property
    def description(self) -> str:
        return "Sets up Redis caching/session store with connection code"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["javascript", "typescript", "python"],
                    "description": "Programming language"
                },
                "use_case": {
                    "type": "string",
                    "enum": ["cache", "session", "queue"],
                    "description": "Primary use case"
                }
            },
            "required": ["language"]
        }

    def execute(self, language: str, use_case: str = "cache") -> ToolResult:
        """Set up Redis integration"""
        try:
            project_path = Path(self.working_directory)

            if language in ["javascript", "typescript"]:
                is_ts = language == "typescript"
                ext = "ts" if is_ts else "js"

                redis_code = f'''{"import { createClient } from 'redis';" if is_ts else "const { createClient } = require('redis');"}
{"import dotenv from 'dotenv';" if is_ts else "const dotenv = require('dotenv');"}
dotenv.config();

const redisClient = createClient({"{"}
  url: process.env.REDIS_URL || 'redis://localhost:6379'
{"}"});

redisClient.on('error', (err{"" if is_ts else ""}) => {"{"}
  console.error('Redis Client Error', err);
{"}"});

export async function connectRedis() {"{"}
  if (!redisClient.isOpen) {"{"}
    await redisClient.connect();
    console.log('Connected to Redis');
  {"}"}
  return redisClient;
{"}"}

export function getRedis() {"{"}
  return redisClient;
{"}"}

// Helper functions for common operations
export async function setCache(key{"" if is_ts else ""}, value{"" if is_ts else ""}, ttl = 3600) {"{"}
  await redisClient.setEx(key, ttl, JSON.stringify(value));
{"}"}

export async function getCache(key{"" if is_ts else ""}) {"{"}
  const value = await redisClient.get(key);
  return value ? JSON.parse(value) : null;
{"}"}

export async function deleteCache(key{"" if is_ts else ""}) {"{"}
  await redisClient.del(key);
{"}"}

export async function closeRedis() {"{"}
  await redisClient.quit();
{"}"}
'''

                redis_file = project_path / f"redis.{ext}"
                with open(redis_file, 'w') as f:
                    f.write(redis_code)

                # Update package.json
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)

                    if "dependencies" not in pkg_data:
                        pkg_data["dependencies"] = {}

                    pkg_data["dependencies"]["redis"] = "^4.6.0"

                    with open(pkg_file, 'w') as f:
                        json.dump(pkg_data, f, indent=2)

                # Update .env
                env_file = project_path / ".env"
                env_content = ""
                if env_file.exists():
                    env_content = env_file.read_text()

                if "REDIS_URL" not in env_content:
                    env_content += "\nREDIS_URL=redis://localhost:6379\n"

                with open(env_file, 'w') as f:
                    f.write(env_content)

                output = f"Redis setup complete!\n"
                output += f"- Created redis.{ext} with connection code\n"
                output += f"- Added helper functions for {use_case}\n"
                output += f"- Updated .env with REDIS_URL\n"
                output += f"\nRun: npm install"

            elif language == "python":
                redis_code = '''"""Redis connection and caching utilities"""

import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.from_url(redis_url, decode_responses=True)

def get_redis():
    """Get Redis client"""
    return redis_client

def set_cache(key, value, ttl=3600):
    """Set cache with TTL"""
    redis_client.setex(key, ttl, json.dumps(value))

def get_cache(key):
    """Get cached value"""
    value = redis_client.get(key)
    return json.loads(value) if value else None

def delete_cache(key):
    """Delete cache key"""
    redis_client.delete(key)

def clear_pattern(pattern):
    """Clear all keys matching pattern"""
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)
'''

                redis_file = project_path / "redis_client.py"
                with open(redis_file, 'w') as f:
                    f.write(redis_code)

                # Update requirements.txt
                req_file = project_path / "requirements.txt"
                requirements = []
                if req_file.exists():
                    requirements = req_file.read_text().splitlines()

                if "redis" not in str(requirements):
                    requirements.append("redis>=5.0.0")

                with open(req_file, 'w') as f:
                    f.write("\n".join(requirements))

                # Update .env
                env_file = project_path / ".env"
                env_content = ""
                if env_file.exists():
                    env_content = env_file.read_text()

                if "REDIS_URL" not in env_content:
                    env_content += "\nREDIS_URL=redis://localhost:6379\n"

                with open(env_file, 'w') as f:
                    f.write(env_content)

                output = f"Redis setup complete!\n"
                output += f"- Created redis_client.py with connection code\n"
                output += f"- Added helper functions for {use_case}\n"
                output += f"- Updated requirements.txt\n"
                output += f"\nRun: pip install -r requirements.txt"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"language": language, "use_case": use_case}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up Redis: {str(e)}"
            )


class PostgreSQLSetupTool(Tool):
    """Tool for setting up PostgreSQL in a project"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "PostgreSQLSetup"

    @property
    def description(self) -> str:
        return "Sets up PostgreSQL database with ORM and connection code"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "language": {
                    "type": "string",
                    "enum": ["javascript", "typescript", "python"],
                    "description": "Programming language"
                },
                "orm": {
                    "type": "string",
                    "enum": ["prisma", "sequelize", "sqlalchemy", "none"],
                    "description": "ORM to use"
                }
            },
            "required": ["language"]
        }

    def execute(self, language: str, orm: str = "prisma") -> ToolResult:
        """Set up PostgreSQL integration"""
        try:
            project_path = Path(self.working_directory)

            if language in ["javascript", "typescript"]:
                if orm == "prisma":
                    # Create Prisma schema
                    prisma_schema = '''generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Example model
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
'''

                    prisma_dir = project_path / "prisma"
                    prisma_dir.mkdir(exist_ok=True)

                    with open(prisma_dir / "schema.prisma", 'w') as f:
                        f.write(prisma_schema)

                    # Update package.json
                    pkg_file = project_path / "package.json"
                    if pkg_file.exists():
                        with open(pkg_file, 'r') as f:
                            pkg_data = json.load(f)

                        if "dependencies" not in pkg_data:
                            pkg_data["dependencies"] = {}
                        if "devDependencies" not in pkg_data:
                            pkg_data["devDependencies"] = {}

                        pkg_data["dependencies"]["@prisma/client"] = "^5.0.0"
                        pkg_data["devDependencies"]["prisma"] = "^5.0.0"

                        if "scripts" not in pkg_data:
                            pkg_data["scripts"] = {}

                        pkg_data["scripts"]["prisma:generate"] = "prisma generate"
                        pkg_data["scripts"]["prisma:migrate"] = "prisma migrate dev"

                        with open(pkg_file, 'w') as f:
                            json.dump(pkg_data, f, indent=2)

                    output = "PostgreSQL with Prisma setup complete!\n"
                    output += "- Created prisma/schema.prisma\n"
                    output += "- Added Prisma to package.json\n"
                    output += "\nNext steps:\n"
                    output += "1. Set DATABASE_URL in .env\n"
                    output += "2. Run: npm install\n"
                    output += "3. Run: npx prisma migrate dev\n"

                elif orm == "sequelize":
                    is_ts = language == "typescript"
                    ext = "ts" if is_ts else "js"

                    db_code = f'''{"import { Sequelize } from 'sequelize';" if is_ts else "const { Sequelize } = require('sequelize');"}
{"import dotenv from 'dotenv';" if is_ts else "const dotenv = require('dotenv');"}
dotenv.config();

const sequelize = new Sequelize(process.env.DATABASE_URL || '', {"{"}
  dialect: 'postgres',
  logging: process.env.NODE_ENV === 'development'
{"}"});

export async function connectDB() {"{"}
  try {"{"}
    await sequelize.authenticate();
    console.log('Connected to PostgreSQL');
    return sequelize;
  {"}"} catch (error) {"{"}
    console.error('PostgreSQL connection error:', error);
    throw error;
  {"}"}
{"}"}

export function getDB() {"{"}
  return sequelize;
{"}"}

export { "{"} Sequelize {"}"};
export default sequelize;
'''

                    with open(project_path / f"database.{ext}", 'w') as f:
                        f.write(db_code)

                    # Update package.json
                    pkg_file = project_path / "package.json"
                    if pkg_file.exists():
                        with open(pkg_file, 'r') as f:
                            pkg_data = json.load(f)

                        if "dependencies" not in pkg_data:
                            pkg_data["dependencies"] = {}

                        pkg_data["dependencies"]["sequelize"] = "^6.35.0"
                        pkg_data["dependencies"]["pg"] = "^8.11.0"
                        pkg_data["dependencies"]["pg-hstore"] = "^2.3.4"

                        with open(pkg_file, 'w') as f:
                            json.dump(pkg_data, f, indent=2)

                    output = "PostgreSQL with Sequelize setup complete!\n"
                    output += f"- Created database.{ext}\n"
                    output += "- Added Sequelize to package.json\n"

            elif language == "python":
                if orm == "sqlalchemy":
                    db_code = '''"""PostgreSQL database with SQLAlchemy"""

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/myapp")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Example model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
'''

                    with open(project_path / "database.py", 'w') as f:
                        f.write(db_code)

                    # Update requirements.txt
                    req_file = project_path / "requirements.txt"
                    requirements = []
                    if req_file.exists():
                        requirements = req_file.read_text().splitlines()

                    if "sqlalchemy" not in str(requirements):
                        requirements.append("sqlalchemy>=2.0.0")
                    if "psycopg2-binary" not in str(requirements):
                        requirements.append("psycopg2-binary>=2.9.0")

                    with open(req_file, 'w') as f:
                        f.write("\n".join(requirements))

                    output = "PostgreSQL with SQLAlchemy setup complete!\n"
                    output += "- Created database.py with models\n"
                    output += "- Updated requirements.txt\n"

            # Update .env
            env_file = project_path / ".env"
            env_content = ""
            if env_file.exists():
                env_content = env_file.read_text()

            if "DATABASE_URL" not in env_content:
                env_content += "\nDATABASE_URL=postgresql://user:password@localhost:5432/myapp\n"

            with open(env_file, 'w') as f:
                f.write(env_content)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"language": language, "orm": orm}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up PostgreSQL: {str(e)}"
            )
