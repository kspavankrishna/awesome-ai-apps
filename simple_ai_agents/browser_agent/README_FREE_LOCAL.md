# Free Local Browser Agent

This is the free local path for Browser Agent.

What changed:
- Replaced Nebius with a local Ollama model through the OpenAI-compatible Ollama endpoint.
- Kept the original paid files untouched.

## Files to use
- `main_free_local.py`
- `requirements_free_local.txt`

## Setup

1. Install Ollama.
2. Pull a local model:
   - `ollama pull llama3.1:8b`
3. Install browser and Python dependencies:
   - `uv pip install -r requirements_free_local.txt`
   - install Playwright/browser requirements needed by `browser-use` if your environment does not have them yet
4. Optional `.env`:
   - `OLLAMA_BASE_URL=http://localhost:11434/v1`
   - `OLLAMA_MODEL=llama3.1:8b`
   - `OLLAMA_API_KEY=ollama`

## Run

```bash
uv run python main_free_local.py
```

## Notes
- This free local path still needs a local browser environment because it uses `browser-use`.
- Use the original paid files only if you specifically want Nebius.
