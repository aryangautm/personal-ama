from langgraph.checkpoint.postgres import PostgresSaver
from psycopg import Connection
from app.core.config import settings

conn = Connection.connect(settings.DATABASE_URL)
conn.autocommit = True

pg_checkpointer = PostgresSaver(conn)
