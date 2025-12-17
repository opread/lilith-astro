"""Use case for calculating natal charts."""

from src.core.domain.models import BirthData, NatalChart
from src.infrastructure.astro_engine.swiss_ephemeris import SwissEphemerisEngine


class CalculateChartUseCase:
    """Use case to calculate a natal chart."""

    def __init__(self, astro_engine: SwissEphemerisEngine):
        """Initialize with the astro engine.

        Args:
            astro_engine: The astro engine to use for calculations.
        """
        self.astro_engine = astro_engine

    def execute(self, birth_data: BirthData) -> NatalChart:
        """Execute the use case to calculate the chart.

        Args:
            birth_data: The birth data for the chart.

        Returns:
            NatalChart: The calculated natal chart.
        """
        return self.astro_engine.calculate_chart(birth_data)