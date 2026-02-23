from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: nothing to set up
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()

def test_signup_for_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

def test_signup_already_registered():
    # Arrange
    email = "emma@mergington.edu"
    activity = "Programming Class"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_unregister_from_activity():
    # Arrange
    email = "mia@mergington.edu"
    activity = "Soccer Team"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_unregister_not_found():
    # Arrange
    email = "notfound@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
