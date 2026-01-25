---
trigger: always_on
---

# Core Rules for TalkTrace

## Architecture Pattern
- **Clean Architecture** is MANDATORY for all services
- **Dependency Direction**: Inward only (Domain ← Application ← Infrastructure ← API)
- **No circular dependencies** between layers
- **Interface segregation** in domain layer

## Code Standards
- MAX_FILE_LENGTH: 200 lines (hard limit — split if longer)
- MIN_COVERAGE: 80%
- ARTIFACTS_MANDATORY: true
- ERRORS_LOG_APPEND: always
- NO_RANDOM_IN_PIPELINE: true
- SERVICES: transcriber, analyzer, exporter
- COMMUNICATION: HTTP + disk only

## Layer Responsibilities
- **Domain**: Business logic, entities, ports (interfaces)
- **Application**: Use cases, orchestrators, business rules
- **Infrastructure**: External integrations, adapters, implementations
- **API**: HTTP endpoints, request/response mapping

When suggesting code:
- Always show imports first
- Keep functions small (< 30 lines ideal)
- Add docstrings to public functions
- Follow dependency injection principles
- Never import from outer layers