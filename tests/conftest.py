import pytest

from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture

def client():
    """Return a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Save a copy of the original activities mapping and restore it after each test.

    This ensures tests can modify the dict (add/remove entries or participants)
    without affecting other cases.
    """
    import copy

    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))
