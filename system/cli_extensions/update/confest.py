# tests/conftest.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from core.application import app

@pytest.fixture
def mock_ai():
    ai = AsyncMock()
    ai.generate.return_value = "Mock AI response"
    return ai

@pytest.fixture
def mock_command_manager():
    cm = MagicMock()
    cm.get_all_commands.return_value = {
        "TEST": {"description": "Test command", "status": False}
    }
    cm.toggle_command.return_value = True
    return cm

@pytest.fixture
def test_client(mock_ai, mock_command_manager):
    app.dependency_overrides[AIConnector] = lambda: mock_ai
    app.dependency_overrides[CommandManager] = lambda: mock_command_manager
    return TestClient(app)