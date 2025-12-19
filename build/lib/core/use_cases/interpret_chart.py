"""Use case for interpreting a natal chart."""

from typing import Set

from src.core.domain.models import Aspect, Interpretation, NatalChart
from src.core.domain.rules import ASPECT_RULES, HOUSE_RULES, SIGN_RULES


def interpret_chart(chart: NatalChart) -> Interpretation:
    """Interpret a natal chart by applying astrological rules.

    Args:
        chart: The natal chart to interpret.

    Returns:
        An Interpretation object with traits, strengths, and challenges.
    """
    traits: Set[str] = set()
    strengths: Set[str] = set()
    challenges: Set[str] = set()

    # Apply rules for planets (sign and house)
    for planet in chart.planets:
        sign = planet.sign
        house = planet.house

        if sign in SIGN_RULES:
            traits.update(SIGN_RULES[sign]["traits"])
            strengths.update(SIGN_RULES[sign]["strengths"])
            challenges.update(SIGN_RULES[sign]["challenges"])

        if house in HOUSE_RULES:
            traits.update(HOUSE_RULES[house]["traits"])
            strengths.update(HOUSE_RULES[house]["strengths"])
            challenges.update(HOUSE_RULES[house]["challenges"])

    # Apply rules for aspects
    for aspect in chart.aspects:
        aspect_type = aspect.type.lower()
        if aspect_type in ASPECT_RULES:
            traits.update(ASPECT_RULES[aspect_type]["traits"])
            strengths.update(ASPECT_RULES[aspect_type]["strengths"])
            challenges.update(ASPECT_RULES[aspect_type]["challenges"])

    return Interpretation(
        traits=list(traits),
        strengths=list(strengths),
        challenges=list(challenges)
    )