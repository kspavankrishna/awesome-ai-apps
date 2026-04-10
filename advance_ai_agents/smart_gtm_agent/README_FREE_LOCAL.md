# Free Local Smart GTM Agent

This is the free local path for Smart GTM Agent.

What changed:
- Replaced SmartCrawler and SearchScraper with DDGS plus direct page extraction.
- Replaced Nebius with a local Ollama model.
- Kept the original paid files untouched.

## Files to use
- `app/agents_free_local.py`
- `requirements_free_local.txt`

## Setup

1. Install Ollama.
2. Pull a local model:
   - `ollama pull llama3.1:8b`
3. Install Python dependencies:
   - `uv pip install -r requirements_free_local.txt`
4. Optional `.env`:
   - `OLLAMA_MODEL=llama3.1:8b`
   - `SEARCH_RESULTS=6`

## What you lose
- No hosted SmartCrawler polling.
- No hosted SearchScraper enrichment.

## What you gain
- No paid API requirement.
- Local model control.
- A simpler stack that is easier to run and debug.

## Run
Use the free local agent module instead of the original paid one.
