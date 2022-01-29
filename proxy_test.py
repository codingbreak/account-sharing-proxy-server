import pytest


def test_home_request(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_method(client):
    headers = {"Accept": "application/json"}
    response = client.get("/echo/get/json", headers=headers)
    assert response.json["success"] == "true"


def test_post_method(client):
    headers = {"Content-Type": "application/json"}
    data = {"login": "my_login", "password": "my_password"}
    response = client.post("/echo/post/json", data=data, headers=headers)
    assert response.json["success"] == "true"


def test_put_method(client):
    data = "PUT resquest data"
    response = client.put("/echo/put/json", data=data)
    assert response.json["success"] == "true"


def test_patch_method(client):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"Id": 78912, "Customer": "Jason Sweet", "Quantity": 1}
    response = client.patch("/echo/patch/json", data=data, headers=headers)
    assert response.json["success"] == "true"


def test_delete_method(client):
    headers = {"Accept": "application/json"}
    response = client.delete("/sample/delete/json?id=1", headers=headers)
    assert response.json["success"] == "true"
