"""Integration tests for the API."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Mock swisseph to avoid import error
mock_swe = MagicMock()
mock_swe.julday.return_value = 2448029.020833
mock_swe.houses.return_value = ([0]*13, 0, 0, 0, 0)  # cusps, asc, mc, armc, vertex
mock_swe.calc_ut.return_value = ((56.45, 0, 0, 1.0, 0), 0)  # pos, flag
mock_swe.house_pos.return_value = 9
with patch.dict('sys.modules', {'swisseph': mock_swe}):
    from src.core.domain.models import NatalChart, Planet, House, Aspect
    from src.interfaces.api.main import app
    import src.interfaces.api.v1 as v1_module  # Ensure v1 is imported for patching


@pytest.fixture
def client():
    """Test client fixture."""
    yield TestClient(app)


def test_calculate_chart(client):
    """Test the /api/v1/chart/calculate endpoint."""
    request_data = {
        "date": "1990-05-17",
        "time": "12:30",
        "latitude": 44.4268,
        "longitude": 26.1025,
        "timezone": "Europe/Bucharest"
    }
    response = client.post("/api/v1/chart/calculate", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "meta" in data
    assert "julian_day" in data["meta"]
    assert "planets" in data
    assert len(data["planets"]) > 0
    assert "houses" in data
    assert len(data["houses"]) == 12
    assert "aspects" in data


def test_generate_personal_horoscope(client):
    """Test the /api/v1/horoscope/personal endpoint."""
    from src.core.domain.models import HoroscopeOutput, NatalChart, Interpretation, Planet

    # Mock the use case
    mock_chart = NatalChart(
        julian_day=2448029.020833,
        planets=[Planet(name="Sun", sign="Leo", longitude=135.0, house=5, is_retrograde=False)],
        houses=[],
        aspects=[]
    )
    mock_interpretation = Interpretation(
        traits=["Creative"],
        strengths=["Artistic"],
        challenges=["Impatient"]
    )
    mock_output = HoroscopeOutput(
        chart=mock_chart,
        interpretation=mock_interpretation,
        ai_text="AI generated horoscope text"
    )

    with patch.object(v1_module, 'get_generate_horoscope_use_case') as mock_get_use_case, \
         patch('src.infrastructure.ai.gemini_adapter.GeminiAdapter.generate_text', return_value="Mocked AI text"):
        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = mock_output
        mock_get_use_case.return_value = mock_use_case

        request_data = {
            "profile": {
                "name": "Alex",
                "birth_date": "1990-05-17",
                "birth_time": "12:30",
                "latitude": 44.4268,
                "longitude": 26.1025
            },
            "preferences": {
                "tone": "spiritual",
                "focus": "career",
                "language": "en"
            }
        }
        response = client.post("/api/v1/horoscope/personal", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert "chart" in data
        assert "interpretation" in data
        assert "traits" in data["interpretation"]
        assert "strengths" in data["interpretation"]
        assert "challenges" in data["interpretation"]
        assert "ai_text" in data
        assert data["ai_text"] == "AI generated horoscope text"


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}