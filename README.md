# LLMCode - AI-Powered Full-Stack Development Assistant

A powerful AI coding assistant powered by Claude that can create complete applications from scratch. Build full-stack web applications, REST APIs, and scalable backends with natural language commands.

## ⚡ Key Features

### 🚀 Full-Stack Development
- **Frontend Frameworks**: React, Vue.js, Next.js, Svelte
- **Backend Frameworks**: Express.js, FastAPI, Flask
- **Databases**: MongoDB, PostgreSQL, Redis
- **Complete App Generation**: One command to create entire applications

### 🔐 Security & Authentication
- **JWT Authentication**: Automatic setup with token generation/verification
- **Password Hashing**: BCrypt integration for secure password storage
- **Rate Limiting**: Protect APIs from abuse
- **CORS Configuration**: Cross-origin resource sharing setup

### 🐳 DevOps & Infrastructure
- **Docker**: Automatic Dockerfile and docker-compose generation
- **Containerization**: Multi-service orchestration
- **Environment Management**: Secure .env configuration
- **Production-Ready**: Scalable infrastructure setup

### 🔧 Development Tools
- **Package Management**: NPM, pip automation
- **API Development**: CRUD endpoint generation, Swagger docs
- **Code Operations**: Read, write, edit files intelligently
- **Command Execution**: Run bash commands and scripts
- **Git Integration**: Repository awareness and operations

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llmcode.git
cd llmcode

# Run setup script
bash setup.sh

# Or manual installation
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"
```

## 🚀 Quick Start

### Interactive Mode

```bash
llmcode
```

### Create a Full-Stack Application

```bash
llmcode "Create a full-stack todo app with React frontend, Express backend, MongoDB database, and Docker support"
```

### Create a REST API with Authentication

```bash
llmcode "Create a REST API with Express, MongoDB, JWT auth, and rate limiting for a blog platform"
```

### Single Command Examples

```bash
# Create React app
llmcode "Create a React app with TypeScript using Vite"

# Set up database
llmcode "Add MongoDB integration with connection pooling"

# Add authentication
llmcode "Implement JWT authentication with login and register endpoints"

# Generate API endpoints
llmcode "Create CRUD API endpoints for a User resource"

# Docker setup
llmcode "Create Dockerfile and docker-compose with PostgreSQL and Redis"
```

## 🛠️ Available Tools

### File Operations
- **Read**: Read file contents with line numbers
- **Write**: Create new files with content
- **Edit**: Modify existing files with precision

### System Tools
- **Bash**: Execute shell commands
- **Glob**: Find files by pattern matching
- **Grep**: Search file contents with regex

### Node.js/JavaScript
- **NpmInstall**: Install NPM packages
- **PackageJson**: Manage package.json
- **NpmRun**: Execute NPM scripts

### Project Scaffolding
- **CreateReactApp**: Generate React applications (Vite/CRA/Next.js)
- **CreateVueApp**: Generate Vue.js applications
- **CreateExpressApp**: Generate Express.js backends
- **CreateFullStackApp**: Generate complete full-stack projects

### Database Integration
- **MongoDBSetup**: MongoDB connection and configuration
- **RedisSetup**: Redis caching and session store
- **PostgreSQLSetup**: PostgreSQL with Prisma/Sequelize/SQLAlchemy

### Docker & Containerization
- **DockerfileGenerator**: Generate optimized Dockerfiles
- **DockerCompose**: Create docker-compose.yml configurations
- **DockerCommand**: Execute Docker commands

### Security Tools
- **JWTAuthSetup**: Complete JWT authentication setup
- **RateLimitSetup**: API rate limiting configuration
- **CORSSetup**: Cross-origin resource sharing setup

### API Development
- **APIEndpointGenerator**: Generate REST CRUD endpoints
- **SwaggerSetup**: API documentation with Swagger/OpenAPI

### Web Tools
- **WebSearch**: Search the web (requires API key)
- **WebFetch**: Fetch web page content

## 💡 Usage Examples

### Example 1: Create a Todo Application

```bash
llmcode
> Create a full-stack todo application with:
  - React frontend with TypeScript
  - Express backend with TypeScript
  - MongoDB for data storage
  - JWT authentication
  - Docker support
  - CRUD operations for todos
```

### Example 2: Add Features to Existing Project

```bash
llmcode
> Add user authentication to this Express app with JWT
> Set up Redis for session management
> Create API endpoints for a Comment resource
> Add rate limiting to all API routes
```

### Example 3: DevOps Setup

```bash
llmcode
> Create a Dockerfile for this Node.js app
> Set up docker-compose with MongoDB, Redis, and Nginx
> Generate .env.example with all required variables
```

## 🎯 Common Use Cases

### Full-Stack Web Applications
```
"Create a social media platform with posts, comments, likes, and user profiles"
```

### REST APIs
```
"Build a REST API for an e-commerce store with products, orders, and payments"
```

### Microservices
```
"Create a microservices architecture with auth service, API gateway, and user service"
```

### Real-Time Applications
```
"Build a real-time chat application with WebSocket support"
```

### Admin Dashboards
```
"Create an admin dashboard with analytics, user management, and data visualization"
```

## 📁 Project Structure

```
llmcode/
├── llmcode/                    # Main package
│   ├── cli.py                 # Command-line interface
│   ├── llm_client.py          # Claude API client
│   ├── config.py              # Configuration management
│   ├── session.py             # Session handling
│   ├── git_utils.py           # Git integration
│   └── tools/                 # Tool implementations
│       ├── file_tools.py      # File operations
│       ├── bash_tool.py       # Command execution
│       ├── node_tools.py      # Node.js/NPM
│       ├── scaffold_tools.py  # Project generation
│       ├── database_tools.py  # Database setup
│       ├── docker_tools.py    # Docker/containerization
│       ├── security_tools.py  # Authentication/security
│       ├── api_tools.py       # API development
│       ├── search_tools.py    # Code search
│       └── web_tools.py       # Web access
├── examples/                   # Usage examples
│   ├── create_fullstack_app.py
│   ├── create_api_with_auth.py
│   └── docker_deployment.py
├── tests/                      # Test suite
├── README.md                   # This file
├── CLAUDE.md                   # AI assistant guide
└── pyproject.toml             # Dependencies

```

## ⚙️ Configuration

Create a `.env` file in your project:

```env
# Required
ANTHROPIC_API_KEY=your-api-key-here

# Optional
DEFAULT_MODEL=claude-sonnet-4-5-20250929
MAX_TOKENS=8000
TEMPERATURE=1.0
SERPER_API_KEY=your-serper-key-here  # For web search
```

## 🧪 Examples

Run the included examples to see LLMCode in action:

```bash
# Create a full-stack application
python examples/create_fullstack_app.py

# Create an API with authentication
python examples/create_api_with_auth.py

# Set up Docker deployment
python examples/docker_deployment.py
```

## 🎓 Tutorials

### Creating Your First Full-Stack App

1. **Start LLMCode**:
   ```bash
   llmcode
   ```

2. **Request the application**:
   ```
   Create a blog platform with React frontend, Express backend, and MongoDB
   ```

3. **LLMCode will**:
   - Create project structure
   - Set up frontend with routing and components
   - Create backend with API endpoints
   - Configure MongoDB connection
   - Add authentication
   - Set up Docker
   - Generate documentation

4. **Run your app**:
   ```bash
   cd blog-platform
   npm run install:all
   docker-compose up -d
   npm run dev
   ```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)**: Comprehensive technical guide for AI assistants
- **[Examples](examples/)**: Practical usage examples
- **[Tests](tests/)**: Test suite and examples

## 🔧 Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black llmcode/ tests/ examples/
ruff check llmcode/ tests/ examples/

# Type checking
mypy llmcode/
```

## 🌟 What Makes LLMCode Special?

Unlike traditional code generators, LLMCode:

✅ **Understands Context**: Reads your existing code before making changes
✅ **Full-Stack Ready**: Creates complete applications, not just snippets
✅ **Production-Quality**: Includes security, error handling, and best practices
✅ **DevOps Integrated**: Automatic Docker and deployment configuration
✅ **Conversational**: Chat naturally to build and modify applications
✅ **Extensible**: Easy to add custom tools and capabilities

## 🚀 Roadmap

- [ ] Cloud deployment (AWS, GCP, Azure, Vercel)
- [ ] Kubernetes configurations
- [ ] Testing framework integration
- [ ] CI/CD pipeline generation
- [ ] GraphQL API support
- [ ] WebSocket real-time features
- [ ] Database migrations
- [ ] Monitoring and logging setup

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Built with inspiration from Claude Code
- Terminal UI with [Rich](https://github.com/Textualize/rich)

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/llmcode/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/llmcode/discussions)
- **Documentation**: [Full Documentation](https://llmcode.dev)

---

**Start building complete applications with AI today!** 🚀

```bash
llmcode "Create my dream application"
```
