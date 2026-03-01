
# tests/test_app.py

"""Tests for the FastAPI application using the Arrange-Act-Assert pattern."""

from fastapi import status

from src.app import activities


def test_root_redirect(client):
    # Arrange: nothing special, client fixture provided

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"].endswith("/static/index.html")


def test_get_empty_activities(client):
    # Arrange: explicitly clear activities for this scenario
    activities.clear()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}


def test_successful_signup_and_listing(client):
    # Arrange: create a new activity with empty participants
    activities["yoga"] = {"participants": []}
    email = "alice@example.com"

    # Act
    post_resp = client.post("/activities/yoga/signup", json={"email": email})

    # Assert
    assert post_resp.status_code == status.HTTP_201_CREATED

    # Act again
    get_resp = client.get("/activities")
    assert get_resp.status_code == status.HTTP_200_OK
    assert email in get_resp.json()["yoga"]["participants"]


def test_duplicate_signup(client):
    # Arrange: ensure activity exists with one participant
    activities["piano"] = {"participants": ["bob@example.com"]}
    email = "bob@example.com"

    # Act
    dup_resp = client.post("/activities/piano/signup", json={"email": email})

    # Assert
    assert dup_resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "already signed up" in dup_resp.json()["detail"].lower()


def test_remove_signup(client):
    # Arrange
    activities["painting"] = {"participants": ["carol@example.com"]}
    email = "carol@example.com"

    # Act
    delete_resp = client.request("DELETE", "/activities/painting/signup", json={"email": email})

    # Assert
    assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    # Confirm removal
    get_resp = client.get("/activities")
    assert email not in get_resp.json()["painting"]["participants"]


def test_remove_nonexistent(client):
    # Arrange: activity exists but no participants
    activities["swimming"] = {"participants": []}
    email = "dave@example.com"

    # Act
    del_resp = client.request("DELETE", "/activities/swimming/signup", json={"email": email})

    # Assert
    assert del_resp.status_code == status.HTTP_404_NOT_FOUND
    assert "not signed up" in del_resp.json()["detail"].lower()


def test_unknown_activity(client):
    # Arrange
    email = "eve@example.com"

    # Act
    resp_post = client.post("/activities/unknown/signup", json={"email": email})
    resp_del = client.request("DELETE", "/activities/unknown/signup", json={"email": email})

    # Assert
    assert resp_post.status_code == status.HTTP_404_NOT_FOUND
    assert resp_del.status_code == status.HTTP_404_NOT_FOUND
