"""Swiss Ephemeris wrapper for calculating natal charts."""

import math
from datetime import datetime
from typing import List

try:
    import swisseph as swe
except ImportError:
    raise ImportError(
        "The 'pyswisseph' package is not installed. This is a critical dependency for astrological calculations. "
        "Please try to install it manually. If you are running tests, ensure this module is mocked."
    )

from src.core.domain.models import Aspect, BirthData, House, NatalChart, Planet


class SwissEphemerisEngine:
    """Astro engine using Swiss Ephemeris for calculations."""

    SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    PLANETS = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("Mercury", swe.MERCURY),
        ("Venus", swe.VENUS),
        ("Mars", swe.MARS),
        ("Jupiter", swe.JUPITER),
        ("Saturn", swe.SATURN),
        ("Uranus", swe.URANUS),
        ("Neptune", swe.NEPTUNE),
        ("Pluto", swe.PLUTO),
    ]

    ASPECT_TYPES = {
        0: "Conjunction",
        60: "Sextile",
        90: "Square",
        120: "Trine",
        180: "Opposition",
    }

    MAX_ORB = 10.0  # degrees

    def __init__(self, eph_path: str = "/usr/local/share/sweph"):
        """Initialize the engine.

        Args:
            eph_path: Path to the ephemeris files.
        """
        swe.set_ephe_path(eph_path)

    def calculate_chart(self, birth_data: BirthData) -> NatalChart:
        """Calculate the complete natal chart for given birth data.

        Args:
            birth_data: The birth data including date, time, location.

        Returns:
            NatalChart: The calculated natal chart.
        """
        jd = self._calculate_julian_day(birth_data)
        houses_data = swe.houses(jd, birth_data.lat, birth_data.lon, b'P')
        houses = self._calculate_houses(houses_data)
        planets = self._calculate_planets(jd, houses_data, birth_data.lat)
        aspects = self._calculate_aspects(planets)
        return NatalChart(julian_day=jd, planets=planets, houses=houses, aspects=aspects)

    def _calculate_julian_day(self, birth_data: BirthData) -> float:
        """Calculate Julian Day for the birth data.

        Assumes time is in UTC for simplicity. In production, handle timezone conversion.

        Args:
            birth_data: Birth data.

        Returns:
            float: Julian Day.
        """
        date_str = birth_data.date
        time_str = birth_data.time or "12:00"  # Default to noon if no time
        dt_str = f"{date_str} {time_str}"
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        year, month, day = dt.year, dt.month, dt.day
        hour = dt.hour + dt.minute / 60.0
        return swe.julday(year, month, day, hour)

    def _calculate_planets(self, jd: float, houses_data, lat: float) -> List[Planet]:
        """Calculate planetary positions.

        Args:
            jd: Julian Day.
            houses_data: Houses data from swe.houses.
            lat: Latitude.

        Returns:
            List[Planet]: List of planets with positions.
        """
        planets = []
        armc = houses_data[3]
        eps = houses_data[4]
        for name, planet_id in self.PLANETS:
            pos = swe.calc_ut(jd, planet_id)
            longitude = pos[0][0]
            speed = pos[0][3]  # daily speed
            is_retrograde = speed < 0
            sign = self._get_sign(longitude)
            house = int(swe.house_pos(armc, lat, eps, b'P', longitude, lat))
            planets.append(Planet(
                name=name,
                sign=sign,
                longitude=longitude,
                house=house,
                is_retrograde=is_retrograde
            ))
        return planets

    def _calculate_houses(self, houses_data) -> List[House]:
        """Calculate house cusps using Placidus system.

        Args:
            houses_data: Houses data from swe.houses.

        Returns:
            List[House]: List of houses.
        """
        cusps = houses_data[0]  # cusps[1] to cusps[12]
        houses = []
        for i in range(1, 13):
            degree = cusps[i]
            sign = self._get_sign(degree)
            houses.append(House(number=i, degree=degree, sign=sign))
        return houses

    def _calculate_aspects(self, planets: List[Planet]) -> List[Aspect]:
        """Calculate aspects between planets.

        Args:
            planets: List of planets.

        Returns:
            List[Aspect]: List of aspects.
        """
        aspects = []
        planet_dict = {p.name: p for p in planets}
        for i, p1 in enumerate(planets):
            for p2 in planets[i+1:]:
                diff = abs(p1.longitude - p2.longitude)
                diff = min(diff, 360 - diff)
                for angle, aspect_type in self.ASPECT_TYPES.items():
                    if abs(diff - angle) <= self.MAX_ORB:
                        orb = abs(diff - angle)
                        aspects.append(Aspect(
                            planet1=p1.name,
                            planet2=p2.name,
                            type=aspect_type,
                            orb=orb
                        ))
                        break  # Take the closest aspect
        return aspects

    def _get_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude.

        Args:
            longitude: Longitude in degrees.

        Returns:
            str: Zodiac sign.
        """
        index = int(longitude // 30) % 12
        return self.SIGNS[index]
