from fastapi.testclient import TestClient

from backend.main import app

#test to get the chats
def test_get_chats():
    test_client = TestClient(app)
    response = test_client.get("/chats")
    assert response.status_code == 200

def test_get_chat():
    test_client = TestClient(app)
    response = test_client.get("/chats/6215e6864e884132baa01f7f972400e2")
    expected_response = {
  "chat": {
    "id": "6215e6864e884132baa01f7f972400e2",
    "name": "skynet",
    "user_ids": [
      "sarah",
      "terminator"
    ],
    "owner_id": "sarah",
    "created_at": "2023-07-08T18:46:47"
  }
}
    assert response.status_code == 200
    assert response.json() == expected_response

def test_get_chat_wrong_id():
    test_client = TestClient(app)
    response = test_client.get("/chats/uji")
    expected_response = {
  "detail": {
    "type": "entity_not_found",
    "entity_name": "Chat",
    "entity_id": "uji"
  }
}
    assert response.status_code == 404
    assert response.json() == expected_response