# Product Requirements Document (PRD)

## 1. Overview

**Product Name:** AstroPersona (working title)

**Vision:** O aplicație premium de horoscop personalizat, bazată pe calcule astronomice precise (Swiss Ephemeris) + interpretare avansată (rule-based + AI), livrată prin API modern și extensibil.

**Target users:**
- Utilizatori finali (B2C)
- Creatori de conținut astrologic
- Platforme wellness / lifestyle (B2B API)

---

## 2. Goals & Non‑Goals

### Goals
- Calcul precis al hărții natale
- Interpretare coerentă, premium
- Text generat AI personalizat
- Modularitate totală (fiecare modul poate fi înlocuit)
- Testabilitate ridicată

### Non‑Goals
- Predictii medicale / financiare deterministe
- Social network features (v1)

---

## 3. Functional Scope

### 3.1 Input User

| Field | Type | Required |
|-----|------|----------|
| date_of_birth | date | yes |
| time_of_birth | time | optional |
| location | string | yes |
| latitude | float | derived |
| longitude | float | derived |
| timezone | string | derived |

---

## 4. System Architecture

```
[Client]
   |
[FastAPI]
   |
+------------------------------+
| Astro Engine (Swiss Ephemeris)|
+------------------------------+
   |
[Interpretation Engine]
   |
[AI Text Generator]
   |
[Persistence / Cache]
```

---

## 5. Module Breakdown (Independent & Robust)

### 5.1 Astro Engine (Pure Math)

**Responsibility:** strict calcule astronomice

**Dependencies:** pyswisseph, astropy

**Outputs:** structuri JSON pure

```json
{
  "sun": {"sign": "Leo", "degree": 15.2},
  "moon": {"sign": "Scorpio", "degree": 2.1},
  "ascendant": "Gemini",
  "houses": {...}
}
```

---

### 5.2 Interpretation Engine (Rule‑based)

**Responsibility:** transformă datele în trăsături

**Rule Example:**
- Sun in Fire + Moon in Water → tension score

**Output:** profile semantic

```json
{
  "traits": ["leadership", "emotional depth"],
  "strengths": [...],
  "challenges": [...]
}
```

---

### 5.3 AI Text Engine (Premium Layer)

**Responsibility:** generare text fluent

**Model:** LLM external (OpenAI / local LLM)

**Style Modes:**
- Spiritual
- Psychological
- Premium professional

---

## 6. Data Model (Exact Schema)

### 6.1 UserProfile

```json
{
  "user_id": "uuid",
  "birth": {
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "lat": 44.43,
    "lon": 26.10,
    "timezone": "Europe/Bucharest"
  }
}
```

### 6.2 NatalChart

```json
{
  "planets": {
    "Sun": {"sign": "Leo", "deg": 15.2},
    "Moon": {"sign": "Scorpio", "deg": 2.1}
  },
  "houses": {...},
  "aspects": [...]
}
```

### 6.3 HoroscopeOutput

```json
{
  "summary": "text",
  "detailed": "text",
  "scores": {"career": 0.8, "relationships": 0.6}
}
```

---

## 7. API Specification (FastAPI)

### Endpoint

```
POST /api/v1/horoscope/personal
```

### Response

```json
{
  "chart": {...},
  "interpretation": {...},
  "ai_text": "..."
}
```

---

## 8. Minimal Functional Code (Swiss Ephemeris + FastAPI)

```python
import swisseph as swe
from fastapi import FastAPI

app = FastAPI()

@app.post("/horoscope")
def horoscope(data: dict):
    jd = swe.julday(1990, 5, 17, 12.0)
    sun_pos = swe.calc_ut(jd, swe.SUN)
    return {"sun_longitude": sun_pos[0][0]}
```

---

## 9. AI Prompt Templates (Commercial‑ready)

### Natal Reading

```
You are a professional astrologer.
Based on the natal chart below, write a premium, psychologically nuanced horoscope.
Avoid vague statements. Be specific and empowering.

Chart:
{{chart_json}}
```

### Daily Horoscope

```
Create a concise daily horoscope aligned with the user's natal Sun and Moon.
Tone: warm, confident, premium.
```

---

## 10. Testing Strategy (Included)

### Unit Tests
- Planet position accuracy
- Rule evaluation

### Integration Tests
- Full API call
- AI generation mocked

### Validation Tests
- Timezone edge cases
- Missing birth time fallback

```python
def test_sun_position():
    assert 0 <= sun_deg <= 360
```

---

## 11. Differentiation vs Existing Apps

| Feature | AstroPersona | Others |
|------|--------------|--------|
| Swiss Ephemeris | ✅ | ❌ |
| Explainable logic | ✅ | ❌ |
| Style‑adaptive AI | ✅ | ❌ |
| API‑first | ✅ | ❌ |
| Premium tone control | ✅ | ❌ |

---

## 12. Monetization (Premium)

- Monthly subscription
- Paid natal chart
- API usage tiers

---

## 13. Roadmap

**Phase 1:** Core astro + rules
**Phase 2:** AI text
**Phase 3:** Mobile + B2B API

---

## 14. Success Metrics

- Retention D30
- Text quality score
- API latency < 300ms

---

✅ Document ready for implementation & stakeholder review

