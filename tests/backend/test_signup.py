from urllib.parse import quote


def test_signup_succeeds_for_new_email(client):
    email = "new.student@mergington.edu"
    activity_path = quote("Chess Club")

    response = client.post(f"/activities/{activity_path}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_duplicate_signup_is_rejected(client):
    email = "test@mergington.edu"
    activity_path = quote("Chess Club")

    first_response = client.post(f"/activities/{activity_path}/signup?email={email}")
    assert first_response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity_path}/signup?email={email}")

    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()


def test_signup_for_unknown_activity_returns_404(client):
    activity_path = quote("Unknown Club")

    response = client.post(
        f"/activities/{activity_path}/signup?email=student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email_query_param(client):
    activity_path = quote("Chess Club")

    response = client.post(f"/activities/{activity_path}/signup")

    assert response.status_code == 422
