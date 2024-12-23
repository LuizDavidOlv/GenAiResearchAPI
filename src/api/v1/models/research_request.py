from pydantic import BaseModel


class ResearchRequest(BaseModel):
    input_text: str
    chat_model: str = 'gpt-4o-mini'
    temp: int = 1

