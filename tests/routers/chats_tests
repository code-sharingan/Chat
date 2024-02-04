from fastapi.testclient import TestClient

from backend.main import app

#test to get the chats
def test_get_chats():
    test_client = TestClient(app)
    response = test_client.get("/chats")
    assert response.status_code == 200