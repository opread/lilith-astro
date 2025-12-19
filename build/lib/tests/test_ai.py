"""Tests for AI components."""

import pytest
from unittest.mock import MagicMock, patch

# Mock swisseph to avoid import error
mock_swe = MagicMock()
mock_swe.julday.return_value = 2448029.020833
mock_swe.houses.return_value = ([0]*13, 0, 0, 0, 0)  # cusps, asc, mc, armc, vertex
mock_swe.calc_ut.return_value = ((56.45, 0, 0, 1.0, 0), 0)  # pos, flag
mock_swe.house_pos.return_value = 9
with patch.dict('sys.modules', {'swisseph': mock_swe}):
    from src.core.domain.models import BirthData, HoroscopeOutput, Interpretation, NatalChart, Planet
    from src.core.use_cases import generate_horoscope
    from src.core.use_cases.generate_horoscope import GenerateHoroscopeUseCase
    from src.infrastructure.ai.gemini_adapter import GeminiAdapter


class TestGeminiAdapter:
    """Unit tests for GeminiAdapter."""

    def test_generate_text(self):
        """Test generating text with mocked AI."""
        adapter = GeminiAdapter(api_key="fake_key")
        with patch.object(adapter.client.models, 'generate_content') as mock_generate:
            mock_response = MagicMock()
            mock_response.text = "Generated horoscope text"
            mock_generate.return_value = mock_response

            result = adapter.generate_text("Test prompt")

            assert result == "Generated horoscope text"
            mock_generate.assert_called_once_with(model=adapter.model_name, contents="Test prompt")


class TestGenerateHoroscopeUseCase:
    """Integration tests for GenerateHoroscopeUseCase."""

    def test_execute(self):
        """Test the full use case execution."""
        # Mock calculate use case
        mock_calculate_uc = MagicMock()
        mock_chart = NatalChart(
            planets=[Planet(name="Sun", sign="Leo", longitude=135.0, house=5, is_retrograde=False)],
            houses=[],
            aspects=[]
        )
        mock_calculate_uc.execute.return_value = mock_chart

        # Mock interpretation
        mock_interpretation = Interpretation(traits=["Creative"], strengths=["Artistic"], challenges=["Impatient"])

        # Mock AI
        ai_adapter = GeminiAdapter(api_key="fake_key")

        with patch.object(generate_horoscope, 'interpret_chart', return_value=mock_interpretation), \
             patch.object(ai_adapter, 'generate_text', return_value="AI generated horoscope"):

            use_case = GenerateHoroscopeUseCase(mock_calculate_uc, ai_adapter)

            birth_data = BirthData(date="1990-05-17", time="12:00", lat=44.4, lon=26.1, timezone="UTC")
            result = use_case.execute(birth_data)

            assert isinstance(result, HoroscopeOutput)
            assert result.chart == mock_chart
            assert result.interpretation == mock_interpretation
            assert result.ai_text == "AI generated horoscope"

            mock_calculate_uc.execute.assert_called_once_with(birth_data)