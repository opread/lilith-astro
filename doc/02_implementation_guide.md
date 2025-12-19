# 02. Implementation Guide - Clean Architecture

## 1. Project Structure
We adhere to **Clean Architecture** principles. The directory structure is organized to separate concerns, making the core business logic independent of frameworks and external agents.

```
src/
├── core/                   # Inner Layer: Domain & Application Logic (No external deps)
│   ├── domain/             # Entities & Value Objects
│   │   ├── models.py       # Pydantic models (User, Chart, Interpretation)
│   │   └── exceptions.py   # Domain-specific exceptions
│   │
│   └── use_cases/          # Application Business Rules
│       ├── calculate_chart.py
│       ├── interpret_chart.py
│       └── generate_horoscope.py
│
├── infrastructure/         # Outer Layer: Frameworks & Drivers
│   ├── astro_engine/       # Implementation of Astro Interface
│   │   └── swiss_ephemeris.py
│   ├── ai/                 # Implementation of AI Interface
│   │   └── gemini_adapter.py
│   └── persistence/        # Database Repositories
│       └── in_memory_repo.py # Current: In-memory implementation
│
├── interfaces/             # Interface Adapters
│   ├── api/                # FastAPI Controllers (Routers)
│   │   ├── v1.py           # API v1 Router
│   │   └── main.py         # App Entrypoint
│   └── cli/                # (Optional) CLI commands
│
├── config/                 # Configuration & Environment Variables
│   └── settings.py
│
└── tests/                  # Test Suite (Mirrors src structure)
```

## 2. Core Dependencies
*   **FastAPI**: Web framework.
*   **Pydantic**: Data validation and settings management.
*   **pyswisseph**: Python extension to the Swiss Ephemeris library.
    *   **Windows prerequisite**: install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) before running `pip install pyswisseph`; the package compiles native extensions and requires the MSVC toolchain.
*   **google-generativeai**: Official Google Gemini SDK for Python.
*   **LangChain** (optional but recommended): For structured interaction with LLMs.
*   **SQLAlchemy** (Async): ORM for database interactions.
*   **Alembic**: Database migrations.

## 3. Development Phases

### Phase 1: Core Domain (The "Astro" Kernel)
**Goal**: Calculate precise planetary positions without any API or AI.
1.  Setup `src/core/domain` models.
2.  Implement `src/infrastructure/astro_engine` wrapper around `pyswisseph`.
3.  Write unit tests to verify calculation accuracy against known ephemeris data.

### Phase 2: Rules Engine
**Goal**: Transform mathematical data into basic text tokens.
1.  Define rules (currently Python dictionaries in `src/core/domain/rules.py`) mapping aspects/placements to traits.
2.  Implement the Interpretation logic in `src/core/use_cases`.

### Phase 3: API & Basic Persistence
**Goal**: Expose logic via HTTP.
1.  Setup FastAPI structure in `src/interfaces/api`.
2.  Configure Docker container.
3.  Implement basic endpoints defined in the API Spec.

### Phase 4: AI Layer
**Goal**: Generate premium narratives using Google Gemini.
1.  Implement `src/infrastructure/ai/gemini_adapter.py` using `google-generativeai`.
2.  Design system instructions and prompts optimized for Gemini's context window.
3.  Integrate AI calls into the `generate_horoscope` use case.

## 4. Coding Standards
*   **Type Hinting**: Mandatory for all function signatures.
*   **Docstrings**: Google style docstrings for all public modules and functions.
*   **Error Handling**: Use custom exceptions defined in `core/domain/exceptions.py`. Never let raw system errors leak to the API response.
*   **Testing**:
    *   Unit tests for logic (Core).
    *   Integration tests for Infrastructure (DB, AI).
    *   E2E tests for API endpoints.

## 5. Environment Configuration
Use a `.env` file loaded via `pydantic-settings`.

```env
APP_ENV=development
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/astro_db
GOOGLE_API_KEY=AIza...
SWISS_EPH_PATH=/usr/local/share/sweph  # Path to ephemeris files