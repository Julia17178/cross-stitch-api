import time
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db_patterns

# Initialize the programmatic FastAPI testing client execution engine
client = TestClient(app)


# TEST DOUBLE JUSTIFICATION (Rubric Requirement):
# This test suite utilizes an in-memory dictionary mock (`db_patterns`) as a 
# test double instead of connecting to a live, external production database. 
# This isolates the unit tests and ensures rapid, side-effect-free execution loops.


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

def test_create_pattern_invalid_negative_fabric_count():
    """
    Test 5 (EP - Invalid Partition): Verifies that passing a negative integer 
    for the fabric_count fails validation because it represents an impossible physical fabric.
    """
    payload = {
        "title": "Midnight Cats",
        "designer": "Stitch Wizards",
        "fabric_count": -14,  # Invalid partition: negative measurement
        "grid_width": 120,
        "grid_height": 120
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 422  # Unprocessable Entity error

def test_create_pattern_boundary_zero_fabric_count():
    """
    Test 6 (BVA - Out-of-Bounds Boundary): Verifies that a fabric_count of exactly 0 
    fails validation, as 0 is the absolute lower limit boundary violation.
    """
    payload = {
        "title": "Summer Meadow",
        "designer": "DMC Labs",
        "fabric_count": 0,  # Boundary condition: exact invalid lower limit
        "grid_width": 150,
        "grid_height": 150
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 422  # Unprocessable Entity error

def test_create_pattern_with_valid_colors():
    """
    Cycle 1 (EP - Valid Partition): Checks that a pattern containing a standard list
    of 5 valid color strings successfully catalogs with a 201 status code.
    """
    payload = {
        "title": "Enchanted Forest",
        "designer": "Barbara Ana",
        "fabric_count": 14,
        "grid_width": 120,
        "grid_height": 140,
        "colors": ["DMC 310", "DMC 666", "DMC 700", "DMC 939", "DMC White"]
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 201
    assert "colors" in response.json()
    assert len(response.json()["colors"]) == 5

def test_create_pattern_maximum_boundary_colors():
    """
    Cycle 2 (BVA - Maximum Boundary): Verifies that a pattern containing exactly
    20 colors (the maximum allowable limit constraint rule) passes successfully.
    """
    twenty_colors = [f"DMC Color {i}" for i in range(1, 21)]  # Generates 20 items
    payload = {
        "title": "Massive Masterpiece",
        "designer": "Long Dog Sampler",
        "fabric_count": 18,
        "grid_width": 300,
        "grid_height": 300,
        "colors": twenty_colors
    }
    response = client.post("/patterns", json=payload)
    assert response.status_code == 201
    assert len(response.json()["colors"]) == 20

def test_create_pattern_invalid_max_colors_violation():
    """
    Cycle 3 (BVA - Out-of-Bounds): Verifies that trying to add a pattern with 21 colors 
    violates our maximum limit rule and is rejected with a 422 Unprocessable Content error.
    """
    twenty_one_colors = [f"DMC Color {i}" for i in range(1, 22)]  # Generates 21 items
    payload = {
        "title": "Too Many Colors",
        "designer": "Stitch Wizards",
        "fabric_count": 14,
        "grid_width": 100,
        "grid_height": 100,
        "colors": twenty_one_colors
    }
    response = client.post("/patterns", json=payload)
    # This assertion WILL fail because our API currently returns a 201 instead of a 422!
    assert response.status_code == 422

# FUNCTIONAL TEST: Checks if listing works and returns 200 OK
def test_hw6_list_all_patterns_functional():
    seed_payload = {
        "title": "Autumn Leaf",
        "designer": "Barbara Ana",
        "fabric_count": 14,
        "grid_width": 100,
        "grid_height": 100
    }
    client.post("/patterns", json=seed_payload)
    response = client.get("/patterns")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# NFR PERFORMANCE TEST
# THRESHOLD: The API must complete a batch loop of 10 list requests in under 100ms.
def test_hw6_list_patterns_load_performance_threshold():
    start_time = time.time()
    
    for _ in range(10):
        response = client.get("/patterns")
        assert response.status_code == 200
        
    end_time = time.time()
    total_elapsed_ms = (end_time - start_time) * 1000
    
    assert total_elapsed_ms < 100, f"Failed: Took {total_elapsed_ms:.2f}ms"
