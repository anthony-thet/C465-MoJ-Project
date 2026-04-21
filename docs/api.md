# Ministry of Jokes — API Contract

**Base URL:** `http://localhost:5000/api/v1`  
**Version:** 1.0

---

## Public Joke Endpoints

### GET /api/v1/jokes/count

Returns the total number of jokes in the database.

#### Request
- **Method:** GET
- **Authentication:** Not required
- **Query Parameters:** None
- **Request Body:** None

#### Success Response (200 OK)
```json
{
  "data": {
    "count": 42
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 500 | INTERNAL_ERROR | Database unreachable |

#### Notes
- Count includes all jokes regardless of author or status.
- Returns `0` (not an error) when no jokes exist.
- This endpoint is a prerequisite for client-side pagination of `GET /api/v1/jokes`.

---

### GET /api/v1/jokes

Returns all jokes in the database.

#### Request
- **Method:** GET
- **Authentication:** Not required
- **Query Parameters:** None
- **Request Body:** None

#### Success Response (200 OK)
```json
{
  "data": {
    "jokes": [
      {
        "id": 1,
        "text": "Why did the chicken cross the road?",
        "author": "newuser"
      }
    ]
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 500 | INTERNAL_ERROR | Database unreachable |

#### Notes
- Includes all jokes regardless of author or status.
- Returns an empty list (`[]`) if no jokes exist.

---

## Authentication Endpoints

### POST /api/v1/auth/login

Authenticates a user and creates a session.

#### Request
- **Method:** POST
- **Authentication:** Not required
- **Query Parameters:** None
- **Request Body:**
```json
{
  "username": "newuser",
  "password": "secretpassword"
}
```

#### Success Response (200 OK)
```json
{
  "data": {
    "user": {
      "id": 1,
      "username": "newuser"
    }
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | Invalid username or password |

---

### GET /api/v1/auth/me

Returns the currently authenticated user.

#### Request
- **Method:** GET
- **Authentication:** Required (session cookie)
- **Query Parameters:** None
- **Request Body:** None

#### Success Response (200 OK)
```json
{
  "data": {
    "user": {
      "id": 1,
      "username": "newuser",
      "role": "joke-teller",
      "has_submitted": true
    }
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |

---

### POST /api/v1/auth/logout

Logs out the currently authenticated user and clears the session.

#### Request
- **Method:** POST
- **Authentication:** Required (session cookie)
- **Query Parameters:** None
- **Request Body:** None

#### Success Response (200 OK)
```json
{
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |

---

## Admin Joke Management Endpoints

### GET /api/v1/admin/jokes

Returns jokes visible to administrators. Supports filtering flagged jokes.

#### Request
- **Method:** GET
- **Authentication:** Required
- **Authorization:** Admin only
- **Query Parameters:**
  - `flagged=true` — return only jokes where `flagged` is `true`
- **Request Body:** None

#### Success Response (200 OK)
```json
{
  "data": {
    "jokes": [
      {
        "id": 1,
        "text": "Why did the chicken cross the road?",
        "author": "newuser",
        "flagged": true,
        "ai_rating": 0.87
      }
    ]
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |
| 403 | FORBIDDEN | Authenticated user is not an admin |

#### Notes
- If `?flagged=true` is provided, only jokes with `flagged=true` are returned.
- Any other value for `flagged` is ignored, and all jokes are returned.
- Returns an empty list (`[]`) if no jokes match.
- Each joke includes `id`, `text`, `author`, `flagged`, and `ai_rating`.

---

### DELETE /api/v1/admin/jokes/<id>

Permanently deletes a joke by ID.

#### Request
- **Method:** DELETE
- **Authentication:** Required
- **Authorization:** Admin only
- **Query Parameters:** None
- **Request Body:** None

#### Success Response (204 No Content)
- No response body.

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |
| 403 | FORBIDDEN | Authenticated user is not an admin |
| 404 | NOT_FOUND | Joke with the given ID does not exist |

#### Error Response Example (404 Not Found)
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Joke not found."
  }
}
```

#### Notes
- This is a hard delete.
- A `204 No Content` response does not include a JSON body.

---

### PATCH /api/v1/admin/jokes/<id>/flag

Updates a joke’s flagged status.

#### Request
- **Method:** PATCH
- **Authentication:** Required
- **Authorization:** Admin only
- **Query Parameters:** None
- **Request Body:**
```json
{
  "flagged": true
}
```

#### Success Response (200 OK)
```json
{
  "data": {
    "joke": {
      "id": 1,
      "flagged": true
    }
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |
| 403 | FORBIDDEN | Authenticated user is not an admin |
| 404 | NOT_FOUND | Joke with the given ID does not exist |
| 422 | VALIDATION_ERROR | Request body missing `flagged` field |

#### Error Response Example (422 Unprocessable Entity)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request must include 'flagged' field."
  }
}
```

#### Notes
- The request body must include a `flagged` field.
- In the current implementation, `joke.flagged = bool(data["flagged"])`.
- This means non-boolean truthy or falsy values may be coerced instead of rejected.

---

## Admin User Management Endpoints

### GET /api/v1/admin/users

Returns all users visible to administrators.

#### Request
- **Method:** GET
- **Authentication:** Required
- **Authorization:** Admin only
- **Query Parameters:** None
- **Request Body:** None

#### Success Response (200 OK)
```json
{
  "data": {
    "users": [
      {
        "id": 1,
        "username": "newuser",
        "role": "user",
        "joke_count": 3
      }
    ]
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |
| 403 | FORBIDDEN | Authenticated user is not an admin |

#### Notes
- Returns an empty list (`[]`) if no users exist.
- Each user includes `id`, `username`, `role`, and `joke_count`.

---

### PATCH /api/v1/admin/users/<id>/role

Updates a user’s role.

#### Request
- **Method:** PATCH
- **Authentication:** Required
- **Authorization:** Admin only
- **Query Parameters:** None
- **Request Body:**
```json
{
  "role": "admin"
}
```

#### Success Response (200 OK)
```json
{
  "data": {
    "user": {
      "id": 1,
      "username": "newuser",
      "role": "admin"
    }
  },
  "status": "ok"
}
```

#### Error Responses
| Status | Code | When |
|--------|------|------|
| 401 | UNAUTHORIZED | No active session |
| 403 | FORBIDDEN | Authenticated user is not an admin |
| 404 | NOT_FOUND | User with the given ID does not exist |
| 422 | VALIDATION_ERROR | `role` is missing or not one of `"user"` or `"admin"` |

#### Error Response Example (422 Unprocessable Entity)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Role must be 'user' or 'admin'."
  }
}
```

#### Notes
- The only accepted role values are `"user"` and `"admin"`.
