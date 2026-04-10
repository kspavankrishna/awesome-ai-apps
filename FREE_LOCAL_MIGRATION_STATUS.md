# Free Local Migration Status

This repository contains many apps that currently depend on paid APIs or hosted tools.

Instead of breaking the original versions, this migration adds parallel `*_free_local.py` files and `README_FREE*.md` guides where a practical free replacement exists.

## Free stack policy

Preferred replacements:
- Hosted paid LLMs -> local Ollama models
- Paid web search APIs -> DDGS
- Paid page extraction APIs -> Trafilatura or direct requests parsing

## Current status

Completed in this pass:
- `advance_ai_agents/deep_researcher_agent` free-local path added
- `advance_ai_agents/smart_gtm_agent` free-local path added

Notes:
- Original paid versions are intentionally left untouched.
- Use the new free-local files and README guides first.
- Repo-wide full migration is large and should be done app by app to avoid breaking assumptions.
