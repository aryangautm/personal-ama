from app.crud import session as session_crud
from app.crud import persona as persona_crud
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatInvoke, ChatInit
from fastapi.responses import StreamingResponse
from app.services.chat.agent import conversation
from app.models import ChatMessage
from uuid import UUID
from app.core.security import limiter
from app.core.config import settings

router = APIRouter()


@router.get("/init/{persona_id}", response_model=ChatInit)
@limiter.limit([settings.RATE_LIMIT])
def chat_init(persona_id: UUID, request: Request, db: Session = Depends(get_db)):

    persona = persona_crud.get(db, persona_id=persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persona not found"
        )

    session = session_crud.create_session(db, persona_id=persona.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not created"
        )

    return ChatInit(session_id=str(session.id))


@router.post("/stream/{session_id}", status_code=status.HTTP_201_CREATED)
@limiter.limit([settings.RATE_LIMIT])
def chat_stream(
    session_id: str,
    chat_in: ChatInvoke,
    request: Request,
    db: Session = Depends(get_db),
):

    session = session_crud.get_session(db, session_id=session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )

    persona_id = session.persona_id
    session_id = str(session.id)

    session_crud.save_message(
        db,
        ChatMessage(session_id=session_id, role="user", content=chat_in.input_message),
    )

    return StreamingResponse(
        conversation(persona_id, chat_in.input_message, session_id),
        media_type="text/event-stream",
    )
