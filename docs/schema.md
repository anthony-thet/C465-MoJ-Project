# MoJ Schema Decisions — ICEX_MJ03

## Models

### User
| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | Integer | No | Primary Key |
| username | String(30) | No | Unique Login |
| password | String(30) | No | User Password, should be hashed or something for security | 

### Joke
| Field | Type | Nullable | Notes |
|---|---|---|---|
| id | Integer | No | Primary Key|
| text | String(500)| No | Joke Content |
| submitted_by | Integer | No | Foreign Key of user.id |
| created_at | Data and Time | No | Timestamp of Joke |

## Data Capture Decisions

### Fields captured in v1 that are not displayed in v1
For each field below, explain: (1) what it enables, (2) why it cannot be reconstructed later.

- `submitted_by`: This field is captured in v1 even though no attribution is displayed. This field cannot be reconstructed from any other data source — once a joke is inserted without a user link, the association is permanently lost. The capture cost is one column and one foreign key constraint. If v2 or v3 introduces joke attribution, leaderboards, or per-user analytics, this field must exist from the beginning. This is a deliberate MVP exception: MVP governs behavior we build, not data we can never recover.
- `created_at`: Provides the context needed for sorting jokes and also managing jokes in the future. Essentially, just ensures that future development of MoJ will not encounter issues due to backfilling or lacking joke information. 

## Deferred Fields
Fields explicitly excluded from v1 with a known migration path:

- `quality_score`: deferred to Cycle 3 (Ollama integration). Will be added via `flask db migrate`.
