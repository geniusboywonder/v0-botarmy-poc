# Architecture Document

## Technology Stack:
- Frontend Framework: React.js
- Backend Language: Node.js
- Database: SQLite

## System Components:
1. Frontend App:
   - Responsible for user input, displaying calculations, and results.
   - Built using React.js for a responsive and interactive user interface.

2. API Server:
   - Handles calculation logic and data processing.
   - Implemented in Node.js to provide a fast and efficient backend service.

3. Database:
   - SQLite database for storing user sessions and calculation history.
   - Provides data persistence and retrieval for user interactions.

## Data Model:
- UserSession:
  - id (Primary Key)
  - timestamp
  - input_expression
  - result

## API Endpoints:
1. `POST /api/calculate`
   - Description: Performs the requested calculation based on user input.
   - Request Body: { input: "2+3" }
   - Response: { result: 5 }

2. `GET /api/history`
   - Description: Retrieves the history of past calculations.
   - Response: [{ input: "2+3", result: 5 }, { input: "4*5", result: 20 }]

3. `DELETE /api/history/:id`
   - Description: Deletes a specific calculation from the history.
   - Response: { message: "Calculation deleted successfully" }

## Security Considerations:
- Use HTTPS for secure communication between frontend and backend.
- Implement input validation to prevent injection attacks.
- Encrypt sensitive data stored in the database.
- Follow best practices for handling user sessions and authentication.

By following this architecture, we ensure a scalable, secure, and efficient calculator app that meets the project requirements while providing a seamless user experience.