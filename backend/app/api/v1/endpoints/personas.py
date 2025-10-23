from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import require_api_key
from app.core.database import get_db
from app.crud import persona as persona_crud
from app.schemas.persona import (
    PersonaCreate,
    PersonaResponse,
    PersonaUpdate,
    PersonaLatestResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
def create_persona(persona_in: PersonaCreate, db: Session = Depends(get_db)):
    existing = persona_crud.get_by_username(db, username=persona_in.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    return persona_crud.create(db, obj_in=persona_in)


@router.get(
    "/", response_model=List[PersonaResponse], dependencies=[Depends(require_api_key)]
)
def list_personas(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    return persona_crud.get_multi(db, skip=skip, limit=limit, active_only=active_only)


@router.get("/latest", response_model=PersonaLatestResponse)
def get_latest_persona(db: Session = Depends(get_db)):
    persona = persona_crud.get_latest(db)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona not found",
        )
    return persona


@router.get(
    "/{persona_id}",
    response_model=PersonaResponse,
    dependencies=[Depends(require_api_key)],
)
def get_persona(persona_id: UUID, db: Session = Depends(get_db)):
    persona = persona_crud.get(db, persona_id=persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona not found",
        )
    return persona


@router.get(
    "/username/{username}",
    response_model=PersonaResponse,
    dependencies=[Depends(require_api_key)],
)
def get_persona_by_username(username: str, db: Session = Depends(get_db)):
    persona = persona_crud.get_by_username(db, username=username)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona not found",
        )
    return persona


@router.patch(
    "/{persona_id}",
    response_model=PersonaResponse,
    dependencies=[Depends(require_api_key)],
)
def update_persona(
    persona_id: UUID, persona_in: PersonaUpdate, db: Session = Depends(get_db)
):
    persona = persona_crud.get(db, persona_id=persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona not found",
        )
    if persona_in.username and persona_in.username != persona.username:
        existing = persona_crud.get_by_username(db, username=persona_in.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
    return persona_crud.update(db, db_obj=persona, obj_in=persona_in)


@router.delete(
    "/{persona_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_api_key)],
)
def delete_persona(persona_id: UUID, db: Session = Depends(get_db)):
    persona = persona_crud.delete(db, persona_id=persona_id)
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Persona not found",
        )
