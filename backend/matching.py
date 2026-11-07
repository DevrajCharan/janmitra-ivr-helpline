from typing import Any, Optional

from db import get_all_schemes


def match_schemes(
    age: int,
    income_annual: Optional[int],
    gender: Optional[str],
    category: Optional[str],
) -> list[dict[str, Any]]:
    requested_gender = (gender or "").strip().casefold()
    matches: list[dict[str, Any]] = []
    for scheme in get_all_schemes():
        if age < (scheme["age_min"] or 0) or age > (scheme["age_max"] or 999):
            continue
        income_limit = scheme["income_annual_max"]
        if income_annual is not None and income_limit is not None and income_annual > income_limit:
            continue
        scheme_gender = (scheme["gender"] or "All").strip().casefold()
        if requested_gender and requested_gender != "all" and scheme_gender not in ("all", requested_gender):
            continue
        if category and scheme["category"] != category:
            continue
        matches.append(scheme)
    return matches
