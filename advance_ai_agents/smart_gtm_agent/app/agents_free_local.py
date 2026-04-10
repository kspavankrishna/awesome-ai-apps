import os
import re
import sqlite3
from typing import Any, Dict, List

from ddgs import DDGS
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
import trafilatura

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
SEARCH_RESULTS = int(os.getenv("SEARCH_RESULTS", "6"))

llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)


def extract_company_name(url: str) -> str:
    match = re.search(r"https?://(?:www\.)?([^/]+)", url)
    name = match.group(1).replace("-", " ").replace(".com", "") if match else url
    return name.title()


def fetch_page_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    extracted = trafilatura.extract(downloaded, include_links=True, include_formatting=True)
    return extracted or ""


def search_company_context(company_name: str) -> List[dict]:
    queries = [
        f"{company_name} company overview funding competitors",
        f"{company_name} target market pricing business model competitors",
    ]
    results: List[dict] = []
    seen: set[str] = set()
    for query in queries:
        for item in DDGS().text(query, max_results=SEARCH_RESULTS):
            url = item.get("href") or item.get("url")
            if not url or url in seen:
                continue
            seen.add(url)
            text = fetch_page_text(url)
            if not text:
                continue
            results.append(
                {
                    "title": item.get("title", "Untitled"),
                    "url": url,
                    "body": text[:12000],
                }
            )
    return results


def summarize_company(url: str) -> str:
    page_text = fetch_page_text(url)
    company_name = extract_company_name(url)
    sources = search_company_context(company_name)
    prompt = (
        "You are a company research assistant. Use only the supplied website text and source snippets. "
        "Return markdown with sections: Company Overview, Funding and Financials, Industry and Market, Competitors, Market Signals, Assumptions and Gaps.\n\n"
        f"Primary URL: {url}\n\n"
        f"Website text:\n{page_text[:12000]}\n\n"
        f"External sources:\n{sources}"
    )
    return llm.invoke(prompt).content


def build_gtm_playbook(url: str) -> str:
    company_name = extract_company_name(url)
    sources = search_company_context(company_name)
    prompt = (
        "You are a GTM strategist. Use only the supplied source snippets. "
        "Return markdown with sections: Target Market, ICP, Messaging, Pricing Hypothesis, Distribution and Sales Strategy, Growth Channels, Metrics and KPIs, Risks and Gaps.\n\n"
        f"Company URL: {url}\n\n"
        f"Sources:\n{sources}"
    )
    return llm.invoke(prompt).content


def build_channel_strategy(url: str) -> str:
    company_name = extract_company_name(url)
    sources = search_company_context(company_name)
    prompt = (
        "You are a distribution and channel strategy expert. Use only the supplied source snippets. "
        "Return markdown with sections: Primary Channels, Digital Channels, Partnerships and Alliances, Emerging Channels, Channel Justification, Risks and Dependencies.\n\n"
        f"Company URL: {url}\n\n"
        f"Sources:\n{sources}"
    )
    return llm.invoke(prompt).content


def save_to_db(url: str, feature: str, content: str, db_path: str = "company_data.db") -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            feature TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute(
        "INSERT INTO reports (url, feature, content) VALUES (?, ?, ?)",
        (url, feature, content or "No content generated."),
    )
    conn.commit()
    conn.close()


def company_market_tool(url: str, feature: str = "research") -> str:
    if feature == "gtm":
        result = build_gtm_playbook(url)
    elif feature == "channel":
        result = build_channel_strategy(url)
    else:
        result = summarize_company(url)
    save_to_db(url, feature, result)
    return result


research_agent = create_react_agent(
    model=llm,
    tools=[company_market_tool],
    prompt="Always call company_market_tool first. Then present a concise, business-ready company research summary.",
)

gtm_agent = create_react_agent(
    model=llm,
    tools=[company_market_tool],
    prompt="Always call company_market_tool with feature='gtm' first. Then present a concise GTM playbook.",
)

channel_agent = create_react_agent(
    model=llm,
    tools=[company_market_tool],
    prompt="Always call company_market_tool with feature='channel' first. Then present a concise channel strategy.",
)


def report_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    return state
