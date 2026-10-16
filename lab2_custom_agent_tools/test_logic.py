import unittest

from agentic_ai_lab.lab2_custom_agent_tools.logic import (
    calculate_watering_volume,
    lookup_plant_care,
)


class PlantCareLogicTests(unittest.TestCase):
    def test_lookup_returns_care_instructions(self) -> None:
        result = lookup_plant_care("Basil")

        self.assertEqual(result["plant"], "basil")
        self.assertIn("sunlight", result["light"])

    def test_unknown_plant_is_reported(self) -> None:
        with self.assertRaisesRegex(ValueError, "supported plants"):
            lookup_plant_care("orchid")

    def test_watering_volume_is_calculated(self) -> None:
        result = calculate_watering_volume(3, 0.4)

        self.assertEqual(result["total_liters"], 1.2)

    def test_non_positive_pot_count_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 1"):
            calculate_watering_volume(0, 0.4)


if __name__ == "__main__":
    unittest.main()
