import asyncio
import os

from dotenv import load_dotenv
from browser_use.llm import ChatOpenAI
from browser_use import Agent

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")


async def run_search(task: str | None = None):
    agent = Agent(
        task=(
            task
            or "Go to flipkart.com, search for laptop, sort by best rating, and give me the price of the first result in markdown"
        ),
        llm=ChatOpenAI(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL,
            api_key=OLLAMA_API_KEY,
        ),
        use_vision=False,
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(run_search())
