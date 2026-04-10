# Free Local Deep Researcher

This is the free local path for Deep Researcher.

What changed:
- Removed the hard requirement on Nebius for this path.
- Replaced hosted search and paid reasoning with free local components.
- Uses DDGS for web search.
- Uses Trafilatura for article extraction.
- Uses Ollama for local reasoning.

## Files to use
- `agents_free_local.py`
- `requirements_free_local.txt`

## Setup

1. Install Ollama on your machine.
2. Pull a local model:
   - `ollama pull llama3.1:8b`
3. Install Python dependencies:
   - `uv pip install -r requirements_free_local.txt`
4. Optional `.env`:
   - `OLLAMA_MODEL=llama3.1:8b`
   - `SEARCH_RESULTS=5`

## Run

```bash
uv run python agents_free_local.py "What are the latest VCS methodology updates affecting agricultural carbon projects in South Asia?"
```

## Notes
- This free local version keeps the original paid files untouched.
- If you want the original paid path, keep using `agents.py`.
- If Ollama is not running locally, this free path will not work.
