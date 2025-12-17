"""Prompt templates for AI text generation."""

NATAL_HOROSCOPE_PROMPT = """
You are a professional astrologer.
Based on the natal chart below, write a premium, psychologically nuanced horoscope.
Avoid vague statements. Be specific and empowering.

Chart:
{chart_json}
"""

DAILY_HOROSCOPE_PROMPT = """
Create a concise daily horoscope aligned with the user's natal Sun and Moon.
Tone: warm, confident, premium.
"""