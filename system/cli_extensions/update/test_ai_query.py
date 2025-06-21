# tests/test_ai.py
def test_ai_query(test_client, mock_ai):
    response = test_client.post("/ai/query", json={"prompt": "Test prompt"})
    assert response.status_code == 200
    assert response.json()["response"] == "Mock AI response"
    mock_ai.generate.assert_called_with("Test prompt", model="hybrid")