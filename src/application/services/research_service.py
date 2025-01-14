
from langchain_openai import ChatOpenAI
from src.api.v1.models.research_request import ResearchRequest
from src.application.agents.essay_agent import EssayWriterAgent
from src.application.agents.research_agent import ResearchAgent


class ResearchService:
    async def research(request: ResearchRequest):
        model = ChatOpenAI(model=request.chat_model, temperature=request.temp)
        agent = ResearchAgent(model)
        result = await agent.graph.ainvoke({"topic": request.input_text})
        return result["final_report"]
    

    def write_essay(request: str, chat_model ='gpt-4o-mini', temp = 1, revisions = 3):
        model = ChatOpenAI(model= chat_model, temperature=temp)
        agent = EssayWriterAgent(model)
        result = agent.graph.invoke(
            {
                "topic": request,
                "max_revisions": revisions,
                "revision_number": 1,
            }
        )
        return result["content"]