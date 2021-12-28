import random
from database import User, db


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


def test_login_page_success(client):
    password = str(random.randint(1000, 1000000))
    user: User = User(
        username="username",
        email="email@gmail.com",
        password=User.create_password(password),
    )
    db.session.add(user)
    db.session.commit()
    response = client.post(
        "/login", json={"email": "email@gmail.com", "password": password}
    )
    assert response.status_code == 200
    assert response.get_json() is not None
    assert "access_token" in response.get_json()
