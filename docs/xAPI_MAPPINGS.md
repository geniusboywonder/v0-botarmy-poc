# BotArmy API Mappings

**Version:** 3.0.0  
**Last Updated:** September 3, 2025  
**Base URL:** `http://localhost:8000` (Development)

## Frontend to Backend API Mapping Document

| Frontend Component                     | Expected API Endpoint                          | HTTP Method | Description                                           | Status         |
|----------------------------------------|------------------------------------------------|-------------|-------------------------------------------------------|----------------|
| `app/artifacts/page.tsx`              | `/artifacts/download/{relativePath}`          | `GET`       | Download artifact based on the relative path.       | Missing         |
|                                        | `/artifacts/structure`                        | `GET`       | Retrieve the structure of artifacts.                 | Missing         |
|                                        | `websocketService.sendArtifactPreference`     | N/A         | Send user preference for artifact download via WebSocket. | Missing         |
| `app/page.tsx`                        | `/api/status`                                 | `GET`       | Get system status and metrics.                       | Present         |
| `app/settings/page.tsx`               | `/api/config`                                 | `POST`      | Update system configuration.                          | Present         |
|                                        | `/api/config/refresh`                         | `POST`      | Refresh configuration cache from .env file.         | Present         |
| `app/interactive/sessions`            | `/api/interactive/sessions`                   | `GET`       | List all active interactive sessions.                | Present         |
|                                        | `/api/interactive/sessions/{session_id}/status` | `GET`     | Get specific session status.                         | Present         |
|                                        | `/api/interactive/sessions/{session_id}/answers` | `POST`    | Submit answers for interactive questions.            | Present         |
| `app/uploads/page.tsx`                | `/api/uploads/validate`                       | `POST`      | Validate file uploads and check rate limits.        | Present         |
|                                        | `/api/uploads/rate-limit/{identifier}`       | `GET`       | Check rate limit status for specific identifier.     | Present         |
|                                        | `/api/uploads/metrics`                        | `GET`       | Global upload metrics and statistics.                | Present         |
| `app/chat/`                            | `/api/chat/messages`                          | `GET`       | Retrieve chat messages for the current session.      | Missing         |
|                                        | `/api/chat/send`                             | `POST`      | Send a new chat message.                             | Missing         |

## Summary of Findings
- **Missing Endpoints**: The following endpoints are expected by the frontend but are currently missing in the backend:
  - `/artifacts/download/{relativePath}`
  - `/artifacts/structure`
  - `websocketService.sendArtifactPreference`
  - `/api/chat/messages`
  - `/api/chat/send`

- **Present Endpoints**: The following endpoints are correctly implemented and mapped:
  - `/api/status`
  - `/api/config`
  - `/api/interactive/sessions`
  - `/api/uploads/validate`
  - `/api/uploads/rate-limit/{identifier}`
  - `/api/uploads/metrics`

## Recommendations
1. **Implement Missing Endpoints**: Work with the backend team to implement the missing endpoints to ensure that the frontend can function correctly.
2. **Update API Documentation**: Ensure that the API documentation is updated to reflect the new endpoints once they are implemented.
3. **Test Integration**: After implementing the missing endpoints, conduct integration tests to verify that the frontend components can successfully communicate with the backend.

---

**Document Created on**: September 3, 2025