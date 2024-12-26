from dataclasses import dataclass, fields
import os
from typing import Any, Optional
from langchain_core.runnables import RunnableConfig

from src.application.prompts.configuration_prompts import DEFAULT_REPORT_STRUCTURE


@dataclass(kw_only=True)
class Configuration:
    """The configuration fields for the chatbot """
    report_structure: str = DEFAULT_REPORT_STRUCTURE
    number_of_queries: int =2
    tavily_topic: str = "general"
    tavily_days: str = None

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None) -> "Configuration":
        configurable = (config["configurable"] if config and "configurable" in config else {})
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name)) 
            for f in fields(cls)
            if f.init
            }
        return cls(**{k: v for k, v in values.items() if v})


