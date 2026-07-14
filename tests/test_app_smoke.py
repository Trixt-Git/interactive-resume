from streamlit.testing.v1 import AppTest


def test_missing_secrets_file_shows_configuration_error(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    app = AppTest.from_file("WilOS.py", default_timeout=15)
    app.run()
    assert not app.exception
    assert [error.value for error in app.error] == ["API key not configured. See README."]


def test_environment_api_key_renders_landing_page(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    app = AppTest.from_file("WilOS.py", default_timeout=15)
    app.run()
    assert not app.exception
    assert [button.label for button in app.button] == [
        "Experience", "Projects", "Systems", "Role Fit"
    ]
    assert len(app.chat_input) == 1
