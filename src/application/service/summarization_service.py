
from langchain.chat_models import ChatOpenAI
from src.application.agents.EssayWriterAgent import EssayWriterAgent


class SummarizationService:
    def summarize(request: str):
        return "Summarized"
    

    def write_essay(request: str, chat_model ='gpt-3.5-turbo', temp = 1, revisions = 3):
        model = ChatOpenAI(model= chat_model, temperature=temp)
        agent = EssayWriterAgent(model)
        result = agent.graph.invoke(
            {
                "task": request,
                "max_revisions": revisions,
                "revision_number": 1,
            }
        )
        return result["content"]