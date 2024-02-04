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



def test_put_correct_name():
    test_client = TestClient(app)
    create_param = {"name":"hello"}
    expected_response ={
  "chat": {
    "id": "660c7a6bc1324e4488cafabc59529c93",
    "name": "hello",
    "user_ids": [
      "reese",
      "sarah"
    ],
    "owner_id": "reese",
    "created_at": "2023-04-12T20:11:21"
  }
}
    response = test_client.post("/chats/660c7a6bc1324e4488cafabc59529c93",json = create_param)
    assert response.status_code ==200
    assert response.json() ==  expected_response


def test_put_wrong_id():
    test_client = TestClient(app)
    create_param = {"name":"hello"}
    expected_response ={
  "detail": {
    "type": "entity_not_found",
    "entity_name": "Chat",
    "entity_id": "jj"
  }
}
    response = test_client.post("/chats/jj",json = create_param)
    assert response.status_code ==404
    assert response.json() ==  expected_response
    
def test_delete():
    test_client =TestClient(app)
    response = test_client.delete("/chats/660c7a6bc1324e4488cafabc59529c93")
    assert response.status_code ==204

def test_delete_invalid_id():
    test_client=TestClient(app)
    expected_response ={
  "detail": {
    "type": "entity_not_found",
    "entity_name": "Chat",
    "entity_id": "ujj"
  }
}
    response = test_client.delete("/chats/ujj")
    assert response.status_code ==404
    assert response.json() == expected_response

    
    
    
    