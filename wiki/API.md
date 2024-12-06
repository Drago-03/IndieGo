# API Documentation

## Overview

The DevAssist bot provides a RESTful API for enterprise subscribers to integrate bot functionality into their own applications.

## Authentication

```http
POST /api/auth
Content-Type: application/json

{
    "api_key": "your_api_key_here"
}
```

Response:
```json
{
    "token": "jwt_token_here",
    "expires_in": 3600
}
```

## Endpoints

### Code Analysis

#### Request Code Review
```http
POST /api/code/review
Authorization: Bearer <token>
Content-Type: application/json

{
    "code": "def example():\n    return True",
    "language": "python"
}
```

Response:
```json
{
    "complexity": 1,
    "suggestions": [...],
    "security_issues": [...],
    "performance_tips": [...]
}
```

### Project Management

#### Create Project Structure
```http
POST /api/project/create
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "my-project",
    "template": "python-web"
}
```

Response:
```json
{
    "structure": [...],
    "setup_instructions": [...]
}
```

## Rate Limits

- Free Tier: 100 requests/day
- Pro Tier: 1000 requests/day
- Enterprise Tier: Unlimited

## Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 429: Too Many Requests
- 500: Internal Server Error

## WebSocket Events

```javascript
// Connect to WebSocket
const ws = new WebSocket('wss://api.devassist.com/ws');

// Subscribe to events
ws.send(JSON.stringify({
    type: 'subscribe',
    events: ['code_review', 'project_update']
}));
```

## Examples

### Python
```python
import requests

api_key = 'your_api_key'
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.post(
    'https://api.devassist.com/code/review',
    headers=headers,
    json={'code': 'print("Hello")'}
)

print(response.json())
```