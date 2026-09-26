# AI Software Engineering Assistant

An AI-powered software engineering assistant that understands GitHub repositories, retrieves relevant source code and documentation, and uses RAG, LLM reasoning, repository inspection tools, and MCP-based tool execution to answer software engineering questions with source-grounded context.

---

## Overview

The AI Software Engineering Assistant is designed to help developers understand and investigate software repositories.

Instead of treating a repository as a collection of documents, the system combines:

- Repository ingestion
- Code-aware chunking
- Embeddings
- PostgreSQL with pgvector
- Semantic retrieval
- Retrieval-Augmented Generation (RAG)
- Gemini LLM
- Agentic tool use
- MCP
- Repository inspection tools
- Source-aware responses

The system can register a GitHub repository, clone and index it, retrieve relevant code, inspect files and repository structure, and use an AI agent to investigate questions before producing an answer.

---

## Key Capabilities

### Repository Understanding

- Register GitHub repositories
- Clone repositories automatically
- Track repository indexing status
- Extract supported source/document files
- Chunk repository content
- Generate embeddings
- Store embeddings in PostgreSQL using pgvector

### Retrieval

- Semantic similarity search
- Repository-specific retrieval
- Metadata filtering
- Document-type filtering
- Programming-language filtering
- Configurable `top_k` retrieval

### RAG

The system constructs repository context from retrieved chunks and provides that context to the LLM.

The RAG pipeline is:

```text
User Question
      ↓
Embedding
      ↓
pgvector Similarity Search
      ↓
Relevant Repository Chunks
      ↓
Context Construction
      ↓
RAG Prompt
      ↓
Gemini
      ↓
Answer
```

### Agentic Investigation

The agent can decide when repository tools are required instead of relying only on retrieved context.

The agent supports:

- Iterative reasoning
- Tool selection
- Tool execution
- Tool-call limits
- Iteration limits
- Tool argument validation
- LLM timeout handling
- MCP-based tool discovery
- MCP-based tool execution

### MCP

The project uses the Model Context Protocol to expose repository capabilities to the AI agent through a standardized tool interface.

The MCP server exposes repository tools and the MCP client discovers and executes them.

Current MCP tools include:

| Tool | Purpose |
|---|---|
| `search_repository_code` | Search source code for a query |
| `read_repository_file` | Read a repository file |
| `list_repository_files` | List repository files |
| `get_repository_information` | Inspect repository Git information |
| `get_python_code_structure` | Inspect Python classes, functions, and methods |

---

## Architecture

```text
                         Developer
                             │
                             ▼
                      ┌─────────────┐
                      │   FastAPI   │
                      │     API     │
                      └──────┬──────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  AI Agent /     │
                    │  Orchestrator   │
                    └───────┬─────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
           RAG          MCP Client     Gemini
              │             │          LLM
              │             ▼
              │        MCP Server
              │             │
              │             ▼
              │      Repository Tools
              │
              ▼
       PostgreSQL + pgvector
              │
              ▼
       Repository Knowledge
```

---

## Core Concepts

The system separates several responsibilities:

```text
RAG       → Know
Tools     → Do
Agent     → Decide
MCP       → Standardized capability interface
LLM       → Reason and generate
```

### RAG

RAG retrieves relevant repository context before generating an answer.

### Tools

Tools allow the system to directly inspect the repository.

For example:

```text
Search code
Read file
List files
Inspect Git information
Inspect Python structure
```

### Agent

The agent determines whether the retrieved context is sufficient or whether additional repository investigation is required.

### MCP

MCP provides the standardized interface between the AI agent and repository capabilities.

---

## Repository Lifecycle

When a repository is registered, it follows this lifecycle:

```text
REGISTER
   ↓
CLONING
   ↓
INDEXING
   ↓
READY
```

If an error occurs:

```text
CLONING ──────┐
              │
INDEXING ─────┼──→ FAILED
              │
```

Repository metadata includes:

- Repository name
- GitHub URL
- Status
- Index timestamp
- Error message

---

## Repository Ingestion Pipeline

```text
GitHub Repository
       ↓
Repository Registration
       ↓
Git Clone
       ↓
File Filtering
       ↓
Document Loading
       ↓
Chunking
       ↓
Embedding Generation
       ↓
PostgreSQL + pgvector
       ↓
Repository READY
```

The indexed content becomes available to the retrieval system.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### AI

- Gemini
- Embeddings
- Retrieval-Augmented Generation
- Agentic workflows

### Database

- PostgreSQL
- pgvector

### Repository Analysis

- Git
- Python AST
- Repository inspection tools

### Protocol

- Model Context Protocol (MCP)

### Infrastructure

- Docker
- Docker Compose

---

## Project Structure

```text
ai-software-engineering-assistant/
│
├── app/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── mcp_tool_executor.py
│   │   ├── mcp_tools.py
│   │   ├── models.py
│   │   ├── tool_call.py
│   │   ├── tool_context.py
│   │   └── tool_executor.py
│   │
│   ├── ai/
│   │   ├── gemini.py
│   │   └── interface.py
│   │
│   ├── api/
│   │   ├── agent.py
│   │   ├── ai.py
│   │   ├── repository.py
│   │   └── retrieval.py
│   │
│   ├── chunking/
│   │   ├── chunk.py
│   │   ├── code.py
│   │   ├── strategy.py
│   │   └── text.py
│   │
│   ├── core/
│   │   ├── agent_dependencies.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── logging_config.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models/
│   │       ├── base.py
│   │       ├── repository.py
│   │       └── vector_chunk.py
│   │
│   ├── embeddings/
│   │   ├── gemini.py
│   │   ├── interface.py
│   │   ├── model.py
│   │   └── service.py
│   │
│   ├── evaluation/
│   │   ├── dataset.py
│   │   ├── evaluator.py
│   │   ├── metrics.py
│   │   ├── models.py
│   │   ├── retrieval_dataset.py
│   │   └── retrieval_evaluator.py
│   │
│   ├── ingestion/
│   │   ├── document.py
│   │   ├── file_filter.py
│   │   ├── loader.py
│   │   └── repository.py
│   │
│   ├── mcp/
│   │   ├── adapter.py
│   │   ├── client.py
│   │   ├── client_test.py
│   │   └── server.py
│   │
│   ├── repositories/
│   │   └── repository.py
│   │
│   ├── schemas/
│   │   ├── agent.py
│   │   ├── ai.py
│   │   ├── repository.py
│   │   └── retrieval.py
│   │
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── ai_service.py
│   │   ├── context_service.py
│   │   ├── embedding_service.py
│   │   ├── ingestion_service.py
│   │   ├── rag_service.py
│   │   ├── repository_service.py
│   │   ├── repository_worker.py
│   │   └── retrieval_service.py
│   │
│   ├── tools/
│   │   ├── base.py
│   │   ├── code_structure.py
│   │   ├── code_structure_tool.py
│   │   ├── executor.py
│   │   ├── list_files.py
│   │   ├── list_files_tool.py
│   │   ├── read_file.py
│   │   ├── read_file_tool.py
│   │   ├── registry.py
│   │   ├── repository_info.py
│   │   ├── repository_info_tool.py
│   │   ├── schemas.py
│   │   ├── search_code.py
│   │   └── search_code_tool.py
│   │
│   ├── vectorstore/
│   │   ├── model.py
│   │   └── repository.py
│   │
│   └── main.py
│
├── alembic/
├── data/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── alembic.ini
```

---

## Requirements

- Python 3.12
- Docker
- Docker Compose
- Git
- Gemini API key

PostgreSQL is provided through Docker using the pgvector image.

---

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+psycopg://aiassistant:aiassistant@postgres:5432/aiassistant

DEBUG=true

AGENT_MAX_ITERATIONS=5
AGENT_MAX_TOOL_CALLS=10

LLM_TIMEOUT_SECONDS=60
```

Never commit `.env` to Git.

The project `.gitignore` excludes:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
data/cloned_repositories/
```

---

## Local Development

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Setup

Start PostgreSQL and the application:

```bash
docker compose up --build
```

The PostgreSQL service uses:

```text
PostgreSQL 16
pgvector
```

The PostgreSQL container exposes port `5432` internally and port `5433` on the host.

The application connects to PostgreSQL through the Docker service name:

```text
postgres:5432
```

---

## Alembic Migrations

Apply all database migrations:

```bash
alembic upgrade head
```

Check the current migration:

```bash
alembic current
```

Check migration history:

```bash
alembic history
```

The current migration chain is:

```text
<base>
   ↓
b9be62ee67a2
   create repository and vector tables
   ↓
ab8a569a568f
   add repository status
   ↓
7ceb339366ab
   add repository indexing metadata
```

The database schema uses:

```text
repositories
knowledge_chunks
alembic_version
```

---

## Running the Application

With Docker:

```bash
docker compose up --build
```

The API is available at:

```text
http://localhost:8000
```

FastAPI's interactive documentation is available through the standard FastAPI documentation endpoints.

Health check:

```text
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

## API Endpoints

### Health

```text
GET /health
```

Checks whether the API process is running.

---

### Register Repository

```text
POST /repositories
```

Registers a GitHub repository and starts repository processing in the background.

The repository progresses through:

```text
CLONING → INDEXING → READY
```

or:

```text
FAILED
```

---

### Repository Status

```text
GET /repositories/{repository_id}
```

Returns repository metadata and current indexing status.

---

### Retrieval Search

```text
POST /retrieval/search
```

Performs semantic retrieval against indexed repository content.

Request fields include:

```json
{
  "repository_id": 1,
  "query": "How does authentication work?",
  "top_k": 5,
  "document_type": "code",
  "language": "python"
}
```

`top_k` is constrained between 1 and 20.

---

### RAG Question

```text
POST /ai/ask
```

Uses retrieved repository context to generate an AI response.

The response includes the generated answer and retrieved source information.

---

### Agent Question

```text
POST /repositories/{repository_id}/ask
```

Sends a question to the software engineering agent.

The agent can:

1. Retrieve relevant context.
2. Determine whether additional investigation is required.
3. Discover available MCP tools.
4. Call repository inspection tools.
5. Use tool results as additional context.
6. Continue investigation when necessary.
7. Generate a final answer.

---

## Agent Execution Flow

```text
User Question
      ↓
Agent
      ↓
Initial Retrieval
      ↓
Context Construction
      ↓
Gemini
      │
      ├── Final Answer
      │
      └── Tool Call
             ↓
          MCP Client
             ↓
          MCP Server
             ↓
       Repository Tool
             ↓
          Tool Result
             ↓
           Agent
             ↓
          Gemini
             ↓
       Final Answer
```

The agent protects execution using:

```text
Maximum iterations
Maximum tool calls
Tool argument validation
LLM timeout
Repository readiness checks
```

---

## MCP Architecture

The MCP client starts the MCP server and establishes a stdio connection.

```text
Agent
  ↓
MCP Client
  ↓
MCP Server
  ↓
Tool Registry / Adapter
  ↓
Repository Tool
  ↓
Repository
```

The MCP server exposes repository capabilities through MCP tool definitions.

The MCP client discovers those tools dynamically and provides their schemas to the LLM.

---

## Repository Tools

### Search Code

Searches repository source files for a query.

```text
search_repository_code
```

Returns:

- source file
- line number
- matching content

### Read File

```text
read_repository_file
```

Reads an individual supported repository file.

Path traversal outside the repository is rejected.

### List Files

```text
list_repository_files
```

Lists repository files while respecting repository file filtering rules.

### Repository Information

```text
get_repository_information
```

Provides repository Git information such as:

- current branch
- latest commit
- latest commit message
- repository status

### Python Code Structure

```text
get_python_code_structure
```

Uses Python AST parsing to identify:

- classes
- functions
- methods
- source locations

---

## Security Considerations

The application includes several repository-level security protections.

### GitHub URL Validation

Repository registration only accepts HTTPS GitHub URLs.

### Path Traversal Protection

Repository file access resolves the requested path and verifies that it remains inside the repository root.

### Ignored Directories

Configured ignored directories cannot be accessed through repository file tools.

### File Type Filtering

Unsupported file types are rejected or skipped.

### Environment Secrets

Secrets are loaded through environment variables and `.env`.

`.env` is excluded from Git.

### Tool Limits

Agent execution is constrained by:

```text
AGENT_MAX_ITERATIONS
AGENT_MAX_TOOL_CALLS
```

### LLM Timeout

LLM calls are protected by:

```text
LLM_TIMEOUT_SECONDS
```

---

## Logging

Application logging is configured centrally.

Operational logging uses Python's `logging` module rather than application-level `print()` statements.

MCP stdio communication is kept separate from application logging so that stdout remains available for MCP JSON-RPC communication.

---

## Error Handling

The application defines dedicated exceptions for important repository and agent states.

Examples include:

```text
RepositoryNotFoundError
RepositoryNotReadyError
ToolExecutionError
AgentExecutionError
```

Repository processing failures are stored with the repository's error message and the repository is moved to:

```text
FAILED
```

---

## Evaluation

The project includes retrieval evaluation infrastructure.

Current evaluation metrics include:

- Precision@K
- Recall@K
- Mean Reciprocal Rank (MRR)

The evaluation dataset contains repository-oriented questions such as:

- Authentication implementation
- Database connection
- Application startup

Evaluation is kept separate from the core application workflow so retrieval quality can be measured independently.

---

## Development Verification

The project uses manual verification scripts rather than pytest for the current development workflow.

Examples include checks for:

- ingestion
- embeddings
- vector storage
- retrieval
- retrieval service
- context construction
- MCP tools

Python compilation can be checked with:

```bash
python -m compileall app
```

---

## Current Architecture Principles

The project intentionally separates:

```text
Ingestion
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Store
   ↓
Retrieval
   ↓
Context
   ↓
RAG / Agent
   ↓
LLM
```

Repository capabilities are separated from AI reasoning:

```text
AI reasoning
     ↓
Agent
     ↓
MCP
     ↓
Repository tools
```

This separation allows the system to evolve from simple retrieval-based question answering toward more capable software engineering workflows.

---

## Future Improvements

Potential future improvements include:

- More sophisticated code-aware chunking
- Improved retrieval ranking
- Hybrid lexical + semantic retrieval
- Repository-wide dependency analysis
- Symbol-aware code search
- GitHub API integration
- Additional programming-language parsers
- More sophisticated agent planning
- Additional engineering tools
- Automated evaluation expansion
- Authentication and authorization for multi-user deployments
- Streaming responses
- Persistent conversation history
- Production-grade background job processing

These are future extensions rather than requirements of the current implementation.

---

## Project Status

The current implementation provides a complete foundation for an AI software engineering assistant with:

```text
Repository ingestion       ✅
Embeddings                 ✅
PostgreSQL + pgvector      ✅
Semantic retrieval         ✅
RAG                        ✅
Gemini integration         ✅
Agent orchestration        ✅
MCP                        ✅
Repository tools           ✅
Background processing      ✅
API layer                  ✅
Alembic migrations         ✅
Docker                     ✅
Security hardening         ✅
Logging                    ✅
Retrieval evaluation       ✅
```

The remaining work is primarily final end-to-end verification and evaluation of retrieval and agent quality.
