from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    project_id: str
    question: str

class ChatResponse(BaseModel):
    answer: str
    cited_chunk_ids: List[str]