import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# AAA: Arrange-Act-Assert

def test_get_activities():
    # Arrange
    # Nenhuma preparação especial necessária

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Remove se já estiver inscrito (idempotente para o teste)
    if email in client.get("/activities").json()[activity]["participants"]:
        client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup
    participants = client.get("/activities").json()[activity]["participants"]
    if email in participants:
        participants.remove(email)

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # Garante que está inscrito
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Activity"
    email = "testuser3@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
