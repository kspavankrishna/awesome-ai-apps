# Free Local Price Monitoring Agent

This is the free local path for Price Monitoring Agent.

What changed:
- Replaced ScrapeGraph scraping with direct page extraction using Trafilatura.
- Replaced Nebius with a local Ollama model for product field extraction.
- Replaced Twilio alerts with free local console and log file alerts.
- Kept the original paid files untouched.

## Files to use
- `main_free_local.py`
- `scheduler_free_local.py`
- `requirements_free_local.txt`

## Setup

1. Install Ollama.
2. Pull a local model:
   - `ollama pull llama3.1:8b`
3. Install Python dependencies:
   - `uv pip install -r requirements_free_local.txt`
4. Optional `.env` values:
   - `OLLAMA_MODEL=llama3.1:8b`
   - `PRICE_MONITOR_DATA_FILE=product_data_local.json`
   - `PRICE_MONITOR_ALERT_LOG=alerts_local.log`
   - `PRICE_MONITOR_TRACKED_URLS_FILE=tracked_urls_local.json`
   - `PRICE_MONITOR_INTERVAL_MINUTES=60`

## Run one product check

```bash
uv run python main_free_local.py "https://example.com/product-page"
```

## Run the scheduler

1. Create `tracked_urls_local.json` as a JSON list of product URLs.
2. Run:

```bash
uv run python scheduler_free_local.py
```

## Notes
- This free path uses local alerts written to `alerts_local.log` and printed to the console.
- This is simpler than the original ScrapeGraph plus Nebius plus Twilio workflow.
- Some JavaScript-heavy product pages may extract poorly with the free path.
