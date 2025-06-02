
# reviro TechStart fastapi project

Simple FastAPI project with SQLAlchemy ORM, Alembic migrations, and Docker support.

## Requirements

- Docker (optional, but recommended)
- Python 3.8+

## Setup and Run

### 1. Clone the repository and set env

```bash
git clone git@github.com:JKLeorio/reviro_fastapi_testapp.git
cd reviro_fastapi_testapp
```
Create a .env file and pass the filled values ​​from .env.example to it

### 2. Run with Docker (recommended)

Build and start the container:

```bash
docker compose build
docker compose up
```

This will build the Docker image, run tests and migrations, and start the FastAPI server with Uvicorn.

The API will be available at:  
`http://localhost:8000`

### 3. Run locally without Docker

#### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh # Linux/macOS
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"    # Windows
```

#### Create and activate virtual environment, install dependencies

```bash
uv sync
```

#### Run tests

```bash
uv run pytest tests\
```

#### Run database migrations

```bash
uv run alembic upgrade head
```

#### Start the FastAPI server

```bash
uv run main.py
```

The API will be available at:  
`http://localhost:8000`

## Alembic commands

- To create a new migration:

```bash
uv run alembic revision --autogenerate -m "Migration message"
```

- To apply migrations:

```bash
uv run alembic upgrade head
```

## API Documentation

Once running, visit the interactive API docs at:  
`http://localhost:8000/docs` (Swagger UI)  
or  
`http://localhost:8000/redoc` (ReDoc)
or 
`https://documenter.getpostman.com/view/16111760/2sB2qgeJBN` (Postman)


## Рефлексия
1. Не знал многие технологии которые пришлось использовать, многое учил почти с нуля
2. Не могу выделить что то особенное
3. Тесты, они получились ужасными
4. Начал вечером 26.05, закончил утром 02.06
5. Sqlalchemy, alembic, fastapi, pytest, pydantic на базовом уровне, postman использовал только для запросов, научился документировать