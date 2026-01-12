from langchain_core.messages import HumanMessage
from langgraph.graph import START, StateGraph

from src.application.agents.deep_research_agent.nodes.supervisor_nodes import (
    SupervisorNodes,
)
from src.application.agents.deep_research_agent.states.supervisor_state import (
    SupervisorState,
)


class SupervisorAgent:
    def __init__(self):
        nodes = SupervisorNodes()
        builder = StateGraph(SupervisorState)
        builder.add_node("supervisor", nodes.supervisor)
        builder.add_node("supervisor_tools", nodes.supervisor_tools)
        builder.add_edge(START, "supervisor")
        self.supervisor_agent = builder.compile()

    async def ainvoke(self, research_brief: str):
        result = await self.supervisor_agent.ainvoke(
            {"supervisor_messages": [HumanMessage(content=f"{research_brief}.")]}
        )
        return result
