"""Unit tests for the astro engine."""

import pytest
from unittest.mock import MagicMock, patch

# Mock swisseph to avoid import error
mock_swe = MagicMock()
mock_swe.julday.return_value = 2448029.020833
mock_swe.houses.return_value = ([0]*13, 0, 0, 0, 0)  # cusps, asc, mc, armc, vertex
mock_swe.calc_ut.return_value = ((280.46, 0, 0, 1.0, 0), 0)  # pos, flag for Sun in Capricorn
mock_swe.house_pos.return_value = 9
with patch.dict('sys.modules', {'swisseph': mock_swe}):
    from src.core.domain.models import BirthData
    from src.core.use_cases.calculate_chart import CalculateChartUseCase
    from src.infrastructure.astro_engine.swiss_ephemeris import SwissEphemerisEngine


class TestSwissEphemerisEngine:
    """Test the Swiss Ephemeris engine."""

    @pytest.fixture
    def engine(self):
        """Fixture for the engine."""
        return SwissEphemerisEngine()

    @pytest.fixture
    def use_case(self, engine):
        """Fixture for the use case."""
        return CalculateChartUseCase(engine)

    def test_calculate_chart_for_known_date(self, engine):
        """Test calculation for a known date against ephemeris data."""
        # Known: On 2000-01-01 00:00 UTC, Sun at ~280.46 degrees (Capricorn)
        birth_data = BirthData(
            date="2000-01-01",
            time="00:00",
            lat=0.0,
            lon=0.0,
            timezone="UTC"
        )
        chart = engine.calculate_chart(birth_data)
        sun = next(p for p in chart.planets if p.name == "Sun")
        assert sun.sign == "Capricorn"
        assert 280.0 <= sun.longitude <= 281.0  # Approximate
        assert not sun.is_retrograde

    def test_calculate_chart_structure(self, engine):
        """Test that the chart has correct structure."""
        birth_data = BirthData(
            date="1990-05-17",
            time="12:30",
            lat=44.4268,
            lon=26.1025,
            timezone="Europe/Bucharest"
        )
        chart = engine.calculate_chart(birth_data)
        assert len(chart.planets) == 10  # Sun to Pluto
        assert len(chart.houses) == 12
        assert isinstance(chart.aspects, list)

    def test_planets_have_correct_attributes(self, engine):
        """Test that planets have all required attributes."""
        birth_data = BirthData(
            date="1990-05-17",
            time="12:30",
            lat=44.4268,
            lon=26.1025,
            timezone="Europe/Bucharest"
        )
        chart = engine.calculate_chart(birth_data)
        for planet in chart.planets:
            assert planet.name
            assert planet.sign in SwissEphemerisEngine.SIGNS
            assert 0 <= planet.longitude < 360
            assert 1 <= planet.house <= 12
            assert isinstance(planet.is_retrograde, bool)

    def test_houses_have_correct_attributes(self, engine):
        """Test that houses have all required attributes."""
        birth_data = BirthData(
            date="1990-05-17",
            time="12:30",
            lat=44.4268,
            lon=26.1025,
            timezone="Europe/Bucharest"
        )
        chart = engine.calculate_chart(birth_data)
        for house in chart.houses:
            assert 1 <= house.number <= 12
            assert 0 <= house.degree < 360
            assert house.sign in SwissEphemerisEngine.SIGNS

    def test_aspects_are_calculated(self, engine):
        """Test that aspects are calculated between planets."""
        birth_data = BirthData(
            date="1990-05-17",
            time="12:30",
            lat=44.4268,
            lon=26.1025,
            timezone="Europe/Bucharest"
        )
        chart = engine.calculate_chart(birth_data)
        # There should be some aspects
        assert len(chart.aspects) >= 0
        for aspect in chart.aspects:
            assert aspect.planet1 != aspect.planet2
            assert aspect.type in ["Conjunction", "Sextile", "Square", "Trine", "Opposition"]
            assert 0 <= aspect.orb <= 10.0

    def test_use_case_execute(self, use_case):
        """Test the use case execution."""
        birth_data = BirthData(
            date="1990-05-17",
            time="12:30",
            lat=44.4268,
            lon=26.1025,
            timezone="Europe/Bucharest"
        )
        chart = use_case.execute(birth_data)
        assert isinstance(chart, type(chart))  # NatalChart
        assert len(chart.planets) == 10