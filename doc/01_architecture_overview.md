# 01. Architecture Overview - AstroPersona

## 1. Introduction
AstroPersona is a premium, personalized horoscope application designed to deliver high-precision astronomical calculations combined with advanced, AI-enhanced interpretations. The system is architected to be modular, scalable, and testable, adhering to modern software engineering standards suitable for production environments.

## 2. Architectural Pattern
We will adopt a **Modular Monolith** architecture with **Clean Architecture** principles.
- **Why Modular Monolith?** It allows for rapid development and simplified deployment (single Docker container initially) while keeping domains strictly separated. This makes the future transition to Microservices trivial if scaling requires it.
- **Why Clean Architecture?** It ensures that the core domain logic (astronomy rules) remains independent of frameworks (FastAPI), databases, or external interfaces (AI providers).

## 3. High-Level Design (C4 Model)

### 3.1 System Context
The user interacts with the AstroPersona API via a React Frontend application.

```mermaid
graph LR
    User[End User] -->|Interacts| Frontend[React Single Page App]
    Frontend -->|HTTP API Calls| Backend[AstroPersona Backend (FastAPI)]
    Backend -->|Queries| LLM[Google Gemini API]
```

### 3.2 Container Diagram
The system is composed of the following distinct logical containers (modules):

```mermaid
graph TD
    Frontend[React Frontend] -->|HTTPS| API[API Gateway / Controller Layer]
    
    subgraph "AstroPersona Backend"
        API --> Service[Service Layer]
        
        subgraph "Core Domain"
            Service --> AstroEng[Astro Engine (Math)]
            Service --> InterpEng[Interpretation Engine (Rules)]
        end
        
        subgraph "Infrastructure / Adapters"
            Service --> AISvc[AI Service Adapter]
            Service --> Repo[Persistence Adapter]
        end
    end
    
    AstroEng -->|Uses| SwissEph[Swiss Ephemeris Lib]
    AISvc -->|API Call| Gemini[Google Gemini API]
    Repo -->|In-Memory| MemStore[(Memory Dict)]
```

## 4. Key Components

### 4.1 Astro Engine (Core Domain)
*   **Responsibility**: Pure mathematical calculations using `pyswisseph`.
*   **Characteristics**: Deterministic, stateless, high precision.
*   **Inputs**: Timestamp, Latitude, Longitude.
*   **Outputs**: Planet positions (Sign, Degree), Houses, Aspects.

### 4.2 Interpretation Engine (Core Domain)
*   **Responsibility**: Translating mathematical data into semantic meaning based on astrological rules.
*   **Characteristics**: Rule-based, extensible.
*   **Pattern**: Strategy Pattern or Rule Engine for mapping planetary configurations to text keys (e.g., `SUN_LEO_HOUSE_5`).

### 4.3 AI Service (Infrastructure)
*   **Responsibility**: Generating natural language narratives from semantic tokens.
*   **Characteristics**: Asynchronous, failure-tolerant (circuit breaker pattern).
*   **Integration**: Uses **Google Gemini API** for high-quality, context-aware generation. Prompts are constructed using data from the Interpretation Engine.

### 4.4 Persistence (Current State)
*   **Repository**: Currently implemented as an **In-Memory Repository** (`InMemoryRepository`).
*   **Storage**: Data (Profiles, Charts) is stored in Python dictionaries (`Dict[str, Model]`) within the application process.
*   **Implication**: Data is ephemeral and is lost when the application restarts. This is suitable for the current development/prototype phase.

## 5. Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Frontend** | React + TypeScript | Modern, type-safe UI with rich component ecosystem. |
| **Backend Language** | Python 3.11+ | Native support for `pyswisseph`, strong AI ecosystem. |
| **Web Framework** | FastAPI | High performance (ASGI), auto-documentation (OpenAPI), strict typing. |
| **Astro Library** | pyswisseph | The gold standard for astrological precision. |
| **Persistence** | In-Memory (Dict) | rapid prototyping; zero external dependencies. |
| **Testing** | Pytest | Industry standard for Python testing. |
| **Linting/Formatting** | Ruff | High-speed linting. |

## 6. Future Work & Roadmap
To move from the current prototype to a production-ready system, the following architectural changes are planned:

### 6.1 Persistence Layer Upgrade
*   **Goal**: Replace `InMemoryRepository` with a persistent database adapter.
*   **Target**: **PostgreSQL**.
*   **Why**: To persist user profiles and historical chart readings across sessions and restarts. The current Repository pattern allows this switch without changing Core Domain logic.

### 6.2 Caching Layer
*   **Goal**: Implement a caching adapter.
*   **Target**: **Redis**.
*   **Why**: To cache heavy astronomical calculations (keyed by lat/long/time) and expensive AI API responses to reduce costs and latency.

## 7. Scalability & Performance
*   **Stateless API**: The application layer is stateless, allowing horizontal scaling behind a load balancer.
*   **Caching Strategy**:
    *   **L1 Cache**: In-memory (LRU) for frequently accessed static data (e.g., rule definitions).
    *   **L2 Cache**: Redis for calculation results keyed by (Lat, Long, Time) rounded to minutes, to avoid re-calculating for same birth times.
*   **Async I/O**: Leveraging `asyncio` for non-blocking calls to the AI provider and Database.