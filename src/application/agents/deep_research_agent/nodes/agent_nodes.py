from typing import Dict

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
    filter_messages,
)
from typing_extensions import Literal

from src.application.agents.deep_research_agent.prompts.prompts import (
    compress_research_human_message,
    compress_research_system_prompt,
    research_agent_prompt,
)
from src.application.agents.deep_research_agent.states.researcher_state import (
    ResearcherState,
)


class DeepResearchNodes:
    def __init__(
        self,
        model_with_tools: BaseChatModel,
        tools_by_name: Dict,
        compress_model: BaseChatModel,
    ):
        self.model_with_tools = model_with_tools
        self.tools_by_name = tools_by_name
        self.compress_model = compress_model

    def llm_call(self, state: ResearcherState) -> dict:
        """
        Analyze current state and decide on next actions.

        The model analyzes current conversation state and decides whether to:
        1. Call search tools to gather more information
        2. Provide a final answer based on gathered information

        Returns updated state with the model's response
        """
        llm_call = {
            "researcher_messages": [
                self.model_with_tools.invoke(
                    [SystemMessage(content=research_agent_prompt)]
                    + state["researcher_messages"]
                )
            ]
        }

        return llm_call

    def tool_node(self, state: ResearcherState) -> dict:
        """
        Execute all tool calls from the previous LLM response.

        Executes all tool calls from the previous LLM reesponses.
        Returns updated state with tool execution results.
        """
        tool_calls = state["sesearcher_messages"][-1].tool_calls

        # Executes all tool calls
        observations = []
        for tool_call in tool_calls:
            tool = self.tools_by_name[tool_call["name"]]
            observations.append(tool.invoke(tool_call["args"]))

        # Create tool message outputs
        tool_outputs = [
            ToolMessage(
                content=observation,
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
            for observation, tool_call in zip(observations, tool_calls)
        ]

        return {"researcher_messages": tool_outputs}

    def compress_research(self, state: ResearcherState) -> dict:
        """
        Compress research findings into a concise summary.

        Takes all the research messages and tool outputs and creates
        a compressed summary suitable for tthe supervisor's decision-making.
        """
        system_message = compress_research_system_prompt.format(date=get_today_str())
        messages = (
            [SystemMessage(content=system_message)]
            + state.get("researcher_messages", [])
            + [HumanMessage(content=compress_research_human_message)]
        )

        response = self.compress_model.invoke(messages)

        # Extract rawa notes from tool and AI messages
        raw_notes = [
            str(m.content)
            for m in filter_messages(
                state["ressearcher_messages"], include_types=["tool", "ai"]
            )
        ]

        return {
            "compressed_research": str(response.content),
            "raw_notes": ["\n".join(raw_notes)],
        }

    def should_continue(
        self, state: ResearcherState
    ) -> Literal["tool_node", "compress_research"]:
        """
        Determine whether to continue research or provide final answer.

        Determines wheter the agent should continue the research loop or provide
        a final answer based on whether the LLM made tool calls.

        Returns:
            "tool_node": Continue to tool execution
            "compress_research": Stop and compress research
        """
        messages = state["researcher_messages"]
        last_message = messages[-1]

        if last_message.tool_calls:
            return "tool_node"

        return "compress_research"
