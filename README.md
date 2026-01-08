1. Problem Understanding & Assumptions

🔍 Interpretation
* Exposes exactly four endpoints (POST, GET, PUT, DELETE)
* Persists all data in a relational database
* Integrates with at least one external API
* Enforces strict request and response validation
* Uses proper HTTP status codes
* Includes automated tests

🎯 Use Case 
The system allows users to register GitHub repositories into a local PostgreSQL database by fetching real-time data from the GitHub Public API.
Once stored, repositories can be retrieved, updated, or deleted via REST endpoints.
chosen because:
    GitHub API is reliable and public
    Demonstrates real external API integration

⚠️ Assumptions
External API Reliability
    GitHub Public API is assumed to be available most of the time.
    If GitHub is unavailable or returns an error, the request fails gracefully.


2. Design Decision

🗄 Database Schema
| Column      | Type         | Reason            |
| ----------- | ------------ | ----------------- |
| id          | Integer (PK) | Unique identifier |
| name        | String       | Repository name   |
| owner       | String       | Repository owner  |
| stars       | Integer      | Popularity metric |
| description | String       | Optional metadata |
| created_at  | Timestamp    | Audit & tracking  |

Indexing:
    Primary key index on id
    Optimized for read-heavy operations (GET by ID)

🏗 Project Structure
app/
├── main.py              # Application entry point
├── database.py          # DB engine & session
├── models.py            # SQLAlchemy ORM models
├── schemas.py           # Pydantic validation models
├── crud.py              # DB operations abstraction
├── api/
│   └── repositories.py # Route definitions
tests/
└── test_repositories.py

✅ Validation Logic
Pydantic models enforce:
    Minimum string lengths
    Non-negative numeric values
response_model ensures output integrity
Invalid input automatically triggers 422 Unprocessable Entity

🌐 External API Design
External Service: GitHub REST API


3. Solution Approach

*  POST /repositories
    Client submits GitHub owner & repo name
    API fetches data from GitHub
    Validated data is stored in PostgreSQL
*  GET /repositories/{id}
    Data fetched directly from PostgreSQL
    Returned using response schema
*  PUT /repositories/{id}
    Partial update using validated input
    Changes persisted to DB
*  DELETE /repositories/{id}
    Entity removed from DB
    No content returned


4. Error Handling Stretegy

🔴 Database Errors
🌐 External API Failures
❌ Application Errors

FastAPI’s built-in exception handling ensures consistent error responses without custom middleware.


5. How to run the project

🔧 Setup Instructions
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Required Environment
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/github_db

🔗 Example API Calls
curl -X POST http://127.0.0.1:8000/repositories \
-H "Content-Type: application/json" \
-d '{"owner": "tiangolo", "repo": "fastapi"}'

curl http://127.0.0.1:8000/repositories/1

Run:
   Pytest -v
