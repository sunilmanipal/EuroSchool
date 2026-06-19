"""Login + profile picker, shared across all pages."""
import streamlit as st

from core import db
from core.auth import APP_PASSWORD, GRADES
from core.ui import _html, hide_sidebar_nav, inject_css

# Fun avatar emojis assigned round-robin by profile id
_AVATARS = ["🦁", "🐯", "🦊", "🐸", "🐧", "🦋", "🐳", "🦄", "🐉", "🌟", "🚀", "🎩"]

# One bright accent colour per avatar (matching order)
_AVATAR_COLORS = [
    "#FF6B35", "#FF9F1C", "#2EC4B6", "#E71D36", "#3F37C9",
    "#7209B7", "#4361EE", "#06D6A0", "#EF233C", "#F72585",
    "#4CC9F0", "#560BAD",
]

_KID_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&display=swap');

/* ── Dark theme login / profile styles ── */

/* Full-page banner for auth screens */
.kid-bg {
    background: linear-gradient(135deg, #0D0520 0%, #0A1628 50%, #050E1A 100%);
    border: 1px solid rgba(124, 58, 237, 0.35);
    border-radius: 28px;
    padding: 2.8rem 1.5rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 80px -20px rgba(124, 58, 237, 0.4),
                0 30px 60px -20px rgba(0,0,0,0.7);
    margin-bottom: 1.5rem;
}
.kid-bg::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(124,58,237,0.25) 0%, transparent 70%);
    pointer-events: none;
}
.kid-bg::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 20%;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(6,182,212,0.18) 0%, transparent 70%);
    pointer-events: none;
}

/* Big title */
.kid-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #E0C3FC 0%, #67E8F9 60%, #A7F3D0 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    margin: 0 0 0.35rem 0 !important;
    line-height: 1.15;
    position: relative;
}

/* Subtitle */
.kid-subtitle {
    font-size: 1.1rem;
    color: #64748B !important;
    margin: 0 0 1.8rem 0;
    font-weight: 500;
    position: relative;
}

/* Emoji row */
.kid-emoji-row {
    font-size: 2.2rem;
    letter-spacing: 0.35rem;
    margin-bottom: 1.2rem;
    position: relative;
}

/* Password card heading */
.kid-card {
    text-align: left;
    margin-bottom: 0.5rem;
}
.kid-card h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.2rem !important;
    color: #A78BFA !important;
    margin-bottom: 0.6rem !important;
    font-weight: 700 !important;
}

/* Profile cards grid */
.kid-profile-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.2rem;
    justify-content: center;
    margin-bottom: 1.5rem;
}

.kid-profile-card {
    background: linear-gradient(145deg, #0F1623, #111827);
    border-radius: 22px;
    padding: 1.6rem 1.3rem 1.2rem;
    border: 1px solid rgba(124, 58, 237, 0.25);
    box-shadow: 0 8px 30px -10px rgba(0,0,0,0.5),
                inset 0 1px 0 rgba(255,255,255,0.04);
    text-align: center;
    min-width: 155px;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.kid-profile-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.5), transparent);
}
.kid-profile-card:hover {
    transform: translateY(-6px) scale(1.04);
    border-color: rgba(167, 139, 250, 0.6);
    box-shadow: 0 0 30px rgba(124, 58, 237, 0.3),
                0 20px 40px -15px rgba(0,0,0,0.6);
}
.kid-avatar {
    font-size: 3.6rem;
    margin-bottom: 0.5rem;
    display: block;
    filter: drop-shadow(0 0 10px rgba(124,58,237,0.4));
}
.kid-profile-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #E2E8F0 !important;
    margin-bottom: 0.3rem;
}
.kid-grade-badge {
    display: inline-block;
    border-radius: 999px;
    padding: 0.2rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: #fff;
    margin-top: 0.25rem;
    box-shadow: 0 0 12px rgba(124, 58, 237, 0.4);
}

/* Section heading for "Add new student" */
.kid-section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(90deg, #A78BFA, #67E8F9);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    margin: 0.5rem 0 0.8rem 0;
    text-align: center;
}
</style>
"""


def require_login():
    """Show login + profile picker if needed. Returns the active profile dict."""
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
    avatar = _AVATARS[profile["id"] % len(_AVATARS)]
    with st.sidebar:
        st.markdown(
            f"<div style='text-align:center;font-size:2rem;'>{avatar}</div>"
            f"<div style='text-align:center;font-weight:700;font-size:1rem;color:#3F37C9'>"
            f"{profile['name']}</div>"
            f"<div style='text-align:center;color:#888;font-size:0.85rem;'>Grade {profile['grade']}</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Switch profile", use_container_width=True):
            st.session_state.pop("profile", None)
            st.rerun()
        if st.button("Log out", use_container_width=True):
            st.session_state.pop("authenticated", None)
            st.session_state.pop("profile", None)
            st.rerun()

    return profile


def _show_login():
    st.markdown(_KID_CSS, unsafe_allow_html=True)

    st.markdown(
        _html("""
        <div class="kid-bg">
            <div class="kid-emoji-row">📚 ✏️ 🔬 🧮 🌍</div>
            <div class="kid-title">Welcome to StudyBuddy!</div>
            <p class="kid-subtitle">Your super-smart AI tutor — lessons, tests & fun learning every day!</p>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.write("")
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown(
            _html("""
            <div class="kid-card">
                <h3>🔑 Enter your family password</h3>
            </div>
            """),
            unsafe_allow_html=True,
        )
        with st.container(border=True):
            with st.form("login_form"):
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Type the secret password...",
                )
                submitted = st.form_submit_button(
                    "🚀 Let's Go!", type="primary", use_container_width=True
                )
            if submitted:
                if password == APP_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Wrong password — ask a grown-up for help!")


def _show_profile_picker():
    st.markdown(_KID_CSS, unsafe_allow_html=True)

    st.markdown(
        _html("""
        <div class="kid-bg">
            <div class="kid-emoji-row">🦁 🐯 🦊 🐸 🐧</div>
            <div class="kid-title">Who's learning today? 🙋</div>
            <p class="kid-subtitle">Pick your name and jump straight into your lessons!</p>
        </div>
        """),
        unsafe_allow_html=True,
    )

    st.write("")
    profiles = db.list_profiles()

    if profiles:
        cols = st.columns(min(len(profiles), 4))
        for i, p in enumerate(profiles):
            avatar = _AVATARS[p["id"] % len(_AVATARS)]
            color = _AVATAR_COLORS[p["id"] % len(_AVATAR_COLORS)]
            with cols[i % 4]:
                st.markdown(
                    _html(f"""
                    <div class="kid-profile-card" style="border-color:{color}22;">
                        <span class="kid-avatar">{avatar}</span>
                        <div class="kid-profile-name">{p['name']}</div>
                        <span class="kid-grade-badge" style="background:{color};">Grade {p['grade']}</span>
                    </div>
                    """),
                    unsafe_allow_html=True,
                )
                st.write("")
                if st.button(
                    f"▶ That's me!",
                    key=f"profile_{p['id']}",
                    use_container_width=True,
                    type="primary",
                ):
                    st.session_state["profile"] = p
                    st.rerun()

    st.write("")
    st.divider()

    st.markdown(
        '<p class="kid-section-heading">➕ New student? Add your profile here!</p>',
        unsafe_allow_html=True,
    )
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        with st.container(border=True):
            with st.form("new_profile_form"):
                name = st.text_input("Your name", placeholder="e.g. Arjun")
                grade = st.selectbox("Your grade / standard", GRADES, index=6)
                submitted = st.form_submit_button(
                    "✅ Create my profile!", type="primary", use_container_width=True
                )
            if submitted:
                if not name.strip():
                    st.error("Please type your name first!")
                else:
                    pid = db.create_profile(name.strip(), grade)
                    st.session_state["profile"] = db.get_profile(pid)
                    st.rerun()
