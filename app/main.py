from fastapi import FastAPI
# 1. Import your new patterns router module here
from app.routers import patterns 

# Define metadata tags for your cross-stitch resource layers
tags_metadata = [
    {
        "name": "Root",
        "description": "API status verification endpoints and health checks.",
    },
    {
        "name": "patterns",
        "description": "Cross-stitch pattern definitions, grid sizes, and required canvas fabric configurations.",
    },
    {
        "name": "floss",
        "description": "Embroidery thread parameters, color inventory levels, and relational pattern trackers.",
    },
]

app = FastAPI(
    title="Cross-Stitch Stash & Pattern Tracker API",
    description=(
        "### Unified Portfolio Architecture\n"
        "This centralized API serving engine functions as a dual-course portfolio component:\n"
        "*   **SDEV 3310 (API Design & Development):** Demonstrates strict contract compliance, "
        "defensive schema configurations, and precise HTTP response mappings.\n"
        "*   **SDEV 3320 (Full-Stack Deployment):** Serves as the high-performance asynchronous data engine "
        "powering dynamic user interface rendering and inventory state mutations."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata
)

# 2. Include the patterns router so it displays in your documentation
app.include_router(patterns.router)

@app.get("/", tags=["Root"], summary="API Core Ingress Check")
def read_root():
    return {"status": "online", "message": "Welcome to the Cross-Stitch Tracker API Engine."}
