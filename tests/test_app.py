import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from app import app


def test_duplicate_signup_is_rejected():
    client = TestClient(app)

    response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 200

    duplicate_response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )

    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()
