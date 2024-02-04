from fastapi.testclient import TestClient

from backend.main import app

# tests to get all the users with request "/users"
def test_get_users():
    test_client = TestClient(app)
    response = test_client.get("/users")
    assert response.status_code == 200


def test_get_user():
    test_client = TestClient(app)
    response = test_client.get("/users/bishop")
    expected_response ={ "user":{
                    "id": "bishop",
                    "created_at": "2014-04-14T10:49:07",
                        }}
    assert response.status_code ==200
    assert response.json() == expected_response

def test_get_user_2():
    """this test is used check that our backend does not break when the user id is invalid"""
    test_client = TestClient(app)
    response = test_client.get("/users/lula")
    expected_response ={"detail": {"type": "entity_not_found","entity_name": "User","entity_id": "lula"}}
    assert response.status_code ==404
    assert response.json() == expected_response


def test_put_existing_user():
    """this test tries to put in existing user"""
    create_param = {"id":"sarah"}
    client = TestClient(app)
    response = client.post("/users",json = create_param)
    assert response.status_code == 422
    assert response.json()["detail"]["type"] == "duplicate_entity"
    assert response.json()["detail"]["entity_name"] == "User"
    assert response.json()["detail"]["entity_id"] == "sarah"

def test_put_user():
    """this test tries to put in a user that does not exists in the database"""
    create_param = {"id":"shubham"}
    client = TestClient(app)
    response = client.post("/users",json=create_param)
    assert response.status_code == 200
    assert response.json()["user"]["id"] == "shubham"


