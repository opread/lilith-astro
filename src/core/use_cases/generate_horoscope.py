"""Use case for generating a complete horoscope including AI text."""

import json

from src.core.domain.models import BirthData, HoroscopeOutput
from src.core.domain.prompts import NATAL_HOROSCOPE_PROMPT
from src.core.use_cases.calculate_chart import CalculateChartUseCase
from src.core.use_cases.interpret_chart import interpret_chart
from src.infrastructure.ai.gemini_adapter import GeminiAdapter


class GenerateHoroscopeUseCase:
    """Use case to generate a complete horoscope with AI text."""

    def __init__(self, calculate_use_case: CalculateChartUseCase, ai_adapter: GeminiAdapter):
        """Initialize with dependencies.

        Args:
            calculate_use_case: Use case for calculating the chart.
            ai_adapter: AI adapter for text generation.
        """
        self.calculate_use_case = calculate_use_case
        self.ai_adapter = ai_adapter

    def execute(self, birth_data: BirthData) -> HoroscopeOutput:
        """Execute the use case to generate the horoscope.

        Args:
            birth_data: The birth data for the horoscope.

        Returns:
            HoroscopeOutput: The complete horoscope output.
        """
        chart = self.calculate_use_case.execute(birth_data)
        interpretation = interpret_chart(chart)

        # Prepare prompt
        chart_dict = chart.model_dump()
        chart_json = json.dumps(chart_dict, indent=2)
        prompt = NATAL_HOROSCOPE_PROMPT.format(chart_json=chart_json)

        # Generate AI text
        ai_text = self.ai_adapter.generate_text(prompt)

        return HoroscopeOutput(
            chart=chart,
            interpretation=interpretation,
            ai_text=ai_text
        )