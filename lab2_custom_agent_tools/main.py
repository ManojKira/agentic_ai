"""Run Lab 2 from the project root with ``python -m ...main``."""

import argparse

from agentic_ai_lab.lab2_custom_agent_tools.agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the custom plant-care agent with tools."
    )
    parser.add_argument(
        "question",
        nargs="?",
        default="How should I care for basil, and how much water for 3 pots at 0.4 liters each?",
        help="Question to ask the plant-care assistant.",
    )
    question = parser.parse_args().question
    print("ANSWER:", run_agent(question))


if __name__ == "__main__":
    main()
