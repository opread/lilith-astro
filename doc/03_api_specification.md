# 03. API Specification - AstroPersona V1.1

## 1. General Info
*   **Base URL**: `/api/v1`
*   **Protocol**: HTTP/1.1 (or HTTP/2)
*   **Content-Type**: `application/json`
*   **Date Format**: ISO 8601 (`YYYY-MM-DD`, `HH:MM`)

## 2. Authentication
*   **Type**: Bearer Token (JWT)
*   **Header**: `Authorization: Bearer <token>`
*(Note: Initial implementation may focus on public endpoints or simple API Key for B2B)*

## 3. Endpoints

### 3.1 Calculate Natal Chart
**POST** `/chart/calculate`

Generates the raw astronomical data without AI interpretation. Useful for debugging or low-latency needs.

**Request Body:**
```json
{
  "date": "1990-05-17",
  "time": "12:30",
  "latitude": 44.4268,
  "longitude": 26.1025,
  "timezone": "Europe/Bucharest"
}
```

**Response (200 OK):**
```json
{
  "meta": {
    "julian_day": 2448029.020833
  },
  "planets": [
    {
      "name": "Sun",
      "sign": "Taurus",
      "longitude": 56.45,
      "house": 9,
      "is_retrograde": false
    },
    {
      "name": "Moon",
      "sign": "Aquarius",
      "longitude": 312.10,
      "house": 4,
      "is_retrograde": false
    }
    // ... other planets
  ],
  "houses": [
    {"number": 1, "degree": 12.5, "sign": "Leo"},
    // ... 12 houses
  ],
  "aspects": [
    {"planet1": "Sun", "planet2": "Moon", "type": "Square", "orb": 2.5}
  ]
}
```

---

### 3.2 Generate Personalized Horoscope
**POST** `/horoscope/personal`

The flagship endpoint. Calculates the chart, applies rules, and generates AI text.

**Request Body:**
```json
{
  "profile": {
    "name": "Alex",
    "birth_date": "1990-05-17",
    "birth_time": "12:30",
    "latitude": 44.4268,
    "longitude": 26.1025
  },
  "preferences": {
    "tone": "spiritual", 
    "focus": "career",
    "language": "en" 
  }
}
```

*   `tone`: `spiritual` | `psychological` | `practical`
*   `focus`: `general` | `love` | `career`

**Response (200 OK):**
```json
{
  "id": "req_123456789",
  "status": "completed",
  "chart_summary": {
    "sun_sign": "Taurus",
    "moon_sign": "Aquarius",
    "ascendant": "Leo"
  },
  "interpretation": {
    "summary": "A grounded visionary...",
    "sections": [
      {
        "title": "Core Identity",
        "content": "With your Sun in Taurus..."
      },
      {
        "title": "Emotional World",
        "content": "Your Aquarius Moon suggests..."
      }
    ]
  },
  "ai_metadata": {
    "model": "gpt-4",
    "tokens_used": 450
  }
}
```

## 4. Error Handling

Standardized error responses.

**Schema:**
```json
{
  "error": {
    "code": "INVALID_COORDINATES",
    "message": "Latitude must be between -90 and 90.",
    "details": "Value provided: 95.0"
  }
}
```

**Common Codes:**
*   `400 Bad Request`: Validation failure (e.g., invalid date format).
*   `422 Unprocessable Entity`: Logical error (e.g., timezone mismatch).
*   `500 Internal Server Error`: Infrastructure failure (e.g., AI provider down).