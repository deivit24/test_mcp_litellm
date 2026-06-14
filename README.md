# MCP Server Playground

A learning project for building and testing custom MCP (Model Context Protocol) servers connected to a deployed LiteLLM proxy.

## What This Is

This project explores how to:

- Build a REST API and automatically expose it as an MCP server
- Register that MCP server with a LiteLLM proxy
- Chat with an LLM that can call your custom tools via MCP
- Test the whole flow from a CLI

## Architecture

```
┌─────────────┐     MCP protocol      ┌──────────────┐     HTTP      ┌──────────────┐
│  LiteLLM    │ ──────────────────── ▶│  MCP Server  │ ────────────▶ │  FastAPI     │
│  Proxy      │                       │  :8001       │               │  :8000       │
│  (deployed) │                       └──────────────┘               └──────────────┘
└─────────────┘
       ▲
       │  OpenAI-compatible API
       │
┌─────────────┐
│   CLI       │
│  (cli.py)   │
└─────────────┘
```

**FastAPI** (`api/`) — serves two endpoints:

- `GET /home` — returns a random David Salazar fact
- `GET /faq` — returns Japan FAQ Q&A pairs

**MCP Server** (`mcp_server/`) — wraps the FastAPI via its OpenAPI spec and exposes the routes as MCP tools. LiteLLM registers this server and makes the tools available to the LLM.

**LiteLLM Proxy** — deployed externally. Holds your Anthropic API key, registers your MCP server, and handles all LLM routing.

**CLI** (`cli.py`) — interactive chat tool. Lists available MCP tools, lets you pick one, then chats with the LLM using that tool.

## Project Structure

```
faq/
├── api/
│   └── main.py          # FastAPI routes
├── mcp_server/
│   └── server.py        # MCP server (auto-generated from OpenAPI spec)
├── core/
│   ├── llm.py           # LLMService — async chat via LiteLLM proxy
│   ├── models.py        # Shared Pydantic models
│   └── settings.py      # Config loaded from .env
├── cli.py               # Interactive CLI chat tool
├── .env.example         # Environment variable template
└── pyproject.toml
```

## Setup

**1. Install dependencies**

```bash
uv sync
```

**2. Configure environment**

```bash
cp .env.example .env
```

Edit `.env` with your values:

```
BASE_URL="http://localhost:8000/"
BASE_URL_DOCS="http://localhost:8000/openapi.json"
OPENAI_KEY="sk-your-litellm-master-key"
LITELLM_URL="https://your-litellm-proxy.com"   # or http://localhost:4000 locally
```

## Running Locally

Start each service in a separate terminal:

```bash
# 1. FastAPI
uv run uvicorn api.main:app --reload --port 8000

# 2. MCP Server (requires FastAPI to be running first)
uv run python mcp_server/server.py

# 3. CLI chat tool (requires MCP server to be running)
uv run python cli.py
```

## Deploying

Both `api/` and `mcp_server/` live in this repo and can be deployed together.

**FastAPI**

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**MCP Server** — update `BASE_URL` in your deployed `.env` to point to the deployed FastAPI URL, then:

```bash
python mcp_server/server.py
```

**Register with LiteLLM** — in your LiteLLM `config.yaml`, add:

```yaml
mcp_servers:
  - name: faq
    url: https://your-mcp-server.com/mcp
```

Or

You can use the LiteLLM UI.

## CLI Usage

```
uv run python cli.py
```

```
Available tools:
  1. faq-home_home_get — Returns a random fact about Me.
  2. faq-faq_faq_get  — Returns a list of frequently asked questions about Japan.

Pick a tool (number): 2

Using tool: faq-faq_faq_get  |  Type 'quit' to exit.

You: Do I need a visa to go to Japan?
Assistant: Based on the information available, **visa requirements for Japan depend on your nationality**:

**Citizens of about 68 countries** can enter Japan **visa-free for short stays**, typically up to **90 days**.

However, this varies by country, so I recommend checking the **Japanese Ministry of Foreign Affairs website** to confirm the specific requirements for your country of citizenship.

If your country isn't on the visa-free list, you'll need to apply for an appropriate visa before traveling to Japan.

You: quit
```

## Adding New Tools

1. Add a new route to `api/main.py`
2. Restart the MCP server — it auto-discovers routes from the OpenAPI spec or the `@mcp.tool` decorator
3. The new tool appears automatically in LiteLLM and the CLI
