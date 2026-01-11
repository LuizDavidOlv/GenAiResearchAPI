import os

from dotenv import load_dotenv


class EnvironmentVariables:
    LANGSMITH_API_KEY: str = os.environ.get("LANGSMITH_API_KEY")
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY")
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY")

    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_PROJECT"] = "deep_research_from_scratch"
