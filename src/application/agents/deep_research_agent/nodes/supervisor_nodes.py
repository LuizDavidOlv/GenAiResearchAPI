import asyncio

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (BaseMessage, HumanMessage, SystemMessage,
                                     ToolMessage, filter_messages)
from langgraph.graph import END
from langgraph.types import Command
from typing_extensions import Literal

from application.agents.deep_research_agent.research_agent import \
    DeepResearchAgent
from src.application.agents.deep_research_agent.prompts.prompts import \
    lead_researcher_prompt
from src.application.agents.deep_research_agent.states.supervisor_state import \
    SupervisorState
from src.application.agents.tools.think_tool import ThinkTool
from src.application.utils.date_util import get_today_str


class SupervisorNodes:
    def __init__(self, supervisor_model_with_tools: BaseChatModel):
        self.max_researcher_iterations = 6  # Calls to think_tool + ConductResearch
        self.max_concurrent_researchers = 3
        self.supervisor_model_with_tools = supervisor_model_with_tools
        self.think_tool = ThinkTool().think

    async def supervisor(
        self, state: SupervisorState
    ) -> Command[Literal["supervisor_tools"]]:
        """Coordinate research activities.

        Analyzes the the research brief and current progress to  decide:
        - What research topics need investigation
        - Wheter to conduct parallel research
        - When research is complete

        Args:
            state: Current supervisor state with messages and research progress

        Returns:
            Command to proceed to supervisor_tools node with updated state
        """

        supervisor_messages = state.get("supervisor_messages", [])

        # Prepare system message with current date and constraints
        system_message = lead_researcher_prompt.format(
            date=get_today_str(),
            max_concurrent_research_units=self.max_concurrent_researchers,
            max_researcher_iterations=self.max_researcher_iterations,
        )

        messages = [SystemMessage(content=system_message)] + supervisor_messages

        response = await self.supervisor_model_with_tools.ainvoke(messages)

        command = Command(
            goto="supervisor_tools",
            update={
                "supervisor_messages": [response],
                "research_iterations": state.get("research_iterations", 0) + 1,
            },
        )

        return command
    
    async def supervisor_tools(self, state: SupervisorState) -> Command[Literal["supervisor", "__end__"]]:
        """
        Excecute supervisor decisions = either conduct research or end the process.

        Handles:
        - Executing think_tool calls for strategic reflection
        - Launching parallel research agents for different topics
        - Aggregating research results
        - Determining when research is complete

        Args:
            state: Current supervisor state with messages and iteration count
        
        Returns:
            Command to continue supervision, end process, or handle errors
        """

        supervisor_messages = state.get("supervisor_messages", [])
        research_iterations = state.get("research_iterations", 0)
        most_recent_message = supervisor_messages[-1]

        # Initialize variables for single return pattern

        tool_messages = []
        all_raw_notes = []
        next_step = "supervisor" # Default next step
        should_end = False

        # Check exit criteria first
        exceeded_iterations = research_iterations >= self.max_researcher_iterations
        no_tool_calls = not most_recent_message.tool_calls
        research_complete = any(
            tool_call["name"] == "ResearchComplete"
            for tool_call in most_recent_message.tool_calls
        )

        if exceeded_iterations or no_tool_calls or research_complete:
            should_end = True
            next_step= EncodingWarning
        else:
            # Execute ALL tool calls before deciding next step
            try:
                think_tool_calls = [
                    tool_call for tool_call in most_recent_message.tool_calls
                    if tool_call["name"] == "think_tool"
                ]

                conduct_research_calls = [
                    tool_call for tool_call in most_recent_message.tool_calls
                    if tool_call=["name"] == "ConductResearch"
                ]
            
                # Handle think_tool calls (synchronous)
                for tool_call in think_tool_calls:
                    observation = self.think_tool.invoke(tool_call["args"])
                    tool_messages.append(
                        ToolMessage(
                            content=observation,
                            name=tool_call["name"],
                            tool_call_id=tool_call["id"]
                        )
                    )
                
                if conduct_research_calls:
                    # Launch parallel research agents
                    coros = [
                        DeepResearchAgent.ainvoke({
                            "researcher_messages": [
                                HumanMessage(content=tool_call["args"]["research_topic"])
                            ],
                            "research_topic": tool_call["args"]["research_topic"]
                        })
                        for tool_call in conduct_research_calls
                    ]

                    # Wait for call research to complete
                    tool_results = await asyncio.gather(*coros)

                    # Format research results as tool messages
                    # Each sub-agent returns compressed research findings in results["compressed_research"]
                    # We write this compressed research as the content of a ToolMessage, which allows
                    # the supervisor to later retrieve these findings via get_notes_from_tool_calls()

                    research_tool_messages = [
                        ToolMessage(
                            content=result.get("compressed_research", "Error synthesizing research report"),
                            name = tool_call["name"],
                            tool_call_id=tool_call=["id"]
                        ) for result, tool_call in zip(tool_results, conduct_research_calls)
                    ]

                    tool_messages.extend(research_tool_messages)

                    all_raw_notes = [
                        "\n".join(result.get("raw_notes",[]))
                        for result in tool_results
                    ]
            except:
                should_end= True
                next_step = END
        
        update = {
            "notes": self.get_notes_from_tool_calls(supervisor_messages),
            "research_brief": state.get("research_brief", "")
        }

        if should_end:
            update ={
                "supervisor_messages": tool_messages,
                "raw_notes": all_raw_notes
            }
        
        command = Command(goto=next_step, update=update)
        return command
        
    def get_notes_from_tool_calls(self, messages: list[BaseMessage]) -> list[str]:
        """
        Extract research notes from ToolMessage objects in supervisor message history.

        This function retrives the compressed research findings that sub-agents
        return as ToolMessage content. When the supervisor delegates research to
        sub-agents via ConductResearch tool calls, each sub-agent returns its
        compressed findings as the content of a ToolMessage. This function
        extracts all such ToolMessages content to compile the final reasearch notes.

        Args:
            messages: List of messages from supervisor's conversation history

        Returns:
            List of research note strings extracted from ToolMessage objects
        """

        content = [tool_msg.content for tool_msg in filter_messages(messages, include_types="tool")]
        return content
