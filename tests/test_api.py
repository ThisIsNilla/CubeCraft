"""Tests for the FastAPI server."""

from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_create_session():
    response = client.post("/api/sessions", json={"method": "cfop"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["method"] == "CFOP"
    assert data["is_solved"] is True  # Default cube is solved
    assert data["progress_percentage"] == 100.0

def test_create_session_with_scramble():
    response = client.post("/api/sessions", json={
        "method": "beginner",
        "scramble_sequence": "R U R' U'"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_solved"] is False
    assert data["progress_percentage"] < 100.0
    
    # Check that we can fetch it via GET
    session_id = data["session_id"]
    get_resp = client.get(f"/api/sessions/{session_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["facelet_string"] == data["facelet_string"]

def test_apply_move():
    # Setup session
    resp = client.post("/api/sessions", json={"method": "cfop", "scramble_sequence": "R"})
    session_id = resp.json()["session_id"]
    
    # Apply R' to solve it
    move_resp = client.post(f"/api/sessions/{session_id}/moves", json={"move": "R'"})
    assert move_resp.status_code == 200
    data = move_resp.json()
    assert data["is_solved"] is True

def test_get_hint():
    # Setup session with cross off by 1
    resp = client.post("/api/sessions", json={"method": "cfop", "scramble_sequence": "D"})
    session_id = resp.json()["session_id"]
    
    # Get hint
    hint_resp = client.get(f"/api/sessions/{session_id}/hint")
    assert hint_resp.status_code == 200
    hint_data = hint_resp.json()
    assert "hint" in hint_data
    assert hint_data["hint"] == ["D'"]
