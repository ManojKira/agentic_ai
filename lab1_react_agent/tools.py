"""Local library tools for the ReAct agent."""

import json
from typing import Any


CATALOG = (
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "science fiction",
        "available_copies": 2,
    },
    {
        "title": "The Left Hand of Darkness",
        "author": "Ursula K. Le Guin",
        "genre": "science fiction",
        "available_copies": 0,
    },
    {
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "genre": "fantasy",
        "available_copies": 1,
    },
)

TOOLS = [
    {
        "name": "search_catalog",
        "description": "Find books by title, author, or genre in the sample library catalog.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Text to search for."}
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "check_availability",
        "description": "Check how many copies of a specific book are available.",
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Exact book title."}
            },
            "required": ["title"],
            "additionalProperties": False,
        },
    },
]


def search_catalog(query: str) -> list[dict[str, Any]]:
    """Search sample books by title, author, or genre."""
    normalized = query.strip().casefold()
    if not normalized:
        raise ValueError("query cannot be empty")
    matches = [
        book
        for book in CATALOG
        if normalized
        in f"{book['title']} {book['author']} {book['genre']}".casefold()
    ]
    return matches


def check_availability(title: str) -> dict[str, Any]:
    """Return the sample inventory count for an exact book title."""
    normalized = title.strip().casefold()
    if not normalized:
        raise ValueError("title cannot be empty")
    for book in CATALOG:
        if book["title"].casefold() == normalized:
            return {
                "title": book["title"],
                "available_copies": book["available_copies"],
                "available": book["available_copies"] > 0,
            }
    raise ValueError(f"book not found: {title}")


FUNCTIONS = {
    "search_catalog": search_catalog,
    "check_availability": check_availability,
}


def run_tool(name: str, arguments: dict[str, Any]) -> tuple[str, bool]:
    """Run a named tool and encode its result for the model's tool protocol."""
    function = FUNCTIONS.get(name)
    if function is None:
        return json.dumps({"error": f"unknown tool: {name}"}), True
    try:
        return json.dumps(function(**arguments)), False
    except (TypeError, ValueError) as error:
        return json.dumps({"error": str(error)}), True
