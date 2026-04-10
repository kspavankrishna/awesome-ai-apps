import argparse
import json
import os
from typing import Iterable

from ddgs import DDGS
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import trafilatura

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
SEARCH_RESULTS = int(os.getenv("SEARCH_RESULTS", "5"))


def get_llm() -> ChatOllama:
    return ChatOllama(model=OLLAMA_MODEL, temperature=0)


def search_web(query: str, max_results: int = SEARCH_RESULTS) -> list[dict]:
    results = DDGS().text(query, max_results=max_results)
    return list(results or [])


def fetch_page_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    extracted = trafilatura.extract(downloaded, include_links=True, include_formatting=True)
    return extracted or ""


def collect_sources(query: str) -> list[dict]:
    search_results = search_web(query)
    sources: list[dict] = []
    for item in search_results:
        url = item.get("href") or item.get("url")
        if not url:
            continue
        text = fetch_page_text(url)
        if not text:
            continue
        sources.append(
            {
                "title": item.get("title", "Untitled"),
                "url": url,
                "body": text[:12000],
            }
        )
    return sources


def build_report(query: str, sources: list[dict]) -> str:
    llm = get_llm()
    payload = json.dumps(sources, ensure_ascii=False, indent=2)
    prompt = (
        "You are a careful research analyst. Use only the provided sources. "
        "Write a structured report with an introduction, key findings, disagreements or gaps, "
        "and a references section using the real URLs from the source list.\n\n"
        f"Research question: {query}\n\n"
        f"Sources:\n{payload}"
    )
    return llm.invoke(prompt).content


def run_research(query: str) -> str:
    sources = collect_sources(query)
    if not sources:
        return "No sources could be extracted. Try a more specific query or check your network access."
    return build_report(query, sources)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="*", help="Research question")
    args = parser.parse_args()
    query = " ".join(args.query).strip() or "What are the latest developments in the voluntary carbon market?"
    print(run_research(query))


if __name__ == "__main__":
    main()
