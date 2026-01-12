"""
State Definitions and Pydantic Schemas for Research Agent

This module defines the state objects and structured schemas used for
the research agent workflow, including researcher state management and output schemas.
"""

import operator

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing_extensions import Annotated, List, Sequence, TypedDict


class ResearcherState(TypedDict):
    """
    State for the research agent containing message history and research metadata.

    This state tracks the researcher's conversation, interation count for limiting
    tool calls, the research topic being investigated, compressed findings,
    and raw search notes for detailed analysis.
    """

    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]
    tool_call_interations: int
    research_topic: str
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]


class ResearcherOutputState(TypedDict):
    """
    Output state for the research agent containing final research results.

    This represents the final output of the research process with compressed
    research findings and all raw notes from the research process.
    """

    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]


class Summary(BaseModel):
    """Schema for webpage content summarization."""

    summary: str = Field(description="Concise summary of the webpage content")
    key_excerpts: str = Field(
        description="Important quotes and excerpts from the content"
    )
