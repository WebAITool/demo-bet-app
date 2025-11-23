# backend

## uv commands

uv add (dep)

uv add -r requirements.txt

uv sync && uv lock

uv sync --upgrade

uv pip compile pyproject.toml -o requirements.txt

## devloop

(z /backend)

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

OR

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

(z /frontend)

npm run dev
