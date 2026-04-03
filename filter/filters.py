# Job title filters

# The `allow` list contains terms that you want to include in any job titles found.
# The `deny` list contains terms that you want to exclude from any job titles found.
# Try all combinations of terms to be safe, e.g. "jr" and "jr." for "junior", "sr" and "sr." for "senior", etc.

import re

allow = [
    "junior",
    "jr",
    "jr.",
    "data",
    "analyst",
    "analytics",
    "junior",
    "entry",
    "scientist",
    "ai",
    "machine learning",
    "ml",
    "ml/ai",
    "statistics",
    "statistician",
    "associate",
    "bi",
    "business intelligence",
    "reporting",
]

deny = [
    "senior",
    "sr.",
    "sr",
    "principal",
    "director",
    "president",
    "vice president",
    "vp",
    "manager",
    "staff",
    "researcher",
    "lead",
    "research",
    "director",
    "executive",
    "head",
    "software",
    "intern",
    "summer",
    "fall",
    "winter",
    "chief",
    "officer",
    "trainer",
]


def filter_title(title: str) -> bool:
    title = title.lower()

    allowed = any(re.search(rf"\b{re.escape(term)}\b", title) for term in allow)
    denied = any(re.search(rf"\b{re.escape(term)}\b", title) for term in deny)

    return allowed and not denied
