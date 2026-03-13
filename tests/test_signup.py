from src import app as app_module


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    missing_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{missing_activity}/signup", params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = app_module.activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"
