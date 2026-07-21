from fastapi import APIRouter
from app.ai.agents.knowledge.agent import KnowledgeAgent
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["Knowledge Copilot"])
agent = KnowledgeAgent()

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    return agent.ask(request.question, request.project_id)