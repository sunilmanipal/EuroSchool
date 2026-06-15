"""Login + profile picker, shared across all pages."""
import streamlit as st

from core import db
from core.auth import APP_PASSWORD, GRADES


def require_login():
    """Show login + profile picker if needed. Returns the active profile dict.

    Stops page execution (st.stop) until the user is logged in AND has an
    active profile selected.
    """
    if not st.session_state.get("authenticated"):
        _show_login()
        st.stop()

    if not st.session_state.get("profile"):
        _show_profile_picker()
        st.stop()

    profile = st.session_state["profile"]
    with st.sidebar:
        st.success(f"👤 **{profile['name']}** — Grade {profile['grade']}")
        if st.button("Switch profile", use_container_width=True):
            st.session_state.pop("profile", None)
            st.rerun()
        if st.button("Log out", use_container_width=True):
            st.session_state.pop("authenticated", None)
            st.session_state.pop("profile", None)
            st.rerun()

    return profile


def _show_login():
    st.title("📚 StudyBuddy — Exam Prep Dashboard")
    st.markdown("### 🔒 Family login")
    with st.form("login_form"):
        password = st.text_input("Household password", type="password")
        submitted = st.form_submit_button("Log in", type="primary")
    if submitted:
        if password == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")


def _show_profile_picker():
    st.title("📚 StudyBuddy — Exam Prep Dashboard")
    st.markdown("### 🙋 Who's studying today?")

    profiles = db.list_profiles()
    if profiles:
        cols = st.columns(min(len(profiles), 4))
        for i, p in enumerate(profiles):
            with cols[i % 4]:
                if st.button(
                    f"{p['name']}\n\nGrade {p['grade']}",
                    key=f"profile_{p['id']}",
                    use_container_width=True,
                ):
                    st.session_state["profile"] = p
                    st.rerun()

    st.divider()
    st.markdown("#### ➕ Add a new student profile")
    with st.form("new_profile_form"):
        name = st.text_input("Name")
        grade = st.selectbox("Grade / Standard", GRADES, index=6)
        submitted = st.form_submit_button("Create profile", type="primary")
    if submitted:
        if not name.strip():
            st.error("Please enter a name.")
        else:
            pid = db.create_profile(name.strip(), grade)
            st.session_state["profile"] = db.get_profile(pid)
            st.rerun()
