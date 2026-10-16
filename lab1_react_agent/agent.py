"""A ReAct loop using the Anthropic messages API through OpenRouter."""

import os
from pathlib import Path
from typing import Any

from agentic_ai_lab.lab1_react_agent.tools import TOOLS, run_tool

SYSTEM_PROMPT = """You are a helpful librarian using a small sample catalog.
Use tools to search the catalog and check availability when useful.
The tools use sample data and cannot reserve, borrow, or modify real books.
Explain what you found and state when a requested book is unavailable."""
MAX_TURNS = 8


def create_client() -> Any:
    """Load local configuration and create the API client."""
    from dotenv import load_dotenv

    from anthropic import Anthropic

    load_dotenv(Path(__file__).with_name(".env"))
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY_HERE":
        raise RuntimeError(
            "Set OPENROUTER_API_KEY in "
            "agentic_ai_lab/lab1_react_agent/.env before running this lab."
        )
    return Anthropic(
        api_key=api_key,
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api"),
    )


def run_agent(
    question: str,
    client: Any | None = None,
    max_turns: int = MAX_TURNS,
) -> str:
    """Run the ReAct cycle until the model responds or the turn limit is reached."""
    if not question.strip():
        raise ValueError("question cannot be empty")
    if max_turns < 1:
        raise ValueError("max_turns must be at least 1")

    if client is None:
        client = create_client()

    messages: list[dict[str, Any]] = [{"role": "user", "content": question}]
    model = os.getenv("MODEL", "anthropic/claude-haiku-4.5")

    for turn in range(1, max_turns + 1):
        response = client.messages.create(
            model=model,
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return "\n".join(
                block.text
                for block in response.content
                if getattr(block, "type", None) == "text"
            )

        tool_results = []
        for block in response.content:
            if getattr(block, "type", None) != "tool_use":
                continue
            output, is_error = run_tool(block.name, block.input)
            print(f"[turn {turn}] {block.name}({block.input}) -> {output}")
            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": is_error,
                }
            )
        if not tool_results:
            raise RuntimeError("model requested tool use but supplied no tool calls")
        messages.append({"role": "user", "content": tool_results})

    return f"Stopped after {max_turns} tool turns."
