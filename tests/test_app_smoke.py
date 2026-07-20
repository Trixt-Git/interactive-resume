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
        "Experience", "Projects", "Career Change", "Stump Me"
    ]
    assert len(app.chat_input) == 1


def test_how_i_built_this_page_renders():
    app = AppTest.from_file("pages/1_How_I_Built_This.py", default_timeout=15)
    app.run()
    assert not app.exception
    assert app.title[0].value == "How I Built This"
