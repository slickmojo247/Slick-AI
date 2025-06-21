"""Merges:
- test_ai_router.py
- test_service_control.py 
- integration_tests.py
- post_reset_validation.py
"""
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def full_mock_environment():
    return {
        'openai': AsyncMock(),
        'deepseek': AsyncMock(),
        'vscode': AsyncMock(),
        'services': {
            'slick-controller': {'status': 'running'},
            'vscode-bridge': {'status': 'stopped'}
        }
    }

def test_ai_routing(full_mock_environment):
    router = AIRouter(providers=full_mock_environment)
    assert router.route_request("test") is not None

def test_service_lifecycle(full_mock_environment):
    manager = ServiceManager(services=full_mock_environment['services'])
    assert manager.start_service('vscode-bridge') == 'running'

def test_project_structure():
    validator = ProjectValidator([
        "slick/api/main.py",
        "web_interface/src/App.vue" 
    ])
    assert validator.validate()