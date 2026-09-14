# Book Catalog

Async FastAPI app with SQLAlchemy and SQLite. Authors register and log in with JWT.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt
cp src/.env.example src/.env
```

## Run

From the project root:

```bash
uvicorn main:app --app-dir src --reload
```

OpenAPI docs: http://127.0.0.1:8000/docs

Protected routes use `Authorization: <token>`. In Swagger click **Authorize**, paste the JWT from login/register (token only, no Bearer prefix).

## Auth

- `POST /api/v1/register` — create an Author (`username`, `name`, `password`)
- `POST /api/v1/login` — authenticate by `username` and `password`, receive a JWT
- `GET /api/v1/profile` — read the current author's profile (`Authorization: <token>`)
- `PATCH /api/v1/profile` — update own profile (`name`, `bio`, `birth_year`; not username or password)
- `DELETE /api/v1/profile` — delete own profile

## Catalog

- `GET /api/v1/catalog` — public paginated list of books (`page`, `page_size` default 10)
- `GET /api/v1/catalog/{id}` — public book detail

## Books

- `GET /api/v1/books/my` — paginated list of the current author's books
- `GET /api/v1/books/{id}` — get one of your books
- `POST /api/v1/books` — create a book (`title`, `published_year`)
- `PATCH /api/v1/books/{id}` — update your book
- `DELETE /api/v1/books/{id}` — delete your book
