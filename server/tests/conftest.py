
import pytest
from app import create_app
from models import db


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test-secret-key-that-is-at-least-32-characters"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    response = client.post("/signup", json={
        "username": "testuser",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = client.post("/login", json={
        "username": "testuser",
        "password": "password123"
    })

    token = response.json["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
