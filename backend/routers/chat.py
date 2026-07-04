from fastapi import APIRouter, HTTPException, status
from schemas.chat import ChatRequest
from Services.langchain_service import ask_ai

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("/")
def chat(request: ChatRequest):
    try:
        response = ask_ai(request.query)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service failed: {exc}"
        )

    return {
        "response": response
    }
