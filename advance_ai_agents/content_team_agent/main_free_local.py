import argparse
import os
from typing import Optional

from ddgs import DDGS
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import trafilatura

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
SEARCH_RESULTS = int(os.getenv("SEARCH_RESULTS", "8"))
llm = ChatOllama(model=OLLAMA_MODEL, temperature=0)


def search_web(query: str, max_results: int = SEARCH_RESULTS) -> list[dict]:
    return list(DDGS().text(query, max_results=max_results) or [])


def extract_text_from_url(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(downloaded, include_links=True, include_formatting=True) or ""


def analyze_serp(topic: str) -> str:
    results = search_web(topic)
    prompt = (
        "You are an SEO research analyst. Use only the supplied search results. "
        "Return markdown with sections: Primary Keywords, Related Keywords, Related Questions, Search Intent, Competitor Patterns, Suggested Angle.\n\n"
        f"Topic: {topic}\n\nResults: {results}"
    )
    return llm.invoke(prompt).content


def generate_content_brief(topic: str, serp_analysis: str) -> str:
    prompt = (
        "You are a content strategist. Use the supplied SEO analysis to create a practical content brief. "
        "Return markdown with sections: Target Intent, Outline, Recommended Headings, FAQ Ideas, Entities to Mention, Writing Guidelines, Internal Link Ideas.\n\n"
        f"Topic: {topic}\n\nSEO Analysis:\n{serp_analysis}"
    )
    return llm.invoke(prompt).content


def audit_article(title: str, content: str, serp_analysis: str) -> str:
    prompt = (
        "You are an SEO editor. Use only the article and SEO analysis. "
        "Return markdown with sections: Strengths, Gaps, Keyword Opportunities, Structure Improvements, E-E-A-T Notes, Prioritized Fixes.\n\n"
        f"Title: {title}\n\nArticle:\n{content[:14000]}\n\nSEO Analysis:\n{serp_analysis}"
    )
    return llm.invoke(prompt).content


def optimize_sections(title: str, content: str, audit: str, serp_analysis: str) -> str:
    prompt = (
        "You are an SEO editor. Rewrite only the highest impact sections. "
        "Keep meaning intact. Return markdown with sections: Improved Sections, Why These Changes Help, Keyword Integration Notes.\n\n"
        f"Title: {title}\n\nArticle:\n{content[:14000]}\n\nAudit:\n{audit}\n\nSEO Analysis:\n{serp_analysis}"
    )
    return llm.invoke(prompt).content


def run_topic_mode(topic: str) -> str:
    serp_analysis = analyze_serp(topic)
    brief = generate_content_brief(topic, serp_analysis)
    return f"# Search Insights\n\n{serp_analysis}\n\n# Content Brief\n\n{brief}"


def run_article_mode(title: str, content: str) -> str:
    topic = title or "article optimization"
    serp_analysis = analyze_serp(topic)
    audit = audit_article(title, content, serp_analysis)
    edits = optimize_sections(title, content, audit, serp_analysis)
    return f"# Search Insights\n\n{serp_analysis}\n\n# Article Audit\n\n{audit}\n\n# Section Edits\n\n{edits}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default=None)
    parser.add_argument("--url", type=str, default=None)
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--content", type=str, default=None)
    args = parser.parse_args()

    if args.url:
        content = extract_text_from_url(args.url)
        title = args.title or args.url
        print(run_article_mode(title, content))
        return

    if args.title and args.content:
        print(run_article_mode(args.title, args.content))
        return

    topic = args.topic or "How to improve SEO content for AI search results"
    print(run_topic_mode(topic))


if __name__ == "__main__":
    main()
