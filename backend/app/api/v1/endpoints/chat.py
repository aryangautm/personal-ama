from app.crud import session as session_crud
from app.crud import persona as persona_crud
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatInvoke, ChatInit
from fastapi.responses import StreamingResponse
from app.services.chat.agent import conversation
from app.models import ChatMessage
from uuid import UUID

router = APIRouter()


@router.get("/init/{persona_id}", response_model=ChatInit)
def chat_init(persona_id: UUID, db: Session = Depends(get_db)):

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
def chat_stream(session_id: str, chat_in: ChatInvoke, db: Session = Depends(get_db)):

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
