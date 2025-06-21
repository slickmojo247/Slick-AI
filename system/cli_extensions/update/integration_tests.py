# tests/integration_tests.py
def test_api_connectivity():
    assert OpenAIAdapter().ping(timeout=5) == STATUS_OK
    assert DeepSeekAdapter().validate_key(KEY) == VALID
    assert TelegramAdapter().bot_online() is True