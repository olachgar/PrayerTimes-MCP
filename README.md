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

## Deployment notes

This app is ready to be deployed to a free cloud platform such as Render or Railway after local validation.

Typical production steps:

1. Add environment variables if needed
2. Run the app on `0.0.0.0` and expose the internal port
3. Choose a provider that supports Python/FastAPI services
4. Keep using the same app entrypoint: `app.main:app`

## Notes

The service relies on the public Aladhan API for prayer time data. It is intended as a light local prototype and can be extended with more tools and a more formal MCP server configuration later.
