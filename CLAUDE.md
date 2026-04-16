# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LenoreSchedule is a Dockerized full-stack app for departmental scheduling. It has a Django Ninja backend API and a Vue 3 + Vuetify frontend, backed by PostgreSQL and fronted by Nginx in production.

## Development Commands

All development is done inside Docker. Start the stack with:
```bash
docker compose up -d        # Start all dev services
docker compose down         # Stop services
```

Service ports in dev:
- Frontend (Vite HMR): `8081`
- Backend API (Django): `8001`
- Backend Docs (MkDocs): `8002`

### Backend
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Testing (run from backend/ directory)
pytest                      # All tests
pytest -m unit              # Unit tests only
pytest -m service           # Service tests only
pytest -m api               # API tests only
pytest --cov                # With coverage report

# Linting
flake8 ./backend --ignore=E501,F401,E203,E701,W503
```

Test settings use `backend.settings_test`. Pytest markers: `unit`, `service`, `api`.

### Frontend
```bash
# Run from frontend/ directory
npm run dev       # Vite dev server with HMR
npm run build     # Production build
npm run lint      # ESLint with auto-fix
npm run format    # Prettier formatting
```

## Architecture

### Backend

**Framework**: Django 5.x with [Django Ninja](https://django-ninja.dev/) for the REST API (type-safe, schema-first, async-ready).

**Main API router**: [backend/backend/api.py](backend/backend/api.py) — mounts routers from all apps under a single `NinjaAPI` instance. All new endpoints must be registered here.

**Apps**:
- `staff/` — Employee, Group, Division, Location models and CRUD APIs
- `planner/` — Holiday definitions (with rule types: `fixed_date`, `nth_weekday`, `last_weekday`, `custom`) and `CalendarEntry` records
- `options/` — Singleton `Version` model and `PayrollInfo` configuration
- `core/` — Shared auth, services, and utilities

**Pattern** (for each app): models → services (`services/`) → DTOs (`api/schemas/`) → view logic (`api/views/`) → router (`api/routers/`) → registered in `backend/api.py`.

**Auth**: Custom `GlobalAuth()` class wraps Django session auth. Applied globally in the NinjaAPI config.

### Frontend

**Stack**: Vue 3 (Composition API) + Vite + Vuetify 3 + Pinia + TanStack Vue Query + Axios.

**API proxy**: Vite forwards `/api/*` to `http://backend:8001` — all API calls use the `/api` prefix.

**State**: Pinia stores in `src/stores/`. `themeStore.js` persists to localStorage. Server state (API data) is managed by Vue Query, not Pinia.

**Routing**: `src/router/index.js` — Vue Router with lazy-loaded views.

### Data flow
Frontend (Vue Query + Axios) → `/api` (Nginx proxy in prod / Vite proxy in dev) → Django Ninja API → Service layer → Django ORM → PostgreSQL.

## Commit Message Format

Semantic commits are enforced via CI (`pr-title-lint.yml`):
```
<type>(optional scope): <description>
```
Types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`. Breaking changes use `feat!:` or `fix!:`.

## Environment

Dev environment variables are in `.env.dev` (checked in). Production uses `.env` (not checked in). Key variable: `TIMEZONE=America/New_York`.

## Test Organization

Tests live under `<app>/tests/{unit,service,api}/`. Fixtures are in the top-level `conftest.py` — notably `api_client` (Django Ninja test client) and `today_date`. Factory Boy is used for model factories.
