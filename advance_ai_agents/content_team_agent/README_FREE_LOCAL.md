# Free Local Content Team Agent

This is the free local path for Content Team Agent.

What changed:
- Replaced Nebius with a local Ollama model.
- Replaced SerpAPI based research with DDGS search.
- Kept Trafilatura for URL text extraction.
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
   - `SEARCH_RESULTS=8`

## Run topic mode

```bash
uv run python main_free_local.py --topic "carbon market outlook for 2026"
```

## Run URL optimization mode

```bash
uv run python main_free_local.py --url "https://example.com/article"
```

## Run pasted article mode

```bash
uv run python main_free_local.py --title "My Article" --content "paste the article text here"
```

## Notes
- This path is simpler than the original workflow.
- It is meant to remove paid blockers first.
- Use the original paid files only if you specifically want Nebius and SerpAPI.
