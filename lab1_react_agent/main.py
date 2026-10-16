"""Run Lab 1 from the project root with ``python -m ...main``."""

import argparse

from agentic_ai_lab.lab1_react_agent.agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ReAct library assistant.")
    parser.add_argument(
        "question",
        nargs="?",
        default="Find science fiction books and check whether Dune is available.",
        help="Question to ask the sample library assistant.",
    )
    question = parser.parse_args().question
    print("ANSWER:", run_agent(question))


if __name__ == "__main__":
    main()
