"""
Optional simple authentication for the app.
Set require_auth = true and password = "..." in .streamlit/secrets.toml to enable.
"""
import streamlit as st


def require_auth() -> bool:
    """
    If require_auth is set in secrets, gate access until password is correct.
    Returns True if user may proceed, False if login form is shown (call st.stop() after).
    """
    try:
        if not st.secrets.get("require_auth", False):
            return True
    except (FileNotFoundError, AttributeError):
        return True

    return check_password()


def check_password() -> bool:
    """
    Simple password check using Streamlit secrets.
    Set password in .streamlit/secrets.toml.
    Returns True if authenticated.
    """
    if st.session_state.get("authenticated"):
        return True

    try:
        expected = st.secrets.get("password")
    except (FileNotFoundError, AttributeError):
        expected = None

    if not expected:
        return True  # No password configured, allow access

    def _login():
        pwd = st.session_state.get("password_input", "")
        if pwd == expected:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid password")

    st.markdown("#### Sign in")
    with st.form("auth", clear_on_submit=True):
        st.text_input("Password", type="password", key="password_input", label_visibility="collapsed")
        st.form_submit_button("Login", on_click=_login)
    st.caption("Enter the password to access the portal.")
    return False


def logout():
    """Clear authentication state."""
    if "authenticated" in st.session_state:
        del st.session_state.authenticated
    st.rerun()


def render_sidebar_auth() -> None:
    """Show logout button in sidebar when authenticated."""
    if st.session_state.get("authenticated"):
        try:
            if st.secrets.get("require_auth", False):
                st.sidebar.divider()
                if st.sidebar.button("Logout", key="logout_btn"):
                    logout()
        except (FileNotFoundError, AttributeError):
            pass
