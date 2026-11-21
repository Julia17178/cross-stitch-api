import os
import logging
from fastapi import FastAPI, HTTPException
from app.routers import patterns

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cross_stitch_api")

app = FastAPI(
    title="Cross-Stitch Catalog API",
    description="An API designed for craft hobbyists to digitally organize and validate cross-stitch patterns.",
    version="1.0.0"
)

ENABLE_FABRIC_CALCULATOR = os.getenv("ENABLE_FABRIC_CALCULATOR", "false").lower() == "true"
ENABLE_STITCH_TIMER = os.getenv("ENABLE_STITCH_TIMER", "false").lower() == "true"

# 1. REAL METRIC: Counter tracking how many times the health endpoint is checked
HEALTH_CHECK_COUNT = 0

app.include_router(patterns.router)

@app.get("/health", tags=["health"], summary="Health Check")
def health_check():
    global HEALTH_CHECK_COUNT
    HEALTH_CHECK_COUNT += 1
    
    # 2. REAL LOG STATEMENT: Records each check and the current feature flag states
    logger.info(f"Health check #{HEALTH_CHECK_COUNT} | fabric_calc={ENABLE_FABRIC_CALCULATOR}, stitch_timer={ENABLE_STITCH_TIMER}")
    
    return {
        "status": "healthy", 
        "message": "Confirm that the API process is running.", 
        "fabric_calculator_enabled": ENABLE_FABRIC_CALCULATOR,
        "stitch_timer_enabled": ENABLE_STITCH_TIMER,
        "health_check_count": HEALTH_CHECK_COUNT
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
