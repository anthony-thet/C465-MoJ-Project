# MoJ Schema Decisions — ICEX_MJ03

## Models

### User
| Field | Type | Nullable | Notes |
|---|---|---|---|
| | | | |

### Joke
| Field | Type | Nullable | Notes |
|---|---|---|---|
| | | | |

## Data Capture Decisions

### Fields captured in v1 that are not displayed in v1
For each field below, explain: (1) what it enables, (2) why it cannot be reconstructed later.

- `submitted_by`:
- `created_at`:

## Deferred Fields
Fields explicitly excluded from v1 with a known migration path:

- `quality_score`: deferred to Cycle 3 (Ollama integration). Will be added via `flask db migrate`.
