"""Login + profile picker, shared across all pages."""
import streamlit as st

from core import db
from core.auth import APP_PASSWORD, GRADES
from core.ui import _html, hide_sidebar_nav, inject_css, render_hero


def require_login():
    """Show login + profile picker if needed. Returns the active profile dict.

    Stops page execution (st.stop) until the user is logged in AND has an
    active profile selected.
    """
    inject_css()

    if not st.session_state.get("authenticated"):
        hide_sidebar_nav()
        _show_login()
        st.stop()

    if not st.session_state.get("profile"):
        hide_sidebar_nav()
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
    render_hero(
        "📚 StudyBuddy",
        "Your family's AI-powered exam prep dashboard — personalised lessons, "
        "practice papers, and progress tracking for every subject and grade.",
        badge="🔒 Family login",
    )
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.container(border=True):
            st.markdown("#### Enter your household password")
            with st.form("login_form"):
                password = st.text_input("Household password", type="password")
                submitted = st.form_submit_button("Log in →", type="primary", use_container_width=True)
            if submitted:
                if password == APP_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")


def _show_profile_picker():
    render_hero(
        "🙋 Who's studying today?",
        "Pick your profile to jump back into your lessons and practice papers, "
        "or create a new profile for another grade.",
    )

    profiles = db.list_profiles()
    if profiles:
        cols = st.columns(min(len(profiles), 4))
        for i, p in enumerate(profiles):
            with cols[i % 4]:
                st.markdown(
                    _html(f"""
                    <div class="sb-card" style="text-align:center;">
                        <div class="sb-card-icon">🧑‍🎓</div>
                        <h4 style="margin-bottom:0;">{p['name']}</h4>
                        <p>Grade {p['grade']}</p>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )
                st.write("")
                if st.button("Continue", key=f"profile_{p['id']}", use_container_width=True, type="primary"):
                    st.session_state["profile"] = p
                    st.rerun()

    st.write("")
    st.divider()
    st.markdown("#### ➕ Add a new student profile")
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        with st.container(border=True):
            with st.form("new_profile_form"):
                name = st.text_input("Name")
                grade = st.selectbox("Grade / Standard", GRADES, index=6)
                submitted = st.form_submit_button("Create profile →", type="primary", use_container_width=True)
            if submitted:
                if not name.strip():
                    st.error("Please enter a name.")
                else:
                    pid = db.create_profile(name.strip(), grade)
                    st.session_state["profile"] = db.get_profile(pid)
                    st.rerun()
