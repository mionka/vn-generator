# FastAPI Template
A FastAPI project template with database integration.

## 🚀 Features

- **FastAPI** for high-performance API development
- **SQLAlchemy & Alembic** for database management and migrations
- **Pydantic** for data validation
- **Poetry** for dependency management
- **Docker & Docker Compose** for containerized deployment


## Installation & Setup

### Requirements

Make sure you have the following installed:

- `Docker` & `docker-compose`
- `Python 3.12`
- `Poetry`

### Dependency management

1. Create a virtual environment and install dependencies
```commandline
poetry install
```

2. Activate virtual environment

```commandline
poetry shell
```

### Running the application

0. Create a `.env` file with the following variables (or use `make env` command)
```dotenv
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=5432
```

1. Start the database in a Docker container
```commandline
make db
```
2. Apply database migrations
```commandline
make migrate head
```
3. Run the application
```commandline
make run
```

After starting the application, you can access the API documentation at `http://127.0.0.1:8080/swagger`.


### Static analysis

- Run linters
```commandline
make lint
```

- Format code
```commandline
make format
```

### Additional commands

- Create a new migration revision
```commandline
make revision message="..."
```

## 📖 API Documentation

After starting the application, you can access the API documentation at `http://127.0.0.1:8080/swagger`.

## 📁 Project Structure

This FastAPI template follows a layered architecture pattern with a focus on separation of concerns. Below is a brief overview of the main components and their roles.

```bash
.
├── Makefile
├── README.md
├── docker-compose.yml
├── poetry.lock
├── poetry.toml
├── pyproject.toml
└── src
    └── app
        ├── __init__.py
        ├── __main__.py
        ├── api
        ├── config
        ├── db
        │   ├── connection
        │   ├── migration
        │   └── models
        ├── repositories
        ├── schemas
        ├── services
        └── utils
```

1. app/ — main application directory:
   - api/: API route definitions.
   - config/: configurations and application settings.
   - db/: everything related to database interactions:
        - connection/: database connection setup.
        - migration/: migration scripts.
        - models/: SQLAlchemy ORM models.
   - repositories/: the logic for interacting with the database (CRUD operations).
   - schemas/: Pydantic models used for data validation and serialization..
   - services/: the business logic of the application; the services use repositories to interact with the database and perform higher-level operations.
   - utils/: various helper functions that are used across the application.
