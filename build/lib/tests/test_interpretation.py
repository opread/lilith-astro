"""Unit tests for interpretation use case."""

import pytest

from src.core.domain.models import Aspect, House, Interpretation, NatalChart, Planet
from src.core.use_cases.interpret_chart import interpret_chart


class TestInterpretChart:
    """Test cases for interpret_chart function."""

    def test_interpret_chart_with_planets(self):
        """Test interpretation with planets in specific signs and houses."""
        planets = [
            Planet(name="Sun", sign="Aries", longitude=10.0, house=1, is_retrograde=False),
            Planet(name="Moon", sign="Taurus", longitude=20.0, house=2, is_retrograde=False)
        ]
        houses = [
            House(number=1, degree=0.0, sign="Aries"),
            House(number=2, degree=30.0, sign="Taurus")
        ]
        aspects = []
        chart = NatalChart(planets=planets, houses=houses, aspects=aspects)

        result = interpret_chart(chart)

        assert isinstance(result, Interpretation)
        assert "bold" in result.traits
        assert "energetic" in result.traits
        assert "leadership" in result.strengths
        assert "practical" in result.traits
        assert "reliable" in result.traits
        assert "stability" in result.strengths
        assert "self-identity" in result.traits
        assert "values" in result.traits

    def test_interpret_chart_with_aspects(self):
        """Test interpretation with aspects."""
        planets = []
        houses = []
        aspects = [
            Aspect(planet1="Sun", planet2="Mars", type="conjunct", orb=1.0),
            Aspect(planet1="Venus", planet2="Saturn", type="square", orb=2.0)
        ]
        chart = NatalChart(planets=planets, houses=houses, aspects=aspects)

        result = interpret_chart(chart)

        assert "intensified" in result.traits
        assert "focus" in result.strengths
        assert "challenging" in result.traits
        assert "growth" in result.strengths

    def test_interpret_chart_empty_chart(self):
        """Test interpretation with empty chart."""
        chart = NatalChart(planets=[], houses=[], aspects=[])

        result = interpret_chart(chart)

        assert result.traits == []
        assert result.strengths == []
        assert result.challenges == []

    def test_interpret_chart_unique_items(self):
        """Test that duplicate traits are not added."""
        planets = [
            Planet(name="Sun", sign="Aries", longitude=10.0, house=1, is_retrograde=False),
            Planet(name="Mars", sign="Aries", longitude=15.0, house=1, is_retrograde=False)
        ]
        houses = []
        aspects = []
        chart = NatalChart(planets=planets, houses=houses, aspects=aspects)

        result = interpret_chart(chart)

        # Should not have duplicates
        assert len(result.traits) == len(set(result.traits))
        assert "bold" in result.traits
        assert result.traits.count("bold") == 1