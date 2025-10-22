from app.models.session import Session as SessionModel, ChatMessage
from sqlalchemy.orm import Session


def get_session(db: Session, session_id: str) -> SessionModel:
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()


def create_session(db: Session, persona_id: str) -> SessionModel:
    new_session = SessionModel(persona_id=persona_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def save_message(db: Session, message: ChatMessage) -> None:
    db.add(message)
    db.commit()
