"""Astrological rules for interpretation."""

from typing import Dict, List

# Rules for signs
SIGN_RULES: Dict[str, Dict[str, List[str]]] = {
    "Aries": {
        "traits": ["bold", "energetic", "independent"],
        "strengths": ["leadership", "courage"],
        "challenges": ["impulsiveness", "short-tempered"]
    },
    "Taurus": {
        "traits": ["practical", "reliable", "patient"],
        "strengths": ["stability", "determination"],
        "challenges": ["stubbornness", "materialistic"]
    },
    "Gemini": {
        "traits": ["adaptable", "communicative", "versatile"],
        "strengths": ["intellect", "social skills"],
        "challenges": ["indecisiveness", "superficiality"]
    },
    "Cancer": {
        "traits": ["emotional", "intuitive", "nurturing"],
        "strengths": ["empathy", "protectiveness"],
        "challenges": ["moodiness", "over-sensitivity"]
    },
    "Leo": {
        "traits": ["confident", "generous", "dramatic"],
        "strengths": ["charisma", "creativity"],
        "challenges": ["arrogance", "need for attention"]
    },
    "Virgo": {
        "traits": ["analytical", "practical", "helpful"],
        "strengths": ["attention to detail", "reliability"],
        "challenges": ["criticism", "perfectionism"]
    },
    "Libra": {
        "traits": ["diplomatic", "fair-minded", "social"],
        "strengths": ["harmony", "balance"],
        "challenges": ["indecision", "people-pleasing"]
    },
    "Scorpio": {
        "traits": ["intense", "passionate", "mysterious"],
        "strengths": ["resilience", "intuition"],
        "challenges": ["jealousy", "control issues"]
    },
    "Sagittarius": {
        "traits": ["optimistic", "adventurous", "philosophical"],
        "strengths": ["freedom", "wisdom"],
        "challenges": ["recklessness", "over-confidence"]
    },
    "Capricorn": {
        "traits": ["ambitious", "disciplined", "responsible"],
        "strengths": ["leadership", "perseverance"],
        "challenges": ["rigidity", "workaholism"]
    },
    "Aquarius": {
        "traits": ["innovative", "independent", "humanitarian"],
        "strengths": ["originality", "progressiveness"],
        "challenges": ["detachment", "eccentricity"]
    },
    "Pisces": {
        "traits": ["compassionate", "artistic", "intuitive"],
        "strengths": ["empathy", "spirituality"],
        "challenges": ["escapism", "victim mentality"]
    }
}

# Rules for houses (simplified)
HOUSE_RULES: Dict[int, Dict[str, List[str]]] = {
    1: {
        "traits": ["self-identity", "appearance"],
        "strengths": ["initiative"],
        "challenges": ["self-centeredness"]
    },
    2: {
        "traits": ["values", "possessions"],
        "strengths": ["resourcefulness"],
        "challenges": ["greed"]
    },
    3: {
        "traits": ["communication", "learning"],
        "strengths": ["adaptability"],
        "challenges": ["gossip"]
    },
    4: {
        "traits": ["home", "family"],
        "strengths": ["security"],
        "challenges": ["emotional dependency"]
    },
    5: {
        "traits": ["creativity", "pleasure"],
        "strengths": ["joy"],
        "challenges": ["self-indulgence"]
    },
    6: {
        "traits": ["health", "service"],
        "strengths": ["duty"],
        "challenges": ["criticism"]
    },
    7: {
        "traits": ["partnerships", "relationships"],
        "strengths": ["cooperation"],
        "challenges": ["codependency"]
    },
    8: {
        "traits": ["transformation", "intimacy"],
        "strengths": ["resilience"],
        "challenges": ["obsession"]
    },
    9: {
        "traits": ["philosophy", "travel"],
        "strengths": ["optimism"],
        "challenges": ["dogmatism"]
    },
    10: {
        "traits": ["career", "reputation"],
        "strengths": ["ambition"],
        "challenges": ["status-seeking"]
    },
    11: {
        "traits": ["friends", "community"],
        "strengths": ["altruism"],
        "challenges": ["detachment"]
    },
    12: {
        "traits": ["spirituality", "subconscious"],
        "strengths": ["compassion"],
        "challenges": ["isolation"]
    }
}

# Rules for aspects (simplified, only conjunct for now)
ASPECT_RULES: Dict[str, Dict[str, List[str]]] = {
    "conjunct": {
        "traits": ["intensified"],
        "strengths": ["focus"],
        "challenges": ["overload"]
    },
    "trine": {
        "traits": ["harmonious"],
        "strengths": ["ease"],
        "challenges": ["complacency"]
    },
    "square": {
        "traits": ["challenging"],
        "strengths": ["growth"],
        "challenges": ["conflict"]
    },
    "opposition": {
        "traits": ["balancing"],
        "strengths": ["awareness"],
        "challenges": ["tension"]
    }
}