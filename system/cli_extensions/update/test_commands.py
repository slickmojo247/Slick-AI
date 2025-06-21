# tests/test_commands.py
def test_toggle_command(test_client, mock_command_manager):
    response = test_client.post("/commands/TEST/toggle")
    assert response.status_code == 200
    assert response.json()["enabled"] is True
    mock_command_manager.toggle_command.assert_called_with("TEST")

def test_list_commands(test_client, mock_command_manager):
    response = test_client.get("/commands")
    assert response.status_code == 200
    assert "TEST" in response.json()