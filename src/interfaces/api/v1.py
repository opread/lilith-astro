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

class HoroscopePersonalResponse(BaseModel):
    chart: dict
    interpretation: dict
    ai_text: str

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
        planets=[PlanetResponse(**p.dict()) for p in chart.planets],
        houses=[HouseResponse(**h.dict()) for h in chart.houses],
        aspects=[AspectResponse(**a.dict()) for a in chart.aspects]
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

    return HoroscopePersonalResponse(
        chart=horoscope_output.chart.dict(),
        interpretation=horoscope_output.interpretation.dict(),
        ai_text=horoscope_output.ai_text
    )