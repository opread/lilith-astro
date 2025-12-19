# AstroPersona: Personalized Horoscope Functional Overview

This document provides a high-level, functional description of what AstroPersona does and how it processes your information, written for users familiar with astrology.

AstroPersona is a sophisticated tool that combines precise astronomical mathematics (the "Astro Engine") with advanced artificial intelligence (AI) to produce deeply personalized, narrative horoscopes.

---

## 1. Core Functionality: The Calculation Process

The foundation of any personalized horoscope is an accurate natal chart. AstroPersona provides complete transparency into this process, displaying each calculation step.

### Detailed Processing Steps:
When you provide your birth date, exact time, and location, the system performs the following actions, visible in the "Processing Steps" dashboard:

1.  **Coordinates Extraction**: Converts your city/location into precise Latitude and Longitude coordinates.
2.  **Time Correction**: Converts your local birth time into Universal Time (UT) based on the specific timezone offset of your birth location.
3.  **Chart Generation**:
    *   Calculates the exact degrees of all major planets (Sun, Moon, Mercury, etc.).
    *   Calculates the precise positions of the 12 Astrological Houses (Ascendant, Midheaven, etc.) based on your chosen House System.
4.  **Relationship Mapping**: Identifies the key relationships between these bodies (Aspects), such as Trines, Squares, and Oppositions, along with their associated orbs.

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

## 4. Advanced Customization & Configuration

AstroPersona offers granular control over both the astronomical calculations and the AI generation process. This "Product Manager" level configuration allows for diverse astrological experiments.

### Astronomical Parameters
| Parameter | Description | Options |
| :--- | :--- | :--- |
| **House System** | Determines how the 12 houses are calculated. | `Placidus` (Default), `Koch`, `Regiomontanus` |
| **Ephemeris Source** | The source of astronomical data. | `Swiss Ephemeris` (Standard), `NASA JPL` (Experimental) |

### AI & Narrative Parameters
| Parameter | Description | Options |
| :--- | :--- | :--- |
| **Interpretation Engine** | Controls how much freedom the AI has. | `RuleBased` (Strict), `Hybrid` (Balanced), `PureAI` (Creative) |
| **Narrative Style** | Sets the tone of the output. | `Professional` (Neutral), `Poetic` (Evocative), `Debug` (Technical) |
| **AI Model** | The underlying Large Language Model used. | `Gemini`, `GPT-4`, `Custom` |
| **Temperature** | Controls the "creativity" or randomness of the AI (0.0 - 1.0). | Lower (e.g., 0.2) is more deterministic; Higher (e.g., 0.8) is more creative. |

By combining unparalleled astronomical precision, structured astrological rules, and state-of-the-art AI narrative generation, AstroPersona provides a premium and profound personal insight.