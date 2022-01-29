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
