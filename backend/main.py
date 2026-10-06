from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from typing import List, Dict, Any, Optional

app = FastAPI(
    title="JanMitra API",
    description="Backend API for JanMitra — AI-powered Government Schemes Helpline (EPICS 2027, VIT Bhopal)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'janmitra_schemes.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ── Root ──────────────────────────────────────────────────────────────
@app.get("/")
def read_root():
    return {
        "project": "JanMitra Call",
        "team": "EPICS 2027 — VIT Bhopal University",
        "version": "2.0.0",
        "endpoints": ["/schemes", "/schemes/{id}", "/categories", "/search", "/match", "/stats"]
    }

# ── All schemes (optional category filter) ────────────────────────────
@app.get("/schemes", response_model=List[Dict[str, Any]])
def get_schemes(category: Optional[str] = Query(None, description="Filter by category")):
    conn = get_db_connection()
    cursor = conn.cursor()
    if category:
        cursor.execute('SELECT * FROM schemes WHERE category = ? ORDER BY scheme_name', (category,))
    else:
        cursor.execute('SELECT * FROM schemes ORDER BY category, scheme_name')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ── Single scheme by ID ───────────────────────────────────────────────
@app.get("/schemes/{scheme_id}", response_model=Dict[str, Any])
def get_scheme(scheme_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schemes WHERE id = ?', (scheme_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return dict(row)

# ── All distinct categories ────────────────────────────────────────────
@app.get("/categories")
def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT category, COUNT(*) as count FROM schemes GROUP BY category ORDER BY count DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{"category": r["category"], "count": r["count"]} for r in rows]

# ── Full-text search ──────────────────────────────────────────────────
@app.get("/search", response_model=List[Dict[str, Any]])
def search_schemes(q: str = Query(..., description="Search keyword")):
    conn = get_db_connection()
    cursor = conn.cursor()
    like = f"%{q}%"
    cursor.execute('''
        SELECT * FROM schemes
        WHERE scheme_name LIKE ? OR hindi_name LIKE ? OR category LIKE ?
           OR benefits LIKE ? OR beneficiary_type LIKE ? OR ministry LIKE ?
        ORDER BY scheme_name
    ''', (like, like, like, like, like, like))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ── Eligibility matcher (age + income) ────────────────────────────────
@app.get("/match", response_model=List[Dict[str, Any]])
def match_schemes(
    age: int = Query(..., description="Applicant age in years"),
    income: Optional[int] = Query(None, description="Annual income in rupees"),
    gender: Optional[str] = Query(None, description="Male / Female / All"),
    category: Optional[str] = Query(None, description="Filter by category")
):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM schemes WHERE age_min <= ? AND age_max >= ?'
    params: list = [age, age]

    if gender and gender.lower() in ("female", "woman", "महिला"):
        query += " AND (gender = 'Female' OR gender = 'All')"
    else:
        query += " AND gender = 'All' OR gender IS NULL OR gender = ''"

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY category, scheme_name"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ── Summary stats (for dashboard) ─────────────────────────────────────
@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    total = cursor.execute("SELECT COUNT(*) FROM schemes").fetchone()[0]
    cats  = cursor.execute("SELECT COUNT(DISTINCT category) FROM schemes").fetchone()[0]
    active = cursor.execute("SELECT COUNT(*) FROM schemes WHERE status='Active'").fetchone()[0]
    ministries = cursor.execute("SELECT COUNT(DISTINCT ministry) FROM schemes").fetchone()[0]
    conn.close()
    return {
        "total_schemes": total,
        "categories": cats,
        "active_schemes": active,
        "ministries_covered": ministries
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

