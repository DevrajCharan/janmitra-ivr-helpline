# JanMitra Project

JanMitra is an AI-powered Government Schemes Helpline developed for EPICS 2027.

## Repository Structure

- `backend/`: Contains the FastAPI backend and database setup scripts.
- `frontend/`: Contains the UI/web interface.
- `data/`: Contains the SQLite database and exported CSV/Excel data files.
- `docs/`: Contains project documentation, literature review, and reports.

## Setup Instructions

### 1. Database Setup
```bash
cd backend
python setup_database.py
```
This will create `janmitra_schemes.db` in the `data/` folder.

### 2. Backend Server
Install dependencies and run the FastAPI server:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### 3. Frontend
Open `frontend/index.html` in any web browser. Make sure the backend server is running so the frontend can fetch the schemes.
