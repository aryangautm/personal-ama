from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.persona import Persona
from app.schemas.persona import PersonaCreate, PersonaUpdate


def create(db: Session, obj_in: PersonaCreate) -> Persona:
    db_obj = Persona(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get(db: Session, persona_id: UUID) -> Optional[Persona]:
    return db.query(Persona).filter(Persona.id == persona_id).first()


def get_latest(db: Session) -> Optional[Session]:
    return (
        db.query(Persona)
        .filter(Persona.is_active == True)
        .order_by(Persona.created_at.desc())
        .limit(1)
        .first()
    )


def get_by_username(db: Session, username: str) -> Optional[Persona]:
    return db.query(Persona).filter(Persona.username == username).first()


def get_multi(
    db: Session, skip: int = 0, limit: int = 100, active_only: bool = False
) -> List[Persona]:
    query = db.query(Persona)
    if active_only:
        query = query.filter(Persona.is_active == True)
    return query.offset(skip).limit(limit).all()


def update(db: Session, db_obj: Persona, obj_in: PersonaUpdate) -> Persona:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, persona_id: UUID) -> Optional[Persona]:
    db_obj = get(db, persona_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj
