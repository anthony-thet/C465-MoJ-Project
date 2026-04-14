# Ministry of Jokes — API Contract

**Base URL:** `http://localhost:5000/api/v1`
**Version:** 1.0

---
## GET /api/v1/jokes/count

Returns the total number of jokes in the database.

### Request
- **Method:** GET
- **Authentication:** Not required
- **Query Parameters:** None
- **Request Body:** None

### Success Response (200 OK)
```json
{
  "data": { "count": 42 },
  "status": "ok"
}

```

### Error Responses
| Status | Code | When |
|--------|------|------|
| 405 | METHOD_NOT_ALLOWED | Non-GET method used |
| 500 | INTERNAL_ERROR | Database unreachable |

### Notes
- Count includes all jokes regardless of author or status.
- Returns 0 (not an error) when no jokes exist.
- This endpoint is the prerequisite for client-side pagination of GET /api/v1/jokes.
---
## GET /api/v1/jokes

Returns all jokes in the database.

### Request
- **Method:** GET
- **Authentication:** Not required
- **Query Parameters:** None
- **Request Body:** None

### Success Response (200 OK)
```json
{
  "data": {
                "jokes": [
                    {
                        "id": joke.id,
                        "text": joke.text,
                        "author": joke.author.username
                            if joke.author else "anonymous"
                    }
                    for joke in jokes
                ]
            }
}

```

### Error Responses
| Status | Code | When |
| 500 | INTERNAL_ERROR | Database unreachable |

### Notes
- Includes all jokes regardless of author or status.
- Returns null (not an error) when no jokes exist.
