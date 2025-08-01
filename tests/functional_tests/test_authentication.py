"""Functional tests for authentication and email management."""


########################################################
#           UNKNOWN EMAIL REDIRECTS TO INDEX PAGE
########################################################


def test_unknown_email_redirects_to_index(test_app):
    """Test that an unknown email redirects to the index page"""
    with test_app.test_client() as client:
        response = client.post(
            "/show_summary", 
            data={"email": "unknown@example.com"},
            follow_redirects=True
        )
        assert response.request.path == "/"


########################################################
#           UNKNOWN EMAIL DISPLAYS ERROR MESSAGE
########################################################


def test_unknown_email_displays_error_message(test_app):
    """
    Test that an unknown email displays an error message 
    after redirect
    """
    with test_app.test_client() as client:
        response = client.post(
            "/show_summary", 
            data={"email": "unknown@example.com"},
            follow_redirects=True
        )
        assert "Unknown email" in response.data.decode("utf-8")
