# GitHub Copilot Instructions for Dolorestec Auth

## Repository Overview

This repository contains the Dolorestec Auth microservice, a secure authentication service built with Python 3.14+ and FastAPI. It handles JWT-based authentication, password hashing, rate limiting, and integrates with PostgreSQL, Redis, and RabbitMQ for a scalable, stateless auth system.

The project follows Clean Architecture, Domain-Driven Design (DDD), and SOLID principles. It uses async programming for high performance and supports OAuth2 flows like password grant and client credentials.

## High-Level Details

- **Languages and Frameworks**: Python 3.14+, FastAPI, Pydantic, Uvicorn
- **Target Runtime**: ASGI server (Uvicorn), designed for async I/O operations
- **Project Type**: Microservice, RESTful API
- **Size**: Small to medium, focused on authentication domain
- **Key Technologies**: JWT (python-jose), bcrypt (passlib), asyncpg, aioredis, aio-pika, structlog

## Build, Test, Run, Lint Instructions

### Bootstrap
- Install dependencies: `uv install` (requires UV package manager)
- Set up environment variables: Copy `.env.example` to `.env` and configure database, Redis, RabbitMQ connections

### Build
- No explicit build step; Python is interpreted. Ensure dependencies are installed via `uv install`

### Test
- Run all tests: `pytest`
- With coverage: `pytest --cov=app --cov-report=html`
- Async tests: `pytest -k "async"`
- Parallel execution: `pytest -n auto`
- Integration tests: `pytest -m integration`

### Run
- Development: `uvicorn app.main:app --reload`
- Production: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Access docs: http://localhost:8000/docs

### Lint
- Ruff (lint and format): `ruff check .` and `ruff format .`
- MyPy (type checking): `mypy .`
- Bandit (security): `bandit -r .`
- Pip-audit (vulnerabilities): `pip-audit`

### Other Scripted Steps
- Pre-commit hooks: `pre-commit run --all-files`
- Docs: `mkdocs serve` (for MkDocs documentation)

Each command should be run from the project root. Dependencies must be installed first. Tests require a test database and Redis/RabbitMQ instances (use Docker or local setup).

## Project Layout and Architecture

### Major Architectural Elements
- **Presentation Layer**: `app/api/` - FastAPI routes for auth endpoints (login, validate, refresh)
- **Application Layer**: `app/use_cases/` - Business logic for authentication, token management, rate limiting
- **Domain Layer**: `app/domain/` - Entities (User, Token), value objects, domain rules
- **Infrastructure Layer**: `app/infrastructure/` - Adapters for PostgreSQL (asyncpg), Redis (aioredis), RabbitMQ (aio-pika)

### Configuration Files
- `pyproject.toml`: Project config, dependencies, tool settings (ruff, mypy)
- `.env`: Environment variables for secrets and connections
- `uv.lock`: Dependency lock file (UV)
- `pre-commit-config.yaml`: Pre-commit hooks for quality

### Validation Pipelines
- GitHub Actions CI: Runs tests, linting, security checks on PRs
- Pre-commit: Local hooks for code quality before commits

### Dependencies
- Core: fastapi, uvicorn, pydantic, python-jose[cryptography], passlib[bcrypt]
- Async: asyncpg, aioredis, aio-pika, httpx
- Quality: ruff, mypy, pytest, pytest-asyncio, structlog
- Docs: mkdocs

No complex migrations; simple queries via asyncpg. Redis for cache/sessions, RabbitMQ for events.

### Key Source Files
- `app/main.py`: FastAPI app entry point
- `app/domain/user.py`: User entity
- `app/domain/token.py`: Token/JWT logic
- `app/use_cases/auth.py`: Login/logout use cases
- `app/infrastructure/redis_client.py`: Redis adapter
- `tests/`: Test files mirroring source structure

## Additional Instructions

- Always use async/await for I/O operations (database, cache, messaging)
- Follow Clean Architecture: Keep domain pure, inject dependencies
- Use Pydantic for validation and settings
- Log with structlog for structured output
- Implement rate limiting via Redis to prevent brute force
- Publish events to RabbitMQ for audit/integration
- Use JWT for stateless auth; validate signatures, not server state
- Hash passwords with bcrypt; never store plain text
- Write tests first (TDD); cover async paths
- Run full test suite before commits/PRs
- Use ruff for fast linting/formatting
- Document APIs with FastAPI's auto-docs
- Ensure complete Swagger documentation with detailed descriptions, examples, and responses for all endpoints
- Apply SOLID principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- Do not hardcode sensitive data; use environment variables for secrets
- **Type Annotations**: Always use `from __future__ import annotations` at the top of modules instead of `TYPE_CHECKING` for conditional imports. This ensures type annotations are strings and avoids runtime dependencies on type-only imports.

Trust these instructions; they are validated and up-to-date. If something is unclear, check the README or pyproject.toml for details.
