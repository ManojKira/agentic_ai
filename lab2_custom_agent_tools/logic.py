"""Sample plant-care knowledge and deterministic calculations."""

from typing import Any

PLANTS: dict[str, dict[str, Any]] = {
    "basil": {
        "light": "6-8 hours of direct sunlight each day",
        "watering": "Water when the top 2 cm of soil feels dry.",
        "notes": "Pinch off flower buds to encourage leaf growth.",
    },
    "snake plant": {
        "light": "Bright indirect light; it also tolerates low light.",
        "watering": "Let the soil dry completely between waterings.",
        "notes": "Avoid leaving the pot in standing water.",
    },
    "tomato": {
        "light": "At least 6 hours of direct sunlight each day",
        "watering": "Keep soil evenly moist and water near the soil line.",
        "notes": "Support the plant as it grows.",
    },
}


def lookup_plant_care(plant_name: str) -> dict[str, Any]:
    """Look up sample care advice for a supported plant."""
    normalized = plant_name.strip().casefold()
    if not normalized:
        raise ValueError("plant_name cannot be empty")
    care = PLANTS.get(normalized)
    if care is None:
        raise ValueError(
            f"unknown plant; supported plants: {', '.join(sorted(PLANTS))}"
        )
    return {"plant": normalized, **care}


def calculate_watering_volume(
    number_of_pots: int, liters_per_pot: float
) -> dict[str, int | float]:
    """Calculate a suggested total volume; this does not control real watering."""
    if number_of_pots < 1:
        raise ValueError("number_of_pots must be at least 1")
    if liters_per_pot <= 0:
        raise ValueError("liters_per_pot must be greater than zero")
    return {
        "number_of_pots": number_of_pots,
        "liters_per_pot": liters_per_pot,
        "total_liters": round(number_of_pots * liters_per_pot, 2),
    }
