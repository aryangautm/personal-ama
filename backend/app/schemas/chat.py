from pydantic import BaseModel
from typing import Optional


class ChatInvoke(BaseModel):
    input_message: str


class ChatInit(BaseModel):
    session_id: str
