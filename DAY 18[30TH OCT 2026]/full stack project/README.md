# Online Quiz and Exam System

React JS + FastAPI + PostgreSQL. Built from docs/SDD (see the PDF in docs/).

## Run it

1. Database: `docker compose up -d db`  (PostgreSQL on port 5433)
2. Backend:
   cd backend
   .\venv\Scripts\Activate.ps1
   alembic upgrade head
   python seed.py
   uvicorn app.main:app --reload --port 8000
3. Frontend:
   cd sdd
   npm install
   npm run dev
4. Open http://localhost:5173

## Test accounts (from seed.py)

| Role | Email | Password |
|---|---|---|
| Teacher | teacher@example.com | Teacher@123 |
| Student | student1@example.com | Student@123 |
| Student | student2@example.com | Student@123 |

## Run the automated tests

   cd backend
   .\venv\Scripts\Activate.ps1
   python -m pytest -v

Results are written to TEST_RESULTS.md.