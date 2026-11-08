import os
from fastapi import FastAPI
from app.routers import patterns

app = FastAPI(
    title="Cross-Stitch Catalog API",
    description="An API designed for craft hobbyists to digitally organize and validate cross-stitch patterns.",
    version="1.0.0"
)

# 🚩 FEATURE FLAG DEFINITION: Defaults to False (Disabled)
ENABLE_FABRIC_CALCULATOR = os.getenv("ENABLE_FABRIC_CALCULATOR", "false").lower() == "true"

# Connect your patterns router layer
app.include_router(patterns.router)

@app.get("/health", tags=["health"], summary="Health Check")
def health_check():
    return {
        "status": "healthy", 
        "message": "Confirm that the API process is running.", 
        "fabric_calculator_enabled": ENABLE_FABRIC_CALCULATOR
    }
