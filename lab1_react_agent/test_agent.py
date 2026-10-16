import contextlib
import io
import unittest
from types import SimpleNamespace

from agentic_ai_lab.lab1_react_agent.agent import run_agent


class FakeMessages:
    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.responses = iter(
            [
                SimpleNamespace(
                    stop_reason="tool_use",
                    content=[
                        SimpleNamespace(
                            type="tool_use",
                            name="search_catalog",
                            input={"query": "science fiction"},
                            id="tool-call-1",
                        )
                    ],
                ),
                SimpleNamespace(
                    stop_reason="end_turn",
                    content=[
                        SimpleNamespace(
                            type="text",
                            text="Dune is available in the sample catalog.",
                        )
                    ],
                ),
            ]
        )

    def create(self, **arguments: dict) -> SimpleNamespace:
        self.calls.append(
            {
                **arguments,
                "messages": list(arguments["messages"]),
            }
        )
        return next(self.responses)


class ReActLoopTests(unittest.TestCase):
    def test_agent_sends_tool_result_back_before_final_answer(self) -> None:
        messages = FakeMessages()
        fake_client = SimpleNamespace(messages=messages)
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            answer = run_agent("Find science fiction books.", client=fake_client)

        self.assertEqual(answer, "Dune is available in the sample catalog.")
        self.assertEqual(len(messages.calls), 2)
        tool_result = messages.calls[1]["messages"][-1]["content"][0]
        self.assertEqual(tool_result["type"], "tool_result")
        self.assertEqual(tool_result["tool_use_id"], "tool-call-1")
        self.assertFalse(tool_result["is_error"])


if __name__ == "__main__":
    unittest.main()
