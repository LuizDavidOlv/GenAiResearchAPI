from unittest.mock import MagicMock, patch
import pytest

from src.application.agents.research_agent import ResearchAgent



@pytest.mark.asyncio
async def test_research_agent():
    #create an instance of the agent
    agent = ResearchAgent(model=MagicMock())

    with patch.object(agent, "structured_llm") as mock_structured_llm:

        mock_structured_llm.invoke.return_value= [ {"mock_section": "This is a mocked section!"}]

        result = await agent.graph.ainvoke({"topic": "Testing topic"})
    
    assert "final_report" in result
