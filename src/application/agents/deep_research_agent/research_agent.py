from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START, StateGraph

from application.agents.deep_research_agent.nodes.research_agent_nodes import (
    ResearchAgentNodes,
)
from application.agents.tools.think_tool import ThinkTool
from src.application.agents.deep_research_agent.states.researcher_state import (
    ResearcherOutputState,
    ResearcherState,
)
from src.application.agents.tools.tavily_search_tool import TavilySearchTool


class ResearchAgent:
    def __init__(self):
        model = "anthropic:claude-sonnet-4-20250514"
        chat_model = init_chat_model(model=model)
        summarization_model = init_chat_model(model=model)
        compress_model = init_chat_model(model=model, max_tokens=64000)

        tavily_search_tool = TavilySearchTool(
            summarization_model=summarization_model
        ).tavily_search
        think_tool = ThinkTool().think
        tools = [tavily_search_tool, think_tool]

        tools_by_name = {tools.name: tool for tool in tools}

        chat_model_with_tools = chat_model.bind_tools(tools)

        nodes = ResearchAgentNodes(
            chat_model_with_tools=chat_model_with_tools,
            tools_by_name=tools_by_name,
            compress_model=compress_model,
        )

        builder = StateGraph(ResearcherState, output_schema=ResearcherOutputState)
        builder.add_node("llm_call", nodes.llm_call)
        builder.add_node("tool_node", nodes.tool_node)
        builder.add_node("compress_research", nodes.compress_research)

        builder.add_edge(START, "llm_call")
        builder.add_conditional_edges(
            "llm_call",
            nodes.should_continue,
            {
                "tools_node": "tool_node",  # Continue research loop
                "compress_research": "compress_research",  # Provide final answer
            },
        )

        builder.add_edge("tools_node", "llm_call")
        builder.add_edge("compressed_research", END)
        self.research_agent = builder.compile()

    def invoke_agent(self, research_brief: str):
        result = self.research_agent.invoke(
            {"researcher_messages": [HumanMessage(content=f"{research_brief}.")]}
        )

        return result
