# API Reference

## Authentication

### Microsoft OAuth

```http
GET /auth/microsoft
```
Get Microsoft OAuth authorization URL.

```http
POST /auth/microsoft/callback
```
Handle Microsoft OAuth callback and return access token.

### Google OAuth

```http
GET /auth/google
```
Get Google OAuth authorization URL.

```http
POST /auth/google/callback
```
Handle Google OAuth callback and return access token.

## AI Processing

```http
POST /ai/process
```
Process user request through AI using Model Context Protocol (MCP).

**Request Body:**
```json
{
  "text": "string",
  "context": {
    "additional": "context",
    "data": "here"
  }
}
```

**Response:**
```json
{
  "response": "string",
  "context": {
    "user_id": "string",
    "platform": "string",
    "conversation_history": [],
    "current_task": {},
    "last_interaction": "string",
    "preferences": {}
  }
}
```

## Document Management

```http
POST /documents/create
```
Create a new document.

**Request Body:**
```json
{
  "name": "string",
  "content": "string",
  "folder_id": "string (optional)"
}
```

```http
GET /documents/{document_id}
```
Read document content.

## Email Management

```http
POST /emails/send
```
Send email.

**Request Body:**
```json
{
  "to": ["string"],
  "subject": "string",
  "body": "string",
  "cc": ["string (optional)"],
  "bcc": ["string (optional)"]
}
```

```http
GET /emails
```
Read emails from folder.

**Query Parameters:**
- `folder` (string, default: "inbox")
- `limit` (integer, default: 10)
- `query` (string, optional)

## Task Management

```http
POST /tasks/create
```
Create new task.

**Request Body:**
```json
{
  "title": "string",
  "description": "string (optional)",
  "due_date": "string (optional)",
  "list_id": "string (optional)"
}
```

```http
GET /tasks
```
Get tasks from list.

**Query Parameters:**
- `list_id` (string, optional)
- `status` (string, optional)

```http
POST /calendar/events/create
```
Create calendar event.

**Request Body:**
```json
{
  "title": "string",
  "start_time": "string",
  "end_time": "string",
  "description": "string (optional)",
  "attendees": ["string (optional)"],
  "location": "string (optional)"
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing the issue"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Authentication

All API endpoints (except OAuth endpoints) require authentication using a JWT token in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

## Rate Limiting

The API implements rate limiting based on the following rules:
- 100 requests per minute per IP address
- 1000 requests per hour per user
- 10,000 requests per day per user

## Webhooks

The API supports webhooks for real-time notifications of events. Configure webhooks in your application settings.

## SDK Support

Official SDKs are available for:
- Python
- JavaScript/TypeScript
- Java
- C#
