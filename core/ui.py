"""Shared visual styling for StudyBuddy.

Call `inject_css()` once near the top of every page (after
`st.set_page_config`) to apply a consistent, modern look: custom fonts,
gradient hero banners, card-style containers, polished buttons/metrics, etc.

`render_hero()` and `render_page_header()` are small helpers for consistent
page headers across the app.
"""
import streamlit as st


def _html(markup):
    """Strip leading whitespace from every line so Streamlit's Markdown
    parser doesn't mistake indented HTML for a code block."""
    return "\n".join(line.strip() for line in markup.strip().splitlines())


def inject_css():
    st.markdown(
        _html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"], .stApp, .stMarkdown, p, span, div, label {
            font-family: 'Inter', -apple-system, sans-serif;
        }
        h1, h2, h3, h4, .sb-hero-title {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em;
        }

        /* App background */
        .stApp {
            background: linear-gradient(180deg, #F7F8FD 0%, #F2F3FB 100%);
        }

        /* Hide default Streamlit chrome we don't need */
        #MainMenu, footer { visibility: hidden; }

        /* ---------------- Hero banner ---------------- */
        .sb-hero {
            background: linear-gradient(135deg, #6C5CE7 0%, #4F8CFF 60%, #00C2A8 100%);
            border-radius: 22px;
            padding: 2.2rem 2.4rem;
            margin-bottom: 1.6rem;
            color: #FFFFFF;
            box-shadow: 0 12px 30px -12px rgba(108, 92, 231, 0.55);
        }
        .sb-hero-title {
            font-size: 2.1rem;
            margin: 0 0 0.3rem 0;
            color: #FFFFFF !important;
        }
        .sb-hero-subtitle {
            font-size: 1.02rem;
            opacity: 0.92;
            margin: 0;
        }
        .sb-badge {
            display: inline-block;
            background: rgba(255,255,255,0.18);
            border: 1px solid rgba(255,255,255,0.35);
            border-radius: 999px;
            padding: 0.18rem 0.85rem;
            font-size: 0.82rem;
            font-weight: 600;
            margin-bottom: 0.6rem;
            backdrop-filter: blur(4px);
        }

        /* ---------------- Page header (non-hero pages) ---------------- */
        .sb-page-header {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 1.4rem 1.8rem;
            margin-bottom: 1.4rem;
            border: 1px solid #ECEDF6;
            box-shadow: 0 6px 18px -14px rgba(31, 36, 51, 0.25);
        }
        .sb-page-header h1 {
            font-size: 1.6rem;
            margin: 0 0 0.15rem 0;
            background: linear-gradient(135deg, #6C5CE7 0%, #4F8CFF 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .sb-page-header p {
            margin: 0;
            color: #6B7280;
        }

        /* ---------------- Cards ---------------- */
        .sb-card {
            background: #FFFFFF;
            border-radius: 18px;
            padding: 1.4rem 1.3rem;
            border: 1px solid #ECEDF6;
            box-shadow: 0 8px 24px -16px rgba(31, 36, 51, 0.25);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            height: 100%;
        }
        .sb-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 14px 28px -16px rgba(108, 92, 231, 0.35);
        }
        .sb-card .sb-card-icon {
            font-size: 1.7rem;
            margin-bottom: 0.4rem;
        }
        .sb-card h3, .sb-card h4 {
            margin: 0 0 0.35rem 0;
        }
        .sb-card p {
            color: #6B7280;
            font-size: 0.92rem;
            margin-bottom: 0;
        }
        .sb-step-num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.7rem;
            height: 1.7rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #6C5CE7, #4F8CFF);
            color: #fff;
            font-size: 0.85rem;
            font-weight: 700;
            margin-right: 0.45rem;
        }

        /* ---------------- Metrics ---------------- */
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid #ECEDF6;
            border-radius: 16px;
            padding: 1rem 1.1rem 0.7rem 1.1rem;
            box-shadow: 0 8px 20px -16px rgba(31, 36, 51, 0.25);
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Poppins', sans-serif;
            color: #4F46E5;
        }

        /* ---------------- Buttons ---------------- */
        div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button {
            border-radius: 12px;
            font-weight: 600;
            transition: transform 0.1s ease, box-shadow 0.15s ease;
            border: 1px solid #E4E6F4;
        }
        div[data-testid="stButton"] button:hover, div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 18px -10px rgba(108, 92, 231, 0.55);
        }
        div[data-testid="stButton"] button[kind="primary"], div[data-testid="stFormSubmitButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #6C5CE7 0%, #4F8CFF 100%);
            border: none;
        }

        /* ---------------- Page links ---------------- */
        [data-testid="stPageLink"] {
            border-radius: 12px;
            border: 1px solid #ECEDF6;
            background: #FAFAFE;
            transition: background 0.15s ease, transform 0.1s ease;
        }
        [data-testid="stPageLink"]:hover {
            background: #EEF0FE;
            transform: translateY(-1px);
        }

        /* ---------------- Sidebar ---------------- */
        [data-testid="stSidebar"] {
            background: #FFFFFF;
            border-right: 1px solid #ECEDF6;
        }

        /* ---------------- Containers with border (st.container(border=True)) ---------------- */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            border-radius: 16px !important;
        }

        /* ---------------- Progress bar ---------------- */
        div[data-testid="stProgress"] > div > div {
            background: linear-gradient(135deg, #6C5CE7 0%, #00C2A8 100%);
        }

        /* ---------------- Dataframe ---------------- */
        [data-testid="stDataFrame"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid #ECEDF6;
        }
        </style>
        """),
        unsafe_allow_html=True,
    )


def render_hero(title, subtitle, badge=None):
    """Render a large gradient hero banner used on the home page and login screen."""
    badge_html = f'<div class="sb-badge">{badge}</div>' if badge else ""
    st.markdown(
        _html(f"""
        <div class="sb-hero">
            {badge_html}
            <div class="sb-hero-title">{title}</div>
            <p class="sb-hero-subtitle">{subtitle}</p>
        </div>
        """),
        unsafe_allow_html=True,
    )


def render_page_header(title, subtitle=""):
    """Render a compact gradient-text page header used on each tool page."""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        _html(f"""
        <div class="sb-page-header">
            <h1>{title}</h1>
            {subtitle_html}
        </div>
        """),
        unsafe_allow_html=True,
    )


def hide_sidebar_nav():
    """Hide the auto-generated multipage navigation list in the sidebar.

    Used on the login / profile-picker screens so users aren't shown links
    to pages they can't access yet.
    """
    st.markdown(
        "<style>[data-testid='stSidebarNav'] { display: none; }</style>",
        unsafe_allow_html=True,
    )
