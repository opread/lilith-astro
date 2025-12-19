# AstroPersona: Personalized Horoscope Functional Overview

This document provides a high-level, functional description of what AstroPersona does and how it processes your information, written for users familiar with astrology.

AstroPersona is a sophisticated tool that combines precise astronomical mathematics (the "Astro Engine") with advanced artificial intelligence (AI) to produce deeply personalized, narrative horoscopes.

---

## 1. Core Functionality: The Calculation

The foundation of any personalized horoscope is an accurate natal chart. AstroPersona uses the **Swiss Ephemeris** library—the gold standard in astronomical calculation—to ensure precision.

### What We Do:
When you provide your birth date, exact time, and location (latitude/longitude), the system performs the following actions:
1.  **Time Correction**: Converts your local birth time, using your specified time zone (e.g., Europe/Bucharest), into Universal Time (UT).
2.  **Chart Generation**: Calculates the exact degrees of all major planets (Sun, Moon, Mercury, etc.) and the precise positions of the 12 Astrological Houses (Ascendant, Midheaven, etc.).
3.  **Relationship Mapping**: Identifies the key relationships between these bodies (Aspects), such as Trines, Squares, and Oppositions, along with their associated orbs.

The result is a complete, scientifically accurate Natal Chart, ready for interpretation.

## 2. The Interpretation Engine: Translating Math to Meaning

Before engaging the AI, AstroPersona applies a rule-based engine to translate the raw astronomical data into structured astrological concepts. This ensures the AI has a solid, consistent foundation based on traditional astrological knowledge.

### How it Works:
*   The system examines every placement (e.g., *Sun in Taurus*, *Moon in Aquarius*, *Mercury in the 3rd House*).
*   It also examines every major relationship (*Sun Square Moon*, *Venus Trine Mars*).
*   For each placement and aspect, the system extracts a set of key **Traits, Strengths, and Challenges** from its internal database (rules).

This internal data structure acts as the blueprint for your reading, identifying the core themes present in your chart.

## 3. The AI Layer: Crafting the Narrative

The structured interpretation data is then fed to the **Google Gemini AI model**. The AI's role is not to perform calculations or define rules, but to act as a skilled astrological writer.

### AI's Role:
1.  **Contextual Generation**: Takes the calculated chart data and the structured themes (Traits, Strengths, Challenges) and weaves them into a fluid, cohesive, and deeply personalized narrative.
2.  **Natural Language**: Ensures the reading feels like it was written by a human astrologer, going beyond simple definitions to describe the interplay between various energies.
3.  **Customization**: Adjusts the language, tone, and focus of the reading based on your provided preferences.

## 4. Customizing Your Reading

When requesting your personalized horoscope, you can tailor the output to focus on specific areas of your life:

| Preference | Description | Options |
| :--- | :--- | :--- |
| **Tone** | Sets the emotional and intellectual style of the writing. | `spiritual`, `psychological`, `practical` |
| **Focus** | Directs the narrative to analyze specific areas of your life in depth. | `general`, `love`, `career` |

By combining unparalleled astronomical precision, structured astrological rules, and state-of-the-art AI narrative generation, AstroPersona provides a premium and profound personal insight.