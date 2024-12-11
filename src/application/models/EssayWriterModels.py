from typing import List, TypedDict
from pydantic import BaseModel


class AgentState(TypedDict):
    task: str
    plan: str
    draft: str
    critique: str
    content: List[str]
    revision_number: int
    max_revisions: int


class Queries(BaseModel):
    # For generating this lists of queries to pass to Tavily,
    # we will use function calling to ensure we get back a list of strings from the language model
    # this pydantic model represents the result we want to get back from the language model
    queries: List[str]