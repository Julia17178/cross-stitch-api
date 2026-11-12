import os
from fastapi import FastAPI, HTTPException
from app.routers import patterns

app = FastAPI(
    title="Cross-Stitch Catalog API",
    description="An API designed for craft hobbyists to digitally organize and validate cross-stitch patterns.",
    version="1.0.0"
)

ENABLE_FABRIC_CALCULATOR = os.getenv("ENABLE_FABRIC_CALCULATOR", "false").lower() == "true"
ENABLE_STITCH_TIMER = os.getenv("ENABLE_STITCH_TIMER", "false").lower() == "true"

app.include_router(patterns.router)

@app.get("/health", tags=["health"], summary="Health Check")
def health_check():
    return {
        "status": "healthy", 
        "message": "Confirm that the API process is running.", 
        "fabric_calculator_enabled": ENABLE_FABRIC_CALCULATOR,
        "stitch_timer_enabled": ENABLE_STITCH_TIMER
    }

@app.get("/patterns/fabric-calculator", tags=["calculator"], summary="Calculate Required Fabric Size")
def get_fabric_calculation():
    if not ENABLE_FABRIC_CALCULATOR:
        raise HTTPException(status_code=404, detail="Feature flag 'ENABLE_FABRIC_CALCULATOR' is disabled.")
    
    return {"message": "Fabric canvas calculator functionality coming soon!"}

@app.get("/patterns/stitch-timer", tags=["timer"], summary="Estimate Project Completion Time")
def get_stitch_timer():
    if not ENABLE_STITCH_TIMER:
        raise HTTPException(status_code=404, detail="Feature flag 'ENABLE_STITCH_TIMER' is disabled.")

    return {"message": "Stitch completion timer functionality coming soon!"}
