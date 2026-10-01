# PrayerTimes MCP

This project provides a local FastAPI API and a real MCP server for fetching prayer times from the public Aladhan API.

## What is included

- FastAPI application with Swagger docs
- Local REST endpoints for health and prayer times
- Real MCP tool named `get_prayer_times`
- VS Code / Copilot compatible config for local MCP integration
- Ready-to-use local testing flow before cloud deployment

## Project structure

- `app/main.py` — FastAPI app
- `app/client.py` — external API client
- `app/config.py` — app settings
- `app/schemas.py` — request/response models
- `prayer_times_mcp_server.py` — MCP server exposing the prayer-times tool
- `.vscode/mcp.json` — local MCP server config for VS Code
- `requirements.txt` — Python dependencies

## Local FastAPI API

### Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Then open:

- http://localhost:8001/docs
- http://localhost:8001/health
- http://localhost:8001/prayer-times?city=Casablanca&country=Morocco

### Example REST call

```bash
curl -X GET "http://localhost:8001/prayer-times?city=Casablanca&country=Morocco"
```

## Local MCP server

The real MCP server is in `prayer_times_mcp_server.py`.

It exposes a tool called `get_prayer_times`.

### Run the MCP server

```bash
cd /home/olachgar/Projects/MCPs/PrayerTimes
source .venv/bin/activate
python prayer_times_mcp_server.py
```

This runs in stdio mode, which is the correct setup for local AI clients such as VS Code / Copilot.

## VS Code / Copilot integration

The repository includes a ready-to-use config file at `.vscode/mcp.json`:

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

After reloading VS Code / Copilot, you can ask the assistant to call the `prayer-times` MCP tool, for example:

- “Use the prayer-times MCP tool to get prayer times for Casablanca, Morocco”
- “Get the Dhuhr time for Paris, France”

## Example tool call

The tool can be called with:

```python
get_prayer_times(city="Casablanca", country="Morocco")
```

Optional parameters:

```python
get_prayer_times(city="Paris", country="France", method=2, date="2026-10-01")
```

## Public MCP deployment on Render

For a public MCP that anyone can use, the project now includes a Render-ready HTTP server: `public_mcp_server.py`.

This version is designed for hosted public access, not the local stdio server.

### Public server entrypoints

- `/mcp` — MCP streamable HTTP endpoint
- `/sse` — SSE endpoint for compatible clients
- `/health` — health check
- `/` — basic service info

### Render configuration

The repository includes a `render.yaml` file:

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

### Render deployment steps

1. Push the repo to GitHub
2. Create a new Render Web Service
3. Connect the GitHub repository
4. Choose the repo and service type: Web Service
5. Use the default Python runtime
6. Set the start command to:

```bash
uvicorn public_mcp_server:app --host 0.0.0.0 --port $PORT
```

7. Deploy the service

After deployment, your public MCP base URL will look like:

```text
https://your-render-app.onrender.com/mcp
```

### Public MCP client config

A public MCP client should use the URL-based connection, not the local stdio command. Example:

```json
{
  "mcpServers": {
    "prayer-times": {
      "url": "https://your-render-app.onrender.com/mcp"
    }
  }
}
```

### Local and public usage

- Local AI tools: use `prayer_times_mcp_server.py` with stdio
- Public AI clients: use `public_mcp_server.py` with HTTP endpoint on Render

## Deployment notes

Render is the simplest free hosting path for a basic public MCP service. It avoids the trial-based pricing model of Railway and keeps the deployment straightforward for a Python/FastAPI service.

## Notes

The service relies on the public Aladhan API for prayer time data. The project is intended as a lightweight public MCP prototype and can be extended with additional prayer-related tools or richer metadata later.
