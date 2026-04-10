# Flexible Deep Researcher

This version removes the hard requirement on Nebius.

## What to use

You need:
- `SGAI_API_KEY`
- one model key: `OPENROUTER_API_KEY` or `OPENAI_API_KEY` or `NEBIUS_API_KEY`

## Files added

- `providers.py`
- `agents_flexible.py`
- `.env.example`

## Recommended path

1. Copy `.env.example` to `.env`
2. Fill in `SGAI_API_KEY`
3. Fill in one model key. For most cases use `OPENROUTER_API_KEY`
4. Run the agent with Python using `agents_flexible.py`

## Example `.env`

```env
SGAI_API_KEY=your_scrapegraph_key
OPENROUTER_API_KEY=your_openrouter_key
MODEL_PROVIDER=auto
OPENROUTER_MODEL=openai/gpt-4o-mini
```

## Minimal test

Use the flexible agent module instead of the Nebius locked one.
