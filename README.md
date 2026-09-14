# Book Catalog

Async FastAPI app with SQLAlchemy and SQLite. Authors register and log in with JWT.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn main:app --reload
```

OpenAPI docs: http://127.0.0.1:8000/docs

## Auth

- `POST /api/v1/register` — create an Author (`username`, `name`, `password`)
- `POST /api/v1/login` — authenticate by `username` and `password`, receive a JWT
