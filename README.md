# ResolveAI – AI Customer Support Intelligence Platform

## Project overview

ResolveAI is a planned platform for turning customer-support conversations into useful, actionable intelligence. It will help support teams understand recurring issues, prioritize customer needs, and make support work more efficient.

## Business problem

Support organizations handle high volumes of conversations across channels. Manual review makes it difficult to identify emerging issues, measure customer sentiment consistently, and deliver timely, relevant answers. ResolveAI aims to make these conversations easier to analyze while keeping support staff in control of customer-facing decisions.

## Planned technology stack

- **Backend:** Python 3.12 and FastAPI
- **Frontend:** React and TypeScript
- **Language models:** Ollama for local model workflows and Gemini API for hosted model workflows
- **Data and evaluation:** Python-based data processing, with storage and retrieval technologies to be selected as requirements become clear
- **Testing and tooling:** pytest, Git, and standard Python/JavaScript project tooling

Technology choices are provisional and will be validated as the project develops. API keys and other secrets must be kept out of source control.

## Initial architecture

```text
Support conversations and approved data
                 |
                 v
       Data preparation and evaluation
                 |
                 v
   Python backend and AI/model integrations
      |                          |
      v                          v
  Ollama (local)          Gemini API (hosted)
                 |
                 v
      React/TypeScript support interface
```

The backend will own data access and model integration. The frontend will present insights and support workflows. Data ingestion, privacy controls, persistence, and deployment details will be defined before implementation.

## Development roadmap

1. Establish the project structure, Python environment, and Git hygiene.
2. Define requirements, data boundaries, privacy expectations, and success metrics.
3. Prepare representative datasets and a repeatable evaluation approach.
4. Design and implement backend interfaces and model integrations.
5. Build the support-facing frontend and connect it to the backend.
6. Test quality, safety, performance, and operational readiness before deployment.

## Project layout

- `backend/` — planned API and AI services
- `frontend/` — planned support interface
- `data/raw/`, `data/processed/`, `data/synthetic/` — local data organization
- `notebooks/` — exploratory analysis and experiments
- `tests/` — automated tests
- `docs/` — project and design documentation

## Development environment

The backend virtual environment uses Python 3.12. To activate it in a new PowerShell terminal from the project root:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

No application code or third-party dependencies have been added yet.
