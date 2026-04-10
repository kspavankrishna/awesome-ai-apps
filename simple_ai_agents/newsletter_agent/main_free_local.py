import argparse
import os
from datetime import datetime

from ddgs import DDGS
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import trafilatura

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
SEARCH_RESULTS = int(os.getenv("SEARCH_RESULTS", "5"))
llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)


def search_web(topic: str, max_results: int = SEARCH_RESULTS) -> list[dict]:
    return list(DDGS().text(topic, max_results=max_results) or [])


def fetch_page_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(downloaded, include_links=True, include_formatting=True) or ""


def gather_sources(topic: str, max_results: int = SEARCH_RESULTS) -> list[dict]:
    results = search_web(topic, max_results=max_results)
    sources: list[dict] = []
    for item in results:
        url = item.get("href") or item.get("url")
        if not url:
            continue
        body = fetch_page_text(url)
        if not body:
            continue
        sources.append(
            {
                "title": item.get("title", "Untitled"),
                "url": url,
                "snippet": item.get("body") or item.get("snippet") or "",
                "content": body[:12000],
            }
        )
    return sources


def generate_newsletter(topic: str, max_results: int = SEARCH_RESULTS) -> str:
    sources = gather_sources(topic, max_results=max_results)
    if not sources:
        return "No sources could be extracted. Try a more specific topic."

    prompt = (
        "You are a newsletter editor. Use only the supplied source list and content. "
        "Write a markdown newsletter with this exact structure: Title, Welcome, Main Story, Featured Content, Quick Updates, This Week's Highlights, Sources and Further Reading. "
        "Do not invent facts or links. Use only the real source URLs.\n\n"
        f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}\n"
        f"Topic: {topic}\n\n"
        f"Sources: {sources}"
    )
    return llm.invoke(prompt).content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("topic", nargs="*", help="Newsletter topic")
    parser.add_argument("--limit", type=int, default=SEARCH_RESULTS)
    args = parser.parse_args()
    topic = " ".join(args.topic).strip() or "Latest developments in AI"
    print(generate_newsletter(topic, max_results=args.limit))


if __name__ == "__main__":
    main()
