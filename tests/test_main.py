from tests.reqover import cover


def test_can_get_swagger_json(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_can_get_status(client):
    response = cover(client.get("/status"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_can_get_item_by_id(client):
    response = cover(client.get("/items/foo", headers={"X-Token": "coneofsilence"}))
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_can_not_read_item_without_token(client):
    response = cover(client.get("/items/foo"))
    assert response.status_code == 422


def test_read_item_bad_token(client):
    response = cover(client.get("/items/foo", headers={"X-Token": "hailhydra"}))
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_item(client):
    response = cover(client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    ))
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token(client):
    response = cover(client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    ))
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_can_not_create_item_without_token(client):
    response = cover(client.post(
        "/items/",
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    ))
    assert response.status_code == 422
