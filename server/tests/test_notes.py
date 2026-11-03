
def test_create_note(client, auth_headers):
    response = client.post("/notes", headers=auth_headers, json={
        "title": "My First Note",
        "content": "Learning Flask",
        "category": "Study"
    })

    assert response.status_code == 201
    assert response.json["title"] == "My First Note"
    assert response.json["content"] == "Learning Flask"


def test_get_notes(client, auth_headers):
    client.post("/notes", headers=auth_headers, json={
        "title": "First Note",
        "content": "First content"
    })

    response = client.get("/notes", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json["notes"]) == 1
    assert response.json["pagination"]["page"] == 1


def test_update_note(client, auth_headers):
    created = client.post("/notes", headers=auth_headers, json={
        "title": "Old Title",
        "content": "Old Content"
    })

    note_id = created.json["id"]

    response = client.patch(
        f"/notes/{note_id}",
        headers=auth_headers,
        json={"title": "Updated Title"}
    )

    assert response.status_code == 200
    assert response.json["title"] == "Updated Title"


def test_delete_note(client, auth_headers):
    created = client.post("/notes", headers=auth_headers, json={
        "title": "Delete Me",
        "content": "Temporary note"
    })

    note_id = created.json["id"]

    response = client.delete(
        f"/notes/{note_id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    check = client.get("/notes", headers=auth_headers)

    assert len(check.json["notes"]) == 0


def test_notes_require_authentication(client):
    response = client.get("/notes")

    assert response.status_code == 401


def test_user_cannot_access_another_users_note(client, auth_headers):
    created = client.post("/notes", headers=auth_headers, json={
        "title": "Private Note",
        "content": "This belongs to another user"
    })

    note_id = created.json["id"]

    second_user = client.post("/signup", json={
        "username": "seconduser",
        "password": "password123",
        "password_confirmation": "password123"
    })

    second_token = second_user.json["token"]

    second_headers = {
        "Authorization": f"Bearer {second_token}"
    }

    response = client.get("/notes", headers=second_headers)

    assert response.status_code == 200
    assert len(response.json["notes"]) == 0

    update = client.patch(
        f"/notes/{note_id}",
        headers=second_headers,
        json={"title": "Hacked"}
    )

    assert update.status_code == 404

    delete = client.delete(
        f"/notes/{note_id}",
        headers=second_headers
    )

    assert delete.status_code == 404


def test_notes_pagination(client, auth_headers):
    for number in range(5):
        client.post("/notes", headers=auth_headers, json={
            "title": f"Note {number}",
            "content": f"Content {number}"
        })

    response = client.get(
        "/notes?page=1&per_page=2",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert len(response.json["notes"]) == 2
    assert response.json["pagination"]["total"] == 5
    assert response.json["pagination"]["pages"] == 3


def test_invalid_pagination(client, auth_headers):
    response = client.get(
        "/notes?page=0",
        headers=auth_headers
    )

    assert response.status_code == 400
