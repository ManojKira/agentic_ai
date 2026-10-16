"""Create and run a custom LangChain agent with explicitly bound tools."""

import os
from pathlib import Path
from typing import Any

from agentic_ai_lab.lab2_custom_agent_tools.tools import build_tools

SYSTEM_PROMPT = """You are a practical plant-care assistant.
Use the plant_care tool for plant-specific advice and watering_volume for
arithmetic. The tools return sample information and do not water real plants.
Do not invent a lookup result for unsupported plants."""
MAX_TURNS = 8


def create_model() -> Any:
    """Create the OpenRouter chat model after loading this lab's .env file."""
    from dotenv import load_dotenv

    from langchain_openrouter import ChatOpenRouter

    load_dotenv(Path(__file__).with_name(".env"))
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key or api_key == "YOUR_OPENROUTER_API_KEY_HERE":
        raise RuntimeError(
            "Set OPENROUTER_API_KEY in "
            "agentic_ai_lab/lab2_custom_agent_tools/.env before running this lab."
        )
    return ChatOpenRouter(
        model=os.getenv("MODEL", "anthropic/claude-haiku-4.5"),
        api_key=api_key,
        temperature=0,
    )


def run_agent(question: str, max_turns: int = MAX_TURNS) -> str:
    """Bind custom tools and run the model/tool loop until a final answer."""
    if not question.strip():
        raise ValueError("question cannot be empty")
    if max_turns < 1:
        raise ValueError("max_turns must be at least 1")

    from langchain_core.messages import (
        HumanMessage,
        SystemMessage,
        ToolMessage,
    )

    tools = build_tools()
    tools_by_name = {tool.name: tool for tool in tools}
    model = create_model().bind_tools(tools)
    messages = [SystemMessage(SYSTEM_PROMPT), HumanMessage(question)]

    for turn in range(1, max_turns + 1):
        assistant_message = model.invoke(messages)
        messages.append(assistant_message)
        tool_calls = assistant_message.tool_calls
        if not tool_calls:
            content = assistant_message.content
            return content if isinstance(content, str) else str(content)

        for call in tool_calls:
            tool = tools_by_name.get(call["name"])
            if tool is None:
                raise RuntimeError(f"model requested unknown tool: {call['name']}")
            print(f"[turn {turn}] {call['name']}({call['args']})")
            try:
                result = tool.invoke(call["args"])
                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=call["id"],
                    )
                )
            except (TypeError, ValueError) as error:
                messages.append(
                    ToolMessage(
                        content=f"Tool input error: {error}",
                        tool_call_id=call["id"],
                        status="error",
                    )
                )

    return f"Stopped after {max_turns} tool turns."
