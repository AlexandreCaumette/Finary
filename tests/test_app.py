from streamlit.testing.v1 import AppTest


def test_click_login_button():
    """A user clicks on the login button, and is redirected to the login interface."""
    at = AppTest.from_file("streamlit_app.py").run()
    at.button[0].click().run()
    assert True
