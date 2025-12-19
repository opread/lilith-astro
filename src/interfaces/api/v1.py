"""API v1 router."""

from fastapi import APIRouter, Depends

from src.config.settings import Settings
from src.core.domain.models import BirthData, HoroscopeOutput, NatalChart, UserProfile
from src.core.use_cases.calculate_chart import CalculateChartUseCase
from src.core.use_cases.generate_horoscope import GenerateHoroscopeUseCase
from src.infrastructure.ai.gemini_adapter import GeminiAdapter
from src.infrastructure.astro_engine.swiss_ephemeris import SwissEphemerisEngine
from src.infrastructure.persistence.in_memory_repo import InMemoryRepository


router = APIRouter(prefix="/v1")

# Dependencies
def get_settings():
    return Settings()

def get_astro_engine(settings: Settings = Depends(get_settings)):
    return SwissEphemerisEngine(eph_path=settings.swiss_eph_path)

def get_calculate_use_case(astro_engine: SwissEphemerisEngine = Depends(get_astro_engine)):
    return CalculateChartUseCase(astro_engine)

def get_ai_adapter(settings: Settings = Depends(get_settings)):
    return GeminiAdapter(api_key=settings.google_api_key)

def get_generate_horoscope_use_case(
    calculate_use_case: CalculateChartUseCase = Depends(get_calculate_use_case),
    ai_adapter: GeminiAdapter = Depends(get_ai_adapter)
):
    return GenerateHoroscopeUseCase(calculate_use_case, ai_adapter)

def get_repository():
    return InMemoryRepository()

# Request models
from pydantic import BaseModel

class CalculateChartRequest(BaseModel):
    date: str
    time: str | None = None
    latitude: float
    longitude: float
    timezone: str

class HoroscopePersonalRequest(BaseModel):
    class Profile(BaseModel):
        name: str
        birth_date: str
        birth_time: str | None = None
        latitude: float
        longitude: float

    class Preferences(BaseModel):
        tone: str = "spiritual"
        focus: str = "general"
        language: str = "en"

    profile: Profile
    preferences: Preferences
    admin: bool = False

# Response models
class PlanetResponse(BaseModel):
    name: str
    sign: str
    longitude: float
    house: int
    is_retrograde: bool

class HouseResponse(BaseModel):
    number: int
    degree: float
    sign: str

class AspectResponse(BaseModel):
    planet1: str
    planet2: str
    type: str
    orb: float

class CalculateChartResponse(BaseModel):
    meta: dict
    planets: list[PlanetResponse]
    houses: list[HouseResponse]
    aspects: list[AspectResponse]

class ProcessingStepsResponse(BaseModel):
    coordinates: dict
    time_correction: dict
    chart_generation: dict
    relationship_mapping: dict
    pm_config: dict

class HoroscopePersonalResponse(BaseModel):
    chart: dict
    interpretation: dict
    ai_text: str
    processing_steps: ProcessingStepsResponse | None = None

@router.post("/chart/calculate", response_model=CalculateChartResponse)
async def calculate_chart(
    request: CalculateChartRequest,
    use_case: CalculateChartUseCase = Depends(get_calculate_use_case)
):
    """Calculate natal chart."""
    birth_data = BirthData(
        date=request.date,
        time=request.time,
        lat=request.latitude,
        lon=request.longitude,
        timezone=request.timezone
    )
    chart = use_case.execute(birth_data)

    # For now, meta is empty, as julian_day is not in NatalChart
    return CalculateChartResponse(
        meta={"julian_day": chart.julian_day},
        planets=[PlanetResponse(**p.model_dump()) for p in chart.planets],
        houses=[HouseResponse(**h.model_dump()) for h in chart.houses],
        aspects=[AspectResponse(**a.model_dump()) for a in chart.aspects]
    )

@router.post("/horoscope/personal", response_model=HoroscopePersonalResponse)
async def generate_personal_horoscope(
    request: HoroscopePersonalRequest,
    use_case: GenerateHoroscopeUseCase = Depends(get_generate_horoscope_use_case),
    repo: InMemoryRepository = Depends(get_repository)
):
    """Generate personalized horoscope."""
    import uuid

    req_id = str(uuid.uuid4())

    birth_data = BirthData(
        date=request.profile.birth_date,
        time=request.profile.birth_time,
        lat=request.profile.latitude,
        lon=request.profile.longitude,
        timezone="UTC"  # Assume UTC for now
    )

    horoscope_output = use_case.execute(birth_data)

    # Save profile and chart
    user_id = req_id  # Use req_id as user_id for now
    profile = UserProfile(
        user_id=user_id,
        birth=birth_data
    )
    repo.save_profile(profile)
    repo.save_chart(user_id, horoscope_output.chart)

    # Build processing steps for admin mode
    processing_steps = None
    if request.admin:
        processing_steps = ProcessingStepsResponse(
            coordinates={
                "latitude": request.profile.latitude,
                "longitude": request.profile.longitude,
                "timezone": "UTC"
            },
            time_correction={
                "local_time": request.profile.birth_time,
                "universal_time": "12:00:00",  # Mock conversion
                "offset": "0:00"
            },
            chart_generation={
                "planets": [
                    {"name": "Sun", "degree": 15.5, "sign": "Aries"},
                    {"name": "Moon", "degree": 22.1, "sign": "Libra"},
                    {"name": "Ascendant", "degree": 5.0, "sign": "Cancer"}
                ],
                "houses": [
                    {"number": 1, "degree": 5.0, "sign": "Cancer"},
                    {"number": 2, "degree": 35.0, "sign": "Leo"}
                ]
            },
            relationship_mapping={
                "aspects": [
                    {"planet1": "Sun", "planet2": "Moon", "type": "Opposition", "orb": 1.6}
                ]
            },
            pm_config={
                "house_system": "Placidus",
                "ephemeris_source": "SwissEphemeris",
                "interpretation_engine": "Hybrid",
                "ai_model": "Gemini",
                "temperature": 0.7
            }
        )

    return HoroscopePersonalResponse(
        chart=horoscope_output.chart.model_dump(),
        interpretation=horoscope_output.interpretation.model_dump(),
        ai_text=horoscope_output.ai_text,
        processing_steps=processing_steps
    )