import json
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from main_free_local import monitor_product

load_dotenv()

TRACKED_URLS_FILE = os.getenv("PRICE_MONITOR_TRACKED_URLS_FILE", "tracked_urls_local.json")
CHECK_INTERVAL_MINUTES = int(os.getenv("PRICE_MONITOR_INTERVAL_MINUTES", "60"))


def load_tracked_urls() -> list[str]:
    if os.path.exists(TRACKED_URLS_FILE):
        try:
            with open(TRACKED_URLS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


def run_all() -> None:
    urls = load_tracked_urls()
    if not urls:
        print("No tracked URLs found.")
        return
    for url in urls:
        try:
            monitor_product(url)
        except Exception as e:
            print(f"Failed to monitor {url}: {e}")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_all, "interval", minutes=CHECK_INTERVAL_MINUTES)
    print(f"Scheduler started. Checking every {CHECK_INTERVAL_MINUTES} minutes.")
    run_all()
    scheduler.start()
