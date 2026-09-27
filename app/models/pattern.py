from pydantic import BaseModel, Field, ConfigDict

class PatternBase(BaseModel):
    # Defensive Guardrail: instantly rejects unexpected payload fields from the frontend
    model_config = ConfigDict(extra="forbid")
    
    title: str = Field(..., min_length=1, description="The name of the cross-stitch pattern design.", examples=["Starry Night"])
    designer: str = Field(..., min_length=1, description="The artist or brand who published the chart.", examples=["Dimensions"])
    fabric_count: int = Field(..., description="Recommended Aida or Linen canvas weave thread count.", examples=[14])
    grid_width: int = Field(..., description="Total stitch width count across the horizontal grid.", examples=[150])
    grid_height: int = Field(..., description="Total stitch height count down the vertical grid.", examples=[200])

class PatternCreate(PatternBase):
    pass

class PatternUpdate(PatternBase):
    pass

class PatternResponse(PatternBase):
    id: int = Field(..., description="Application-assigned internal pattern identifier key.")
