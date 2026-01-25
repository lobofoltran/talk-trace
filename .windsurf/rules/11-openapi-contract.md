---
trigger: always_on
---

# OpenAPI Contract Enforcement (Non-Negotiable)

This repository is **contract-first**.  
Every service API is defined and enforced through OpenAPI.

Agents MUST treat OpenAPI as a binding interface contract.

---

# 1. Contract-First Rule

## 1.1 OpenAPI is the Source of Truth
- Every HTTP endpoint MUST be declared in:

```
services/<name>/openapi.yaml
```

- Code MUST NOT introduce undocumented routes.

If a route exists in Flask, it MUST exist in OpenAPI.

If OpenAPI defines a route, Flask MUST implement it.

---

# 2. Required Structure per Service

Each service MUST include:

```
services/<name>/
openapi.yaml
routes.py
tests/test_routes.py
```


OpenAPI must match runtime behavior exactly.

---

# 3. Endpoint Discipline

## 3.1 Allowed Endpoints Only
- No debug endpoints
- No undocumented admin routes
- No implicit behavior

Every endpoint must be explicit:

- method
- path
- request body schema
- response schema
- error responses

---

# 4. Schema Rules

## 4.1 Request/Response Must Be Typed
All request/response payloads MUST define schemas:

- No free-form JSON blobs
- No untyped dict responses

Every response MUST include:

- status code
- JSON schema
- example

---

## 4.2 Error Response Standard

Every endpoint MUST define:

- `400` (bad request)
- `404` (not found)
- `500` (internal error)

Standard error schema:

```yaml
ErrorResponse:
  type: object
  required: [error]
  properties:
    error:
      type: string
```

---
# 5. Versioning Rule

## 5.1 Breaking Changes Forbidden Without Version Bump

Breaking changes include:

- removing fields
- renaming fields
- changing types
- removing endpoints

If unavoidable:

- introduce /v2/...
- keep /v1/... stable

---
# 6. Determinism + Contracts

Contracts MUST preserve deterministic outputs:

- stable field ordering
- stable schemas
- stable artifact naming
- No timestamp fields unless explicitly required.
---

# 7. Testing Requirement

## 7.1 Contract Coverage Required

Every endpoint MUST have unit tests asserting:

- status code correctness
- schema correctness
- error behavior

Minimum tests:

- happy path
- invalid payload → 400
- missing session → 404

## 7.2 OpenAPI Drift Prevention

Agents MUST ensure:
- Flask routes match OpenAPI paths
- OpenAPI examples match actual outputs
No contract drift is allowed.

---
# 8. Agent Workflow (Mandatory)

When adding/modifying an endpoint:

- Update openapi.yaml FIRST
- Implement route in routes.py
- Add unit tests
- Confirm schema + examples match runtime
Ensure coverage remains >80%

---
# 9. PR Checklist Addition

Before merge, confirm:
- OpenAPI updated
- No undocumented routes exist
- Error responses defined
- Tests cover all endpoints
- No breaking changes without versioning