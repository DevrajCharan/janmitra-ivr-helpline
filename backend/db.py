import os
import sqlite3
from pathlib import Path
from typing import Any, Optional


def get_db_connection() -> sqlite3.Connection:
    default_path = Path(__file__).resolve().parent.parent / "data" / "janmitra_schemes.db"
    connection = sqlite3.connect(Path(os.getenv("DB_PATH", str(default_path))))
    connection.row_factory = sqlite3.Row
    return connection


def _read_all(query: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with get_db_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [dict(row) for row in rows]


def get_all_schemes() -> list[dict[str, Any]]:
    return _read_all("SELECT * FROM schemes ORDER BY category, scheme_name")


def get_scheme_by_id(scheme_id: int) -> Optional[dict[str, Any]]:
    rows = _read_all("SELECT * FROM schemes WHERE id = ?", (scheme_id,))
    return rows[0] if rows else None


def search_schemes(
    query: str, category: Optional[str], page: int, limit: int
) -> dict[str, Any]:
    filters: list[str] = []
    parameters: list[Any] = []
    if query.strip():
        pattern = f"%{query.strip()}%"
        filters.append(
            "(scheme_name LIKE ? OR hindi_name LIKE ? OR category LIKE ? "
            "OR benefits LIKE ? OR benefit_amount LIKE ? OR ministry LIKE ? "
            "OR beneficiary_type LIKE ?)"
        )
        parameters.extend([pattern] * 7)
    if category:
        filters.append("category = ?")
        parameters.append(category)
    where_clause = f" WHERE {' AND '.join(filters)}" if filters else ""
    with get_db_connection() as connection:
        total = connection.execute(
            f"SELECT COUNT(*) FROM schemes{where_clause}", parameters
        ).fetchone()[0]
        offset = (page - 1) * limit
        rows = connection.execute(
            f"SELECT * FROM schemes{where_clause} ORDER BY category, scheme_name "
            "LIMIT ? OFFSET ?",
            (*parameters, limit, offset),
        ).fetchall()
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "schemes": [dict(row) for row in rows],
    }


def get_categories_with_count() -> list[dict[str, Any]]:
    return _read_all(
        "SELECT category, COUNT(*) AS count FROM schemes "
        "GROUP BY category ORDER BY category"
    )
