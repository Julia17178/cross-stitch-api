# Cross-Stitch Catalog API

An API designed for craft hobbyists and pattern designers to digitally organize, create, and validate their cross-stitch charts, tracking systems, and fabric constraints.

## Architecture Layers
Following a clean, layered development pattern, this system isolates core application layers:
* **Schemas:** Pydantic validation files that defensively enforce structural limits (such as a 20-color maximum constraint).
* **Routers:** FastAPI endpoint definitions that route request payloads and declare HTTP response statuses.
* **Database:** Centralized data access layer managing in-memory tracking dictionaries and identity sequences.

## Setup Instructions
1. Ensure your Python virtual environment is active.
2. Install dependencies: `pip install fastapi uvicorn`
3. Spin up the application server: `uvicorn app.main:app --reload`

## Core Execution Flow Examples

### 1. Catalog a Pattern (POST /patterns)
```json
{
  "title": "Starry Night",
  "designer": "Crafty Designs",
  "fabric_count": 14,
  "grid_width": 140,
  "grid_height": 140,
  "colors": ["DMC 310", "DMC 820", "DMC 725"]
}
```
**Expected Server Status Response:** `201 Created`

### 2. List All Patterns (GET /patterns)
**Endpoint:** `GET /patterns`  
**Expected Server Status Response:** `200 OK`
