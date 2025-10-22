from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.state import CompiledStateGraph

from app.core.config import settings
from app.core.database import SessionLocal
from app.crud import persona as persona_crud
from app.crud import session as session_crud
from app.memory.checkpointers import pg_checkpointer
from app.models import ChatMessage


@dataclass
class Context:
    persona_id: str


_agent = {}


def get_agent(persona_id) -> CompiledStateGraph:

    global _agent

    if not _agent.get(persona_id):
        with SessionLocal() as db:
            persona = persona_crud.get(db, persona_id=persona_id)

        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=persona.temperature or 0.7,
        )

        agent = create_agent(
            model=model,
            system_prompt=persona.prompt,
            context_schema=Context,
            checkpointer=pg_checkpointer,
        )

        _agent[persona_id] = agent

    return _agent[persona_id]


def _callback_handler(session_id: str, role: str, message: str) -> None:
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=message,
    )
    with SessionLocal() as db:
        session_crud.save_message(db, message)


def conversation(persona_id: str, input_message: str, session_id: str):
    agent = get_agent(persona_id)
    config = {"configurable": {"thread_id": session_id, "persona_id": persona_id}}

    response = ""
    for token, _ in agent.stream(
        input={"messages": [{"role": "user", "content": input_message}]},
        stream_mode="messages",
        config=config,
        context=Context(persona_id=persona_id),
    ):
        response += token.content
        yield token.content

    _callback_handler(session_id=session_id, role="assistant", message=response)
