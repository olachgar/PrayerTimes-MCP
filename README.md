# PrayerTimes MCP

A production-ready local and public MCP for fetching prayer times from the Aladhan API.

## Overview

This project is designed with a clean two-layer architecture:

- Local MCP: for IDEs like VS Code / Copilot
- Public MCP: for remote AI clients over HTTP, hosted on Render
- FastAPI REST API: for local testing and debugging

This gives you a professional setup for both local development and public deployment.

## Architecture

### 1) Local development MCP

File: `prayer_times_mcp_server.py`

Purpose:
- local tool exposure for a machine running an AI assistant
- uses stdio transport
- ideal for VS Code / Copilot / local MCP clients

### 2) Public Render MCP

File: `public_mcp_server.py`

Purpose:
- internet-facing MCP server
- uses streamable HTTP / SSE transport
- ready for deployment on Render

### 3) REST API

File: `app/main.py`

Purpose:
- human-readable HTTP endpoints
- local testing and debugging
- easy health checks and manual API consumption

## Features

- FastAPI app with Swagger docs
- Prayer time retrieval from Aladhan
- Local stdio MCP server
- Public HTTP MCP server for deployment
- Render-ready config
- Health checks and simple API validation

## Project structure

```text
PrayerTimes-MCP/
├── app/
│   ├── __init__.py
│   ├── client.py
│   ├── config.py
│   ├── main.py
│   └── schemas.py
├── .vscode/
│   └── mcp.json
├── .env.example
├── .gitignore
├── prayer_times_mcp_server.py
├── public_mcp_server.py
├── render.yaml
├── requirements.txt
├── README.md
└── .venv/
```

## Local setup

### 1) Create and activate the virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the FastAPI REST API locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Endpoints:

- http://localhost:8001/health
- http://localhost:8001/docs
- http://localhost:8001/prayer-times?city=Casablanca&country=Morocco

### 3) Run the local MCP server

```bash
python prayer_times_mcp_server.py
```

This starts the tool in stdio mode for local AI clients.

## VS Code / Copilot local MCP config

The project contains a ready config file at `.vscode/mcp.json`:

```json
{
  "servers": {
    "prayer-times": {
      "type": "stdio",
      "command": "/home/olachgar/Projects/MCPs/PrayerTimes/.venv/bin/python",
      "args": [
        "/home/olachgar/Projects/MCPs/PrayerTimes/prayer_times_mcp_server.py"
      ],
      "cwd": "/home/olachgar/Projects/MCPs/PrayerTimes"
    }
  }
}
```

After reloading VS Code / Copilot, you can ask the assistant to call the MCP tool, for example:

- “Use the prayer-times MCP tool to get prayer times for Casablanca, Morocco”
- “Get the Dhuhr time for Paris, France”

## MCP tool contract

The local MCP tool is named:

```python
get_prayer_times(city: str, country: str, method: int | None = None, date: str | None = None)
```

Example:

```python
get_prayer_times(city="Casablanca", country="Morocco")
```

## Public MCP server for Render

The public server is in `public_mcp_server.py`.

It exposes HTTP endpoints:

- `/mcp` — public MCP endpoint
- `/sse` — SSE endpoint for compatible clients
- `/health` — health check
- `/` — info route

### Public server startup command

```bash
uvicorn public_mcp_server:app --host 0.0.0.0 --port $PORT
```

This is the command Render should use.

## Render deployment checklist

Follow these steps to deploy the public MCP to Render.

### Checklist

1. Push this repository to GitHub.
2. Sign in to Render.
3. Click New + → Web Service.
4. Connect the GitHub repository `olachgar/PrayerTimes-MCP`.
5. Keep the repository branch as `main`.
6. Use the default Python environment.
7. Set the build command:

```bash
pip install -r requirements.txt
```

8. Set the start command:

```bash
uvicorn public_mcp_server:app --host 0.0.0.0 --port $PORT
```

9. Pick the free plan.
10. Click Create Web Service.
11. Wait for startup and check the health endpoint.
12. Confirm the public MCP URL is reachable.

### Render URL shape

```text
https://your-app-name.onrender.com/mcp/
```

### Example public MCP client config

```json
{
  "mcpServers": {
    "prayer-times": {
      "url": "https://your-app-name.onrender.com/mcp/"
    }
  }
}
```

## Render config file

The repo includes a ready `render.yaml`:

```yaml
services:
  - type: web
    name: prayer-times-public-mcp
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn public_mcp_server:app --host 0.0.0.0 --port $PORT
    autoDeploy: true
```

## Production recommendation

For a production-ready setup:

- Use `prayer_times_mcp_server.py` for local machine assistants
- Use `public_mcp_server.py` for remote/public AI clients
- Deploy the public version on Render
- Keep the REST API for debugging and manual validation

This is the cleanest architecture for a public MCP service while retaining local developer ergonomics.

## Notes

- The project relies on the public Aladhan API for prayer time data.
- Local stdio MCP is intended for local AI client usage.
- Public HTTP MCP is intended for remote/public deployment.
- No GitHub Actions are required for Render deployment — Render can deploy directly from GitHub.
