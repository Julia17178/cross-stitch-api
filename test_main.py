import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db_patterns

# Initialize the programmatic FastAPI testing client execution engine
client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_mock_database():
    """Clears the mock database dictionary before every test run execution loop."""
    db_patterns.clear()

def test_create_valid_pattern_success():
    """
    Test 1 (EP - Valid Partition): Checks that a standard pattern with perfectly 
    valid title, designer, and structural integers successfully saves.
    """
    payload = {
        "title": "Starry Night",
        "designer": "Dimensions",
        "fabric_count": 14,
        "grid_width": 200,
        "grid_height": 250
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 201
    assert response.json()["id"] == 1

def test_create_pattern_minimum_boundary_title():
    """
    Test 2 (BVA - Minimum Boundary): Verifies that a pattern with a single-character 
    title (the absolute minimum allowable min_length=1 constraint) passes successfully.
    """
    payload = {
        "title": "A",  # Boundary condition: exact lower limit string
        "designer": "DMC",
        "fabric_count": 16,
        "grid_width": 50,
        "grid_height": 50
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 201

def test_create_pattern_invalid_empty_title():
    """
    Test 3 (BVA - Out-of-Bounds Boundary): Verifies that passing an empty string 
    for the title fails validation because it drops below the min_length=1 boundary rule.
    """
    payload = {
        "title": "",  # Invalid boundary violation condition
        "designer": "Classic Stitches",
        "fabric_count": 14,
        "grid_width": 100,
        "grid_height": 100
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 422  # Unprocessable Entity error

def test_create_duplicate_pattern_conflict():
    """
    Test 4 (EP - Invalid Partition): Checks that trying to catalog an identical 
    pattern title and designer pairing returns a clean 409 Conflict error header.
    """
    payload = {
        "title": "Autumn Foliage",
        "designer": "Mirabilia",
        "fabric_count": 32,
        "grid_width": 180,
        "grid_height": 220
    }
    # Initial cataloging creation execution loop succeeds
    response1 = client.post("/patterns", json=payload)
    assert response1.status_code == 201
    
    # Secondary invocation triggers database level uniqueness constraint mismatch
    response2 = client.post("/patterns", json=payload)
    assert response2.status_code == 409
    assert "already registered" in response2.json()["detail"]
