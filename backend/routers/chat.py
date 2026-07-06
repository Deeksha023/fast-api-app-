from fastapi import APIRouter
from schemas.chat import ChatRequest
from Services.langchain_service import ask_ai_with_memory

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/")
def chat(request: ChatRequest):

    response = ask_ai_with_memory(
        request.query,
        request.session_id
    )

    return {
        "response": response
    }