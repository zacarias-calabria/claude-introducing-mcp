# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Application
```bash
# With uv (recommended)
uv run main.py

# With Python directly
python main.py

# With additional MCP server scripts
uv run main.py server1.py server2.py
```

### Development Setup
```bash
# Install dependencies with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Install dependencies without uv
python -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

### Environment Configuration
Create a `.env` file with:
```
ANTHROPIC_API_KEY=""      # Required: Your Anthropic API secret key
CLAUDE_MODEL=""           # Required: Claude model to use
USE_UV="1"                # Optional: Set to use uv for running MCP server
```

## Architecture

### Core Components

**Main Entry Point (`main.py`)**
- Initializes Claude service, MCP clients, and CLI interface
- Supports running additional MCP server scripts via command line arguments
- Manages async context stack for proper client lifecycle

**MCP Architecture**
- `MCPClient`: Wrapper around MCP stdio client for tool execution and resource access
- `mcp_server.py`: FastMCP server providing document management tools and resources
- Multiple MCP clients can be spawned from command line arguments

**Chat System**
- `Chat`: Base chat class handling Claude API interactions and tool execution
- `CliChat`: CLI-specific chat implementation with document retrieval and command processing
- `Claude`: Anthropic API wrapper with message management

**CLI Interface**
- `CliApp`: Terminal interface with auto-completion and key bindings
- `UnifiedCompleter`: Provides completions for commands (`/`) and resources (`@`)
- `CommandAutoSuggest`: Auto-suggests command arguments

**Tool Management**
- `ToolManager`: Aggregates tools from multiple MCP clients and handles execution
- Supports tool discovery, execution, and error handling across clients

### Key Features

**Document Retrieval**: Use `@document_id` to include document content in queries
**Commands**: Use `/command` prefix to execute MCP server prompts
**Multi-Client Support**: Can connect to multiple MCP servers simultaneously

### Document Management
The built-in MCP server (`mcp_server.py`) provides:
- `read_document`: Read document content by ID
- `edit_document`: Edit document content with string replacement
- `list_documents`: Resource to get all document IDs
- `fetch_document`: Resource to get specific document content

### TODOs in Codebase
- `mcp_server.py`: Complete prompts for markdown rewriting and document summarization
- `mcp_client.py`: Implement missing prompt and resource functionality

### Development Notes
- No linting or type checking configured
- Uses uv for dependency management and script execution
- Requires Python 3.10+
- MCP servers run as separate processes via stdio transport