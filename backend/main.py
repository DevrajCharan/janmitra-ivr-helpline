from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from db import get_categories_with_count, get_scheme_by_id, search_schemes
from matching import match_schemes

app = FastAPI(title="JanMitra API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchRequest(BaseModel):
    age: int = Field(ge=1, le=120)
    income_annual: Optional[int] = Field(default=None, ge=0)
    gender: Optional[str] = None
    category: Optional[str] = None


@app.get("/")
def read_root():
    return {"project": "JanMitra", "endpoints": ["/api/schemes", "/api/match", "/api/categories"]}


@app.get("/api/schemes")
def read_schemes(
    search: str = Query(default=""),
    category: Optional[str] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
):
    return search_schemes(search, category, page, limit)


@app.get("/api/schemes/{scheme_id}")
def read_scheme(scheme_id: int):
    scheme = get_scheme_by_id(scheme_id)
    if scheme is None:
        raise HTTPException(status_code=404, detail="Scheme not found / योजना नहीं मिली")
    return scheme


@app.get("/api/categories")
def read_categories():
    return get_categories_with_count()


@app.post("/api/match")
def read_matches(criteria: MatchRequest):
    schemes = match_schemes(
        criteria.age, criteria.income_annual, criteria.gender, criteria.category
    )
    return {"matched": len(schemes), "schemes": schemes}
