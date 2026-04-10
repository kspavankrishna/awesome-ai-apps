# Free Local Newsletter Agent

This is the free local path for Newsletter Agent.

What changed:
- Replaced Firecrawl with DDGS search plus direct page extraction.
- Replaced Nebius with a local Ollama model.
- Kept the original paid files untouched.

## Files to use
- `main_free_local.py`
- `requirements_free_local.txt`

## Setup

1. Install Ollama.
2. Pull a local model:
   - `ollama pull llama3.1:8b`
3. Install Python dependencies:
   - `uv pip install -r requirements_free_local.txt`
4. Optional `.env`:
   - `OLLAMA_MODEL=llama3.1:8b`
   - `SEARCH_RESULTS=5`

## Run

```bash
uv run python main_free_local.py "Latest developments in AI"
```

## Notes
- This path uses free search and local reasoning.
- It is simpler than the original Firecrawl plus Nebius version.
- Use the original paid files only if you specifically want those providers.
