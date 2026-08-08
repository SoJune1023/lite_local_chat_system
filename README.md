# Lite local chat system

[English | [한국어](./README.ko.md)]

A clean chat program using Ollama without over-engineering.  
Developed without vibe-coding. Total working time: 2 hours.  

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.com/)
- [Tavily API Key](https://app.tavily.com/)

## How to use

```bash
uv sync
```

**Windows (PowerShell):**

```bash
uv run python -m src
```

```bash
uv run python -m src.cli
```

**macOS / Linux:**

```bash
uv run python3 -m src
```

```bash
uv run python3 -m src.cli
```

## Why JSON DB ?

I thought it was unnecessary to run a psql instance for this. I was a bit annoyed too, though...  
In the end, it might have been more convenient to apply psql. I might replace it with psql later.

## Project Structure

```planetext
src/
├── __main__.py               # FastAPI app, uvicorn
├── cli.py                    # httpx + rich CLI client
├── routers/interaction.py    # POST /interaction endpoint
├── handlers/interaction.py   # Request handling logic
├── services/
│   ├── history_loader.py     # Reading history from a JSON file
│   ├── history_saver.py      # Add a new turn and save
│   ├── prompt_loader.py      # Reading prompt from a txt file
│   └── response_maker.py     # Calling Ollama AsyncClient
└── schemas/                  # Schemas
```
