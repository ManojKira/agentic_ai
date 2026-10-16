"""LangChain tool definitions for the plant-care assistant."""

from agentic_ai_lab.lab2_custom_agent_tools.logic import (
    calculate_watering_volume,
    lookup_plant_care,
)


def build_tools() -> list[object]:
    """Create LangChain tools; imports are lazy so local logic stays testable."""
    from langchain_core.tools import tool

    @tool
    def plant_care(plant_name: str) -> dict:
        """Look up sample sunlight, watering, and care advice for a plant."""
        return lookup_plant_care(plant_name)

    @tool
    def watering_volume(number_of_pots: int, liters_per_pot: float) -> dict:
        """Calculate the total suggested water volume for a number of pots."""
        return calculate_watering_volume(number_of_pots, liters_per_pot)

    return [plant_care, watering_volume]
