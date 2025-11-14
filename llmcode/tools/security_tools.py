"""Security and authentication tools"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from .base import Tool, ToolResult, ToolStatus


class JWTAuthSetupTool(Tool):
    """Tool for setting up JWT authentication"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "JWTAuthSetup"

    @property
    def description(self) -> str:
        return "Sets up JWT authentication with token generation and verification"

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
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi", "flask"],
                    "description": "Web framework"
                }
            },
            "required": ["language", "framework"]
        }

    def execute(self, language: str, framework: str) -> ToolResult:
        """Set up JWT authentication"""
        try:
            project_path = Path(self.working_directory)

            if language in ["javascript", "typescript"]:
                is_ts = language == "typescript"
                ext = "ts" if is_ts else "js"

                auth_code = f'''{"import jwt from 'jsonwebtoken';" if is_ts else "const jwt = require('jsonwebtoken');"}
{"import { Request, Response, NextFunction } from 'express';" if is_ts else ""}
{"import dotenv from 'dotenv';" if is_ts else "const dotenv = require('dotenv');"}
dotenv.config();

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this';
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '7d';

export function generateToken(payload{"" if is_ts else ""}) {"{"}
  return jwt.sign(payload, JWT_SECRET, {"{"} expiresIn: JWT_EXPIRES_IN {"}"});
{"}"}

export function verifyToken(token{"" if is_ts else ""}) {"{"}
  try {"{"}
    return jwt.verify(token, JWT_SECRET);
  {"}"} catch (error) {"{"}
    return null;
  {"}"}
{"}"}

export function authMiddleware(req{"" if is_ts else ""}, res{"" if is_ts else ""}, next{"" if is_ts else ""}) {"{"}
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {"{"}
    return res.status(401).json({"{"} error: 'No token provided' {"}"});
  {"}"}

  const token = authHeader.substring(7);
  const decoded = verifyToken(token);

  if (!decoded) {"{"}
    return res.status(401).json({"{"} error: 'Invalid token' {"}"});
  {"}"}

  req.user = decoded;
  next();
{"}"}

// Password hashing utilities
{"import bcrypt from 'bcrypt';" if is_ts else "const bcrypt = require('bcrypt');"}

export async function hashPassword(password{"" if is_ts else ""}) {"{"}
  return await bcrypt.hash(password, 10);
{"}"}

export async function comparePassword(password{"" if is_ts else ""}, hash{"" if is_ts else ""}) {"{"}
  return await bcrypt.compare(password, hash);
{"}"}
'''

                with open(project_path / f"auth.{ext}", 'w') as f:
                    f.write(auth_code)

                # Update package.json
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)

                    if "dependencies" not in pkg_data:
                        pkg_data["dependencies"] = {}

                    pkg_data["dependencies"]["jsonwebtoken"] = "^9.0.0"
                    pkg_data["dependencies"]["bcrypt"] = "^5.1.0"

                    if is_ts:
                        if "devDependencies" not in pkg_data:
                            pkg_data["devDependencies"] = {}
                        pkg_data["devDependencies"]["@types/jsonwebtoken"] = "^9.0.0"
                        pkg_data["devDependencies"]["@types/bcrypt"] = "^5.0.0"

                    with open(pkg_file, 'w') as f:
                        json.dump(pkg_data, f, indent=2)

                output = f"JWT Authentication setup complete!\n"
                output += f"- Created auth.{ext} with JWT functions\n"
                output += "- Added password hashing utilities\n"
                output += "- Updated package.json\n"

            elif language == "python":
                if framework == "fastapi":
                    auth_code = '''"""JWT Authentication for FastAPI"""

import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-this")
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", "7"))  # days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=JWT_EXPIRES_IN)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    return payload
'''

                    with open(project_path / "auth.py", 'w') as f:
                        f.write(auth_code)

                    # Update requirements.txt
                    req_file = project_path / "requirements.txt"
                    requirements = []
                    if req_file.exists():
                        requirements = req_file.read_text().splitlines()

                    new_deps = [
                        "python-jose[cryptography]>=3.3.0",
                        "passlib[bcrypt]>=1.7.4",
                        "python-multipart>=0.0.6"
                    ]

                    for dep in new_deps:
                        if dep.split("[")[0].split(">=")[0] not in str(requirements):
                            requirements.append(dep)

                    with open(req_file, 'w') as f:
                        f.write("\n".join(requirements))

                    output = "JWT Authentication setup complete!\n"
                    output += "- Created auth.py with JWT functions\n"
                    output += "- Added password hashing utilities\n"
                    output += "- Updated requirements.txt\n"

            # Update .env
            env_file = project_path / ".env"
            env_content = ""
            if env_file.exists():
                env_content = env_file.read_text()

            if "JWT_SECRET" not in env_content:
                import secrets
                secret_key = secrets.token_urlsafe(32)
                env_content += f"\nJWT_SECRET={secret_key}\n"
                env_content += "JWT_EXPIRES_IN=7\n"

            with open(env_file, 'w') as f:
                f.write(env_content)

            output += "\n⚠️  Important: JWT_SECRET has been generated in .env\n"
            output += "Keep this secret safe and never commit it to version control!"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"language": language, "framework": framework}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up JWT auth: {str(e)}"
            )


class RateLimitSetupTool(Tool):
    """Tool for setting up rate limiting"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "RateLimitSetup"

    @property
    def description(self) -> str:
        return "Sets up rate limiting middleware for API protection"

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
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi"],
                    "description": "Web framework"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max requests per window (default: 100)"
                },
                "window_minutes": {
                    "type": "integer",
                    "description": "Time window in minutes (default: 15)"
                }
            },
            "required": ["language", "framework"]
        }

    def execute(self, language: str, framework: str,
                limit: int = 100, window_minutes: int = 15) -> ToolResult:
        """Set up rate limiting"""
        try:
            project_path = Path(self.working_directory)

            if language in ["javascript", "typescript"] and framework == "express":
                # Update package.json
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)

                    if "dependencies" not in pkg_data:
                        pkg_data["dependencies"] = {}

                    pkg_data["dependencies"]["express-rate-limit"] = "^7.1.0"

                    with open(pkg_file, 'w') as f:
                        json.dump(pkg_data, f, indent=2)

                is_ts = language == "typescript"
                ext = "ts" if is_ts else "js"

                rate_limit_code = f'''{"import rateLimit from 'express-rate-limit';" if is_ts else "const rateLimit = require('express-rate-limit');"}

// Basic rate limiter
export const limiter = rateLimit({"{"}
  windowMs: {window_minutes} * 60 * 1000, // {window_minutes} minutes
  max: {limit}, // Limit each IP to {limit} requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
{"}"});

// Stricter rate limiter for auth endpoints
export const authLimiter = rateLimit({"{"}
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Only 5 requests per 15 minutes
  message: 'Too many authentication attempts, please try again later.',
  skipSuccessfulRequests: true,
{"}"});

// Usage:
// app.use('/api/', limiter);
// app.use('/auth/', authLimiter);
'''

                with open(project_path / f"rate-limit.{ext}", 'w') as f:
                    f.write(rate_limit_code)

                output = "Rate limiting setup complete!\n"
                output += f"- Created rate-limit.{ext}\n"
                output += f"- Configured: {limit} requests per {window_minutes} minutes\n"
                output += "- Added stricter limiter for auth endpoints\n"

            elif language == "python" and framework == "fastapi":
                rate_limit_code = '''"""Rate limiting middleware for FastAPI"""

import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from functools import wraps

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 60):
        """
        Rate limiter

        Args:
            requests: Maximum number of requests
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.clients = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make a request"""
        now = time.time()

        # Remove old requests outside the window
        self.clients[client_id] = [
            req_time for req_time in self.clients[client_id]
            if now - req_time < self.window
        ]

        # Check if under limit
        if len(self.clients[client_id]) < self.requests:
            self.clients[client_id].append(now)
            return True

        return False

# Create rate limiters
general_limiter = RateLimiter(requests=100, window=900)  # 100 req per 15 min
auth_limiter = RateLimiter(requests=5, window=900)  # 5 req per 15 min

def rate_limit(limiter: RateLimiter = general_limiter):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host

            if not limiter.is_allowed(client_ip):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later."
                )

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Usage:
# @app.get("/api/endpoint")
# @rate_limit()
# async def endpoint(request: Request):
#     ...
'''

                with open(project_path / "rate_limit.py", 'w') as f:
                    f.write(rate_limit_code)

                output = "Rate limiting setup complete!\n"
                output += "- Created rate_limit.py with middleware\n"
                output += f"- Configured: {limit} requests per {window_minutes} minutes\n"

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"limit": limit, "window_minutes": window_minutes}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up rate limiting: {str(e)}"
            )


class CORSSetupTool(Tool):
    """Tool for setting up CORS configuration"""

    def __init__(self, working_directory: str = None):
        self.working_directory = working_directory or "."

    @property
    def name(self) -> str:
        return "CORSSetup"

    @property
    def description(self) -> str:
        return "Sets up CORS (Cross-Origin Resource Sharing) configuration"

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
                "framework": {
                    "type": "string",
                    "enum": ["express", "fastapi"],
                    "description": "Web framework"
                },
                "allowed_origins": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Allowed origins"
                }
            },
            "required": ["language", "framework"]
        }

    def execute(self, language: str, framework: str,
                allowed_origins: list = None) -> ToolResult:
        """Set up CORS"""
        try:
            project_path = Path(self.working_directory)

            if not allowed_origins:
                allowed_origins = ["http://localhost:3000", "http://localhost:5173"]

            if language in ["javascript", "typescript"] and framework == "express":
                is_ts = language == "typescript"
                ext = "ts" if is_ts else "js"

                cors_code = f'''{"import cors from 'cors';" if is_ts else "const cors = require('cors');"}

const corsOptions = {"{"}
  origin: process.env.ALLOWED_ORIGINS?.split(',') || {json.dumps(allowed_origins)},
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization'],
{"}"};

export const corsMiddleware = cors(corsOptions);

// Usage:
// app.use(corsMiddleware);
'''

                with open(project_path / f"cors-config.{ext}", 'w') as f:
                    f.write(cors_code)

                # Update package.json
                pkg_file = project_path / "package.json"
                if pkg_file.exists():
                    with open(pkg_file, 'r') as f:
                        pkg_data = json.load(f)

                    if "dependencies" not in pkg_data:
                        pkg_data["dependencies"] = {}

                    pkg_data["dependencies"]["cors"] = "^2.8.5"

                    with open(pkg_file, 'w') as f:
                        json.dump(pkg_data, f, indent=2)

                output = "CORS setup complete!\n"
                output += f"- Created cors-config.{ext}\n"
                output += f"- Allowed origins: {', '.join(allowed_origins)}\n"

            elif language == "python" and framework == "fastapi":
                cors_code = f'''"""CORS configuration for FastAPI"""

from fastapi.middleware.cors import CORSMiddleware
import os

# Get allowed origins from environment or use defaults
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "{','.join(allowed_origins)}")
allowed_origins = allowed_origins_str.split(",")

cors_config = {{
    "allow_origins": allowed_origins,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}}

def setup_cors(app):
    """Add CORS middleware to FastAPI app"""
    app.add_middleware(
        CORSMiddleware,
        **cors_config
    )

# Usage:
# from cors_config import setup_cors
# setup_cors(app)
'''

                with open(project_path / "cors_config.py", 'w') as f:
                    f.write(cors_code)

                output = "CORS setup complete!\n"
                output += "- Created cors_config.py\n"
                output += f"- Allowed origins: {', '.join(allowed_origins)}\n"

            # Update .env
            env_file = project_path / ".env"
            env_content = ""
            if env_file.exists():
                env_content = env_file.read_text()

            if "ALLOWED_ORIGINS" not in env_content:
                env_content += f"\nALLOWED_ORIGINS={','.join(allowed_origins)}\n"

            with open(env_file, 'w') as f:
                f.write(env_content)

            return ToolResult(
                status=ToolStatus.SUCCESS,
                output=output,
                metadata={"allowed_origins": allowed_origins}
            )

        except Exception as e:
            return ToolResult(
                status=ToolStatus.ERROR,
                output="",
                error=f"Error setting up CORS: {str(e)}"
            )
