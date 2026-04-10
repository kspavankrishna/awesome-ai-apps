import argparse
import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import trafilatura

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
DATA_FILE = os.getenv("PRICE_MONITOR_DATA_FILE", "product_data_local.json")
ALERT_LOG = os.getenv("PRICE_MONITOR_ALERT_LOG", "alerts_local.log")

llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)


def load_json(path: str, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default


def save_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch_page_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(downloaded, include_links=True, include_formatting=True) or ""


def fallback_price(text: str) -> str:
    patterns = [
        r"₹\s?[0-9][0-9,]*(?:\.[0-9]{1,2})?",
        r"Rs\.?\s?[0-9][0-9,]*(?:\.[0-9]{1,2})?",
        r"\$\s?[0-9][0-9,]*(?:\.[0-9]{1,2})?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return "N/A"


def fallback_availability(text: str) -> str:
    lowered = text.lower()
    if "out of stock" in lowered or "unavailable" in lowered:
        return "Out of Stock"
    if "in stock" in lowered or "available" in lowered:
        return "In Stock"
    return "Unknown"


def parse_product(url: str, text: str) -> dict:
    if not text:
        return {
            "url": url,
            "title": "N/A",
            "current_price": "N/A",
            "availability": "Unknown",
            "rating": "N/A",
            "source": "local_free_path",
            "checked_at": datetime.utcnow().isoformat(),
        }

    prompt = (
        "Extract product information from the text below. Return strict JSON only with keys: "
        "title, current_price, availability, rating. Use strings for all values. If missing, use 'N/A' or 'Unknown'.\n\n"
        f"URL: {url}\n\n"
        f"TEXT:\n{text[:12000]}"
    )

    try:
        raw = llm.invoke(prompt).content.strip()
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            data = json.loads(raw[start:end + 1])
        else:
            raise ValueError("No JSON object found in model output")
    except Exception:
        data = {
            "title": text.splitlines()[0][:120] if text.splitlines() else "N/A",
            "current_price": fallback_price(text),
            "availability": fallback_availability(text),
            "rating": "N/A",
        }

    data["url"] = url
    data["source"] = "local_free_path"
    data["checked_at"] = datetime.utcnow().isoformat()
    return data


def is_significant_change(old_data: dict | None, new_data: dict) -> bool:
    if not old_data:
        return True
    return (
        old_data.get("current_price") != new_data.get("current_price")
        or old_data.get("availability") != new_data.get("availability")
    )


def generate_message(data: dict) -> str:
    return (
        f"{data.get('title', 'Unknown Product')} is now {data.get('availability', 'Unknown')} "
        f"at price {data.get('current_price', 'N/A')}. Rating: {data.get('rating', 'N/A')}"
    )


def log_alert(message: str) -> None:
    line = f"[{datetime.utcnow().isoformat()}] {message}\n"
    with open(ALERT_LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(message)


def monitor_product(url: str) -> dict:
    all_previous_data = load_json(DATA_FILE, {})
    previous_data = all_previous_data.get(url)

    text = fetch_page_text(url)
    scraped_data = parse_product(url, text)

    if is_significant_change(previous_data, scraped_data):
        log_alert(generate_message(scraped_data))

    all_previous_data[url] = scraped_data
    save_json(DATA_FILE, all_previous_data)
    return scraped_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Product URL to monitor")
    args = parser.parse_args()
    result = monitor_product(args.url)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
