import os

from agno.models.nebius import Nebius
from agno.models.openai import OpenAIChat
from agno.models.openrouter import OpenRouter


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def _pick_provider() -> str:
    explicit = _clean(os.getenv("MODEL_PROVIDER", "auto"))
    if explicit and explicit.lower() != "auto":
        return explicit.lower()

    if _clean(os.getenv("OPENROUTER_API_KEY")):
        return "openrouter"
    if _clean(os.getenv("OPENAI_API_KEY")):
        return "openai"
    if _clean(os.getenv("NEBIUS_API_KEY")):
        return "nebius"

    raise ValueError(
        "No model provider key found. Set OPENROUTER_API_KEY, OPENAI_API_KEY, or NEBIUS_API_KEY."
    )


def build_model():
    provider = _pick_provider()

    if provider == "openrouter":
        return OpenRouter(
            id=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            api_key=_clean(os.getenv("OPENROUTER_API_KEY")),
        )

    if provider == "openai":
        return OpenAIChat(
            id=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=_clean(os.getenv("OPENAI_API_KEY")),
        )

    if provider == "nebius":
        return Nebius(
            id=os.getenv("NEBIUS_MODEL", "deepseek-ai/DeepSeek-V3-0324"),
            api_key=_clean(os.getenv("NEBIUS_API_KEY")),
        )

    raise ValueError(
        f"Unsupported MODEL_PROVIDER '{provider}'. Use openrouter, openai, nebius, or auto."
    )
