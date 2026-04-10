# Free Local Chat

This is the free local path for Nebius Chat.

What changed:
- Replaced Nebius with a local Ollama model.
- Removed hosted image generation from this path.
- Kept the original paid files untouched.

## Files to use
- `app_free_local.py`
- `requirements_free_local.txt`

## Setup

1. Install Ollama.
2. Pull one or more local models:
   - `ollama pull llama3.1:8b`
   - `ollama pull qwen2.5:7b`
   - `ollama pull phi4:mini`
3. Install Python dependencies:
   - `uv pip install -r requirements_free_local.txt`

## Run

```bash
uv run streamlit run app_free_local.py
```

## Notes
- This path is chat only.
- Image generation is not included in the free local replacement.
- Use the original paid app only if you specifically want Nebius hosted chat and image generation.
