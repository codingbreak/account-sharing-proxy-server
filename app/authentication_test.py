import pytest

from app.models import User, db


def test_login_page_failed(client):
    repsonse1 = client.post("/login")
    response2 = client.post(
        "/login", json={"email": "notexist@gmail.com", "password": "password"}
    )
    for response in [repsonse1, response2]:
        assert response.status_code == 401
        assert response.get_json() is not None
        assert "msg" in response.get_json()
    assert (
        repsonse1.get_json()["msg"]
        == "This endpoint only accept application/json content type"
    )
    assert response2.get_json()["msg"] == "Bad username or password"


def test_login_success(client):
    # Create user
    user = User(username="username", email="user@gmail.com")
    user.password = user.create_password("user password")
    db.session.add(user)
    db.session.commit()
    response = client.post(
        "/login", json={"email": "user@gmail.com", "password": "user password"}
    )
    assert response.status_code == 200
    assert response.json["access_token"] != None


def test_register_user(client):
    email = "user-email@gmail.com"
    password = "user passowrd"
    username = "username"
    fullname = "fullname"

    payload_empty_password = {"email": email}
    response_empty_password = client.post("/register", json=payload_empty_password)
    assert response_empty_password.status_code == 400
    assert (
        response_empty_password.json["msg"] == "Please provide both email and password"
    )

    payload_empty_username = {"email": email, "password": password}
    response_empty_username = client.post("/register", json=payload_empty_username)
    assert response_empty_username.status_code == 500

    payload = {"email": email, "password": password, "username": username}
    response = client.post("/register", json=payload)
    assert response.status_code == 201
    assert response.json["msg"] == "User is registered"

    # try to login with registered user
    login_payload = {"email": email, "password": password}
    login_resp = client.post("/login", json=login_payload)
    assert login_resp.status_code == 200
    assert login_resp.json != None
    assert login_resp.json["access_token"] != None
