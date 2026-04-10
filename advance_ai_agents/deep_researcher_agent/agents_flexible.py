import os
from typing import Iterator

from agno.agent import Agent
from agno.tools.scrapegraph import ScrapeGraphTools
from agno.utils.log import logger
from agno.workflow import RunResponse, Workflow
from dotenv import load_dotenv

from providers import build_model

load_dotenv()

SCRAPEGRAPH_API_KEY = os.getenv("SGAI_API_KEY")
if not SCRAPEGRAPH_API_KEY:
    raise ValueError("SGAI_API_KEY is required for ScrapeGraph tools.")


class DeepResearcherAgentFlexible(Workflow):
    searcher: Agent = Agent(
        tools=[ScrapeGraphTools(api_key=SCRAPEGRAPH_API_KEY)],
        model=build_model(),
        show_tool_calls=True,
        markdown=True,
        description=(
            "You gather current, high quality, multi source information from the web."
        ),
        instructions=(
            "1. Search for recent and authoritative sources.\n"
            "2. Extract facts, statistics, and expert opinions.\n"
            "3. Cover multiple perspectives.\n"
            "4. Organize findings clearly.\n"
            "5. Include references only for real sources you actually found."
        ),
    )

    analyst: Agent = Agent(
        model=build_model(),
        markdown=True,
        description="You synthesize research findings into useful insights.",
        instructions=(
            "1. Identify themes, trends, and contradictions.\n"
            "2. Highlight the most important findings and implications.\n"
            "3. Keep only links that were actually found earlier.\n"
            "4. Never invent links or facts."
        ),
    )

    writer: Agent = Agent(
        model=build_model(),
        markdown=True,
        description="You write a clear report from the analyst summary.",
        instructions=(
            "1. Write a direct introduction.\n"
            "2. Organize findings into sections.\n"
            "3. Use bullets or tables when useful.\n"
            "4. End with short recommendations.\n"
            "5. Include references only when real links were passed in."
        ),
    )

    def run(self, topic: str) -> Iterator[RunResponse]:
        logger.info(f"Running flexible deep researcher agent for topic: {topic}")
        research_content = self.searcher.run(topic)
        analysis = self.analyst.run(research_content.content)
        report = self.writer.run(analysis.content, stream=True)
        yield from report


def run_research(query: str) -> str:
    agent = DeepResearcherAgentFlexible()
    final_report_iterator = agent.run(topic=query)
    full_report = ""
    for chunk in final_report_iterator:
        if chunk.content:
            full_report += chunk.content
    return full_report


if __name__ == "__main__":
    topic = "Research a current topic and summarize the results."
    response = run_research(topic)
    print(response)
