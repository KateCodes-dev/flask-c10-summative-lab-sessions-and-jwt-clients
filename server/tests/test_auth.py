
def test_signup_success(client):
    response = client.post("/signup", json={
        "username": "katelyn",
        "password": "password123",
        "password_confirmation": "password123"
    })

    assert response.status_code == 201
    assert response.json["user"]["username"] == "katelyn"
    assert "token" in response.json


def test_signup_duplicate_username(client):
    data = {
        "username": "katelyn",
        "password": "password123",
        "password_confirmation": "password123"
    }

    client.post("/signup", json=data)
    response = client.post("/signup", json=data)

    assert response.status_code == 422
    assert "Username already exists" in response.json["errors"]


def test_signup_password_mismatch(client):
    response = client.post("/signup", json={
        "username": "katelyn",
        "password": "password123",
        "password_confirmation": "different123"
    })

    assert response.status_code == 422


def test_login_success(client):
    client.post("/signup", json={
        "username": "katelyn",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = client.post("/login", json={
        "username": "katelyn",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_password(client):
    client.post("/signup", json={
        "username": "katelyn",
        "password": "password123",
        "password_confirmation": "password123"
    })

    response = client.post("/login", json={
        "username": "katelyn",
        "password": "wrongpassword"
    })

    assert response.status_code == 401


def test_me_authenticated(client, auth_headers):
    response = client.get("/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json["username"] == "testuser"


def test_me_unauthenticated(client):
    response = client.get("/me")

    assert response.status_code == 401
