from fastapi import APIRouter, HTTPException, status
from typing import List
from app.database import db_patterns, pattern_id_counter
from app.models.pattern import PatternCreate, PatternUpdate, PatternResponse

# Adjusted tag to match lowercase "patterns" defined in your app/main.py metadata
router = APIRouter(prefix="/patterns", tags=["patterns"])

@router.post(
    "", 
    response_model=PatternResponse, 
    status_code=status.HTTP_201_CREATED, 
    summary="Catalog a Pattern",
    description="Defensively verifies structural constraints and catalogs a new cross-stitch design pattern chart entry.",
    responses={
        status.HTTP_409_CONFLICT: {"description": "A pattern chart matching this title and designer is already registered."}
    }
)
def create_pattern(pattern_in: PatternCreate):
    global pattern_id_counter
    
    # Enforce database uniqueness constraints via an explicit 409 Conflict
    for p in db_patterns.values():
        if p["title"] == pattern_in.title and p["designer"] == pattern_in.designer:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A pattern chart matching this title and designer is already registered in your stash portfolio."
            )
            
    new_id = pattern_id_counter
    pattern_data = pattern_in.model_dump()
    pattern_data["id"] = new_id
    
    db_patterns[new_id] = pattern_data
    pattern_id_counter += 1
    return pattern_data

@router.get(
    "", 
    response_model=List[PatternResponse], 
    summary="List All Patterns",
    description="Fetches a structural array containing every cross-stitch chart inside your active portfolio catalog database."
)
def get_all_patterns():
    return list(db_patterns.values())
