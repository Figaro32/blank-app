"""
Optional simple authentication for the app.
"""
import streamlit as st


def check_password() -> bool:
    """
    Simple password check using Streamlit secrets.
    Set STREAMLIT_SERVER_PASSWORD in environment or secrets.
    Returns True if authenticated.
    """
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True

    def _login():
        pwd = st.session_state.get("password_input", "")
        expected = st.secrets.get("password") if hasattr(st, "secrets") else None
        if expected and pwd == expected:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid password")

    with st.form("auth"):
        st.text_input("Password", type="password", key="password_input")
        st.form_submit_button("Login", on_click=_login)
    return False


def logout():
    """Clear authentication state."""
    if "authenticated" in st.session_state:
        del st.session_state.authenticated
    st.rerun()
