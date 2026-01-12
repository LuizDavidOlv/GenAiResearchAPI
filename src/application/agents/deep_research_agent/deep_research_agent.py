from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from application.agents.deep_research_agent.nodes.scope_nodes import ScopeNodes
from application.agents.deep_research_agent.states.deep_researcher_state import (
    AgentInputState,
    AgentState,
)
from application.agents.deep_research_agent.supervisor_agent import SupervisorAgent


class DeepResearchAgent:
    def __init__(self):
        builder = StateGraph(AgentState, input_schema=AgentInputState)
        scope_model = ""
        scope_nodes = ScopeNodes(llm_model=scope_model)
        supervisor_agent = SupervisorAgent()

        builder.add_node("clarify_with_user", scope_nodes.clarify_with_user)
        builder.add_node("write_research_brief", scope_nodes.write_research_brief)
        builder.add_node("supervisor_subgraph", supervisor_agent)
        builder.add_node("final_report_reneration", scope_nodes.final_report_generation)

        builder.add_edge(START, "clarify_with_user")
        builder.add_edge("write_research_brief", "suupervisor_subgraph")
        builder.add_edge("supervisor_subgraph", "final_report_generation")
        builder.add_edge("final_report_generation", END)

        self.deep_research_agent = builder.compile()

    async def ainvoke_agent(self, research_brief: str):
        thread = {"configurable": {"thread_id": "1", "recursion_limit": 50}}
        result = await self.deep_research_agent.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Yes the specific Deep Research products.")
                ]
            },
            config=thread,
        )
        return result
