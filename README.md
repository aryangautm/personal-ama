# 💬 Personal AMA - AI powered anonymous Chat

AI-powered anonymous chat application where users can ask questions and get responses through AI personas.

![Demo](https://github.com/user-attachments/assets/253d77e0-1d1a-4721-81c9-4def477b41c2)

<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
    <img src="https://img.shields.io/badge/🦜_LangChain-121212?style=for-the-badge" alt="LangChain">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

- **Backend**: FastAPI with SlowAPI rate limiting
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL with pgvector
- **AI**: LangChain agents with LangGraph checkpointer for memory

## Prerequisites

- [uv](https://github.com/astral-sh/uv) - Python package installer
- Node.js and npm
- Docker (optional, for PostgreSQL)

## Quick Start

### 1. Setup environment

```bash
cp .env.example .env
```

Update the `.env` file with your configuration.

### 2. Install dependencies

**Backend:**
```bash
cd backend
uv pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Start PostgreSQL

Run PostgreSQL locally with Docker:
```bash
docker run -d \
  --name personal-ama-db \
  -e POSTGRES_USER=your_user \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=personal_ama \
  -p 5432:5432 \
  pgvector/pgvector:pg17
```

### 4. Run database migrations

```bash
cd backend
alembic upgrade head
```

### 5. Start the application

**Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
```

**Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment

For production deployment with Docker, refer to the `docker-compose.yml` file:

```bash
docker compose up -d
```

This will start:
- Frontend (Nginx) on port 3000
- Backend API on port 8000
- PostgreSQL database on port 5432
- Nginx Proxy Manager on ports 80, 443, and 81

## License

Apache License 2.0
