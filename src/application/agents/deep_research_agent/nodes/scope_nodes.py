from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langgraph.graph import END
from langgraph.types import Command
from typing_extensions import Literal

from application.agents.deep_research_agent.states.deep_researcher_state import (
    AgentState,
)
from application.utils.date_util import get_today_str
from src.application.agents.deep_research_agent.prompts.scope_prompts import (
    CLARIFICATION_PROMPT,
    FINAL_REPORT_PROMPT,
    RESEARCH_SUMMARIZATION_PROMPT,
)
from src.application.agents.deep_research_agent.states.scope_state import (
    ClarificationState,
    ResearchQuestion,
)


class ScopeNodes:
    def __init__(self, llm_model: BaseChatModel, writer_model: BaseChatModel):
        self.llm_model = llm_model
        self.writer_model = writer_model

    def clarify_with_user(
        self, state: AgentState
    ) -> Command[Literal["write_research_brief", "__end__"]]:
        """
        Determine if the user's request contains sufficient information to proceed with research.

        Uses structured output to make determininistic decisions and avoid hallucination
        Routes to either research brief generation or ends with a clarification question
        """

        structured_output_model = self.llm_model.with_structured_output(
            ClarificationState
        )

        response: ClarificationState = structured_output_model.invoke(
            [
                HumanMessage(
                    content=CLARIFICATION_PROMPT.format(
                        messages=get_buffer_string(messages=state["messages"]),
                        date=get_today_str(),
                    )
                )
            ]
        )

        if response.need_clarification:
            return Command(
                goto=END, update={"messages": [AIMessage(content=response.question)]}
            )
        else:
            return Command(
                goto="write_research_brief",
                update={"messages": [AIMessage(content=response.verification)]},
            )

    def write_research_brief(self, state: AgentState):
        """
        Tranform the conversation history into a comprehensive research brief

        uses structured output to ensure the brief gollows the required format
        and contains all necessary details for effective research
        """

        structured_output_model = self.llm_model.with_structured_output(
            ResearchQuestion
        )

        response: ResearchQuestion = structured_output_model.invoke(
            [
                HumanMessage(
                    content=RESEARCH_SUMMARIZATION_PROMPT.format(
                        messages=get_buffer_string(state.get("messages", [])),
                        date=get_today_str(),
                    )
                )
            ]
        )

        # update state with generated research brief and pass it to the supervisor

        return {
            "research_brief": response.research_brief,
            "supervisor_messages": [
                HumanMessage(content=f"{response.research_brief}.")
            ],
        }

    async def final_report_generation(self, state: AgentState):
        """
        Final report generation node

        Synthesizes all research findings into a comprhensive final report
        """

        notes = state.get("notes", [])

        findings = "\n".join(notes)

        final_report_prompt = FINAL_REPORT_PROMPT.format(
            research_brief=state.get("research_brief", ""),
            findings=findings,
            date=get_today_str(),
        )

        final_report = await self.writer_model.ainvoke(
            [HumanMessage(content=final_report_prompt)]
        )

        return {
            "final_report": final_report.content,
            "messages": ["Here is the final report: " + final_report.content],
        }
