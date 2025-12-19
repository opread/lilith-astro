"""Domain models for AstroPersona application."""

from typing import List, Optional

from pydantic import BaseModel


class BirthData(BaseModel):
    """Represents birth data for a user."""

    date: str  # YYYY-MM-DD
    time: Optional[str] = None  # HH:MM, optional
    lat: float
    lon: float
    timezone: str


class UserProfile(BaseModel):
    """Represents a user profile with birth information."""

    user_id: str
    birth: BirthData


class Planet(BaseModel):
    """Represents a planet in the natal chart."""

    name: str
    sign: str
    longitude: float
    house: int
    is_retrograde: bool


class House(BaseModel):
    """Represents a house in the natal chart."""

    number: int
    degree: float
    sign: str


class Aspect(BaseModel):
    """Represents an aspect between two planets."""

    planet1: str
    planet2: str
    type: str
    orb: float


class NatalChart(BaseModel):
    """Represents the complete natal chart."""

    julian_day: Optional[float] = None
    planets: List[Planet]
    houses: List[House]
    aspects: List[Aspect]


class Interpretation(BaseModel):
    """Represents the interpretation of a natal chart."""

    traits: List[str]
    strengths: List[str]
    challenges: List[str]


class HoroscopeOutput(BaseModel):
    """Represents the complete horoscope output including AI text."""

    chart: NatalChart
    interpretation: Interpretation
    ai_text: str