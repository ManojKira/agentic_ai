import unittest

from agentic_ai_lab.lab1_react_agent.tools import (
    check_availability,
    run_tool,
    search_catalog,
)


class LibraryToolTests(unittest.TestCase):
    def test_search_finds_books_by_genre(self) -> None:
        results = search_catalog("science fiction")

        self.assertEqual(
            [book["title"] for book in results],
            ["Dune", "The Left Hand of Darkness"],
        )

    def test_availability_returns_copy_count(self) -> None:
        self.assertEqual(check_availability("Dune")["available_copies"], 2)

    def test_unknown_book_is_reported(self) -> None:
        with self.assertRaisesRegex(ValueError, "book not found"):
            check_availability("Unknown Book")

    def test_tool_dispatch_reports_invalid_arguments(self) -> None:
        result, is_error = run_tool("check_availability", {})

        self.assertTrue(is_error)
        self.assertIn("title", result)


if __name__ == "__main__":
    unittest.main()
