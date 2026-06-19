"""Shared visual styling for StudyBuddy — dark premium theme.

Call `inject_css()` once near the top of every page (after
`st.set_page_config`) to apply the dark glassmorphism theme.

`render_hero()` and `render_page_header()` are helpers for consistent
page headers across the app.
"""
import streamlit as st


def _html(markup):
    """Strip leading whitespace so Streamlit doesn't treat indented HTML as code."""
    return "\n".join(line.strip() for line in markup.strip().splitlines())


def inject_css():
    st.markdown(
        _html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        /* ═══════════════════════════════════════════════
           BASE — dark background, crisp white text
        ═══════════════════════════════════════════════ */
        html, body, [class*="css"], .stApp, .stMarkdown, p, span, div, label,
        .stTextInput input, .stSelectbox, .stSlider, textarea {
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #E2E8F0;
        }
        h1, h2, h3, h4, h5, .sb-hero-title {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* App background — deep near-black */
        .stApp {
            background: #080B14 !important;
        }

        /* Main content area */
        .main .block-container {
            background: transparent !important;
            padding-top: 1.5rem;
        }

        /* Hide default chrome */
        #MainMenu, footer { visibility: hidden; }

        /* Dark top toolbar */
        [data-testid="stToolbar"], header[data-testid="stHeader"] {
            background: #080B14 !important;
            border-bottom: 1px solid rgba(124, 58, 237, 0.15) !important;
        }
        [data-testid="stToolbar"] * { color: #475569 !important; }
        header[data-testid="stHeader"] { background: #080B14 !important; }

        /* ═══════════════════════════════════════════════
           SIDEBAR
        ═══════════════════════════════════════════════ */
        [data-testid="stSidebar"] {
            background: #0D1117 !important;
            border-right: 1px solid rgba(124, 58, 237, 0.25) !important;
        }
        [data-testid="stSidebar"] * {
            color: #CBD5E1 !important;
        }
        [data-testid="stSidebarNav"] a {
            color: #94A3B8 !important;
            border-radius: 10px;
            padding: 0.4rem 0.8rem;
            transition: background 0.15s, color 0.15s;
        }
        [data-testid="stSidebarNav"] a:hover,
        [data-testid="stSidebarNav"] a[aria-current] {
            background: rgba(124, 58, 237, 0.18) !important;
            color: #A78BFA !important;
        }
        [data-testid="stSidebarNav"] a[aria-current] {
            background: rgba(124, 58, 237, 0.28) !important;
            color: #C4B5FD !important;
            font-weight: 600 !important;
        }

        /* ═══════════════════════════════════════════════
           HERO BANNER — vivid purple→cyan gradient
        ═══════════════════════════════════════════════ */
        .sb-hero {
            background: linear-gradient(135deg, #1A0533 0%, #0D1B3E 40%, #061A2B 100%);
            border: 1px solid rgba(124, 58, 237, 0.4);
            border-radius: 24px;
            padding: 2.4rem 2.8rem;
            margin-bottom: 1.8rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 60px -10px rgba(124, 58, 237, 0.35),
                        0 20px 40px -20px rgba(0, 0, 0, 0.6);
        }
        .sb-hero::before {
            content: '';
            position: absolute;
            top: -60px; right: -60px;
            width: 280px; height: 280px;
            background: radial-gradient(circle, rgba(124,58,237,0.3) 0%, transparent 70%);
            pointer-events: none;
        }
        .sb-hero::after {
            content: '';
            position: absolute;
            bottom: -40px; left: 30%;
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(6,182,212,0.2) 0%, transparent 70%);
            pointer-events: none;
        }
        .sb-hero-title {
            font-size: 2.2rem;
            margin: 0 0 0.4rem 0;
            background: linear-gradient(90deg, #E0C3FC 0%, #8EC5FC 50%, #43E8D8 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
            position: relative;
        }
        .sb-hero-subtitle {
            font-size: 1.0rem;
            color: #94A3B8 !important;
            margin: 0;
            position: relative;
        }
        .sb-badge {
            display: inline-block;
            background: rgba(124, 58, 237, 0.2);
            border: 1px solid rgba(167, 139, 250, 0.5);
            border-radius: 999px;
            padding: 0.2rem 1rem;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
            color: #C4B5FD !important;
            letter-spacing: 0.03em;
            position: relative;
        }

        /* ═══════════════════════════════════════════════
           PAGE HEADER (non-hero pages)
        ═══════════════════════════════════════════════ */
        .sb-page-header {
            background: linear-gradient(135deg, #0D1117 0%, #111827 100%);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 20px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.6rem;
            box-shadow: 0 4px 24px -8px rgba(124, 58, 237, 0.2),
                        inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .sb-page-header h1 {
            font-size: 1.65rem;
            margin: 0 0 0.2rem 0;
            background: linear-gradient(90deg, #A78BFA 0%, #67E8F9 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
        }
        .sb-page-header p {
            margin: 0;
            color: #64748B !important;
            font-size: 0.92rem;
        }

        /* ═══════════════════════════════════════════════
           CARDS
        ═══════════════════════════════════════════════ */
        .sb-card {
            background: linear-gradient(145deg, #0F1623 0%, #111827 100%);
            border: 1px solid rgba(124, 58, 237, 0.22);
            border-radius: 20px;
            padding: 1.5rem 1.4rem;
            transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        .sb-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(167,139,250,0.5), transparent);
        }
        .sb-card:hover {
            transform: translateY(-4px);
            border-color: rgba(124, 58, 237, 0.55);
            box-shadow: 0 0 30px -5px rgba(124, 58, 237, 0.25),
                        0 20px 40px -20px rgba(0,0,0,0.5);
        }
        .sb-card .sb-card-icon {
            font-size: 1.9rem;
            margin-bottom: 0.55rem;
            display: block;
        }
        .sb-card h3, .sb-card h4 {
            margin: 0 0 0.4rem 0;
            color: #E2E8F0 !important;
        }
        .sb-card p {
            color: #64748B !important;
            font-size: 0.9rem;
            margin-bottom: 0;
            line-height: 1.55;
        }
        .sb-step-num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.8rem;
            height: 1.8rem;
            border-radius: 50%;
            background: linear-gradient(135deg, #7C3AED, #06B6D4);
            color: #fff;
            font-size: 0.82rem;
            font-weight: 700;
            margin-right: 0.5rem;
            box-shadow: 0 0 10px rgba(124,58,237,0.5);
        }

        /* ═══════════════════════════════════════════════
           METRICS
        ═══════════════════════════════════════════════ */
        div[data-testid="stMetric"] {
            background: linear-gradient(145deg, #0F1623, #111827) !important;
            border: 1px solid rgba(124, 58, 237, 0.25) !important;
            border-radius: 18px !important;
            padding: 1.1rem 1.2rem 0.8rem !important;
            box-shadow: 0 4px 20px -8px rgba(124, 58, 237, 0.15) !important;
        }
        div[data-testid="stMetricLabel"] p {
            color: #64748B !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="stMetricValue"] {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #A78BFA !important;
            font-size: 2rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricDelta"] {
            color: #22D3EE !important;
        }

        /* ═══════════════════════════════════════════════
           BUTTONS
        ═══════════════════════════════════════════════ */
        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.18s ease !important;
            border: 1px solid rgba(124, 58, 237, 0.35) !important;
            background: rgba(124, 58, 237, 0.08) !important;
            color: #C4B5FD !important;
        }
        div[data-testid="stButton"] button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {
            transform: translateY(-2px) !important;
            border-color: rgba(167, 139, 250, 0.7) !important;
            background: rgba(124, 58, 237, 0.18) !important;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.3),
                        0 8px 20px -8px rgba(0,0,0,0.4) !important;
            color: #DDD6FE !important;
        }
        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%) !important;
            border: none !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.4),
                        0 4px 12px rgba(0,0,0,0.3) !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover {
            background: linear-gradient(135deg, #6D28D9 0%, #0891B2 100%) !important;
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.55),
                        0 8px 20px -8px rgba(0,0,0,0.4) !important;
            transform: translateY(-2px) !important;
        }

        /* ═══════════════════════════════════════════════
           INPUTS, SELECTS, SLIDERS, TEXTAREAS
        ═══════════════════════════════════════════════ */
        .stTextInput > div > div,
        .stTextArea > div > div,
        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        .stNumberInput > div > div {
            background: #0D1117 !important;
            border: 1px solid rgba(124, 58, 237, 0.3) !important;
            border-radius: 12px !important;
            color: #E2E8F0 !important;
        }
        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within,
        .stSelectbox > div > div:focus-within {
            border-color: rgba(167, 139, 250, 0.7) !important;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
        }
        .stTextInput input,
        .stTextArea textarea {
            color: #E2E8F0 !important;
            background: transparent !important;
        }
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #334155 !important;
        }
        /* Selectbox dropdown — force dark on every layer */
        [data-baseweb="select"] * { color: #E2E8F0 !important; }
        [data-baseweb="select"] [data-baseweb="select-dropdown"],
        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [data-baseweb="menu"],
        [data-baseweb="menu"] ul,
        [data-baseweb="menu"] li,
        [role="listbox"],
        [role="option"] {
            background: #0D1117 !important;
            background-color: #0D1117 !important;
            color: #E2E8F0 !important;
            border-color: rgba(124, 58, 237, 0.3) !important;
        }
        [data-baseweb="popover"] {
            border: 1px solid rgba(124, 58, 237, 0.35) !important;
            border-radius: 14px !important;
            box-shadow: 0 0 30px rgba(124, 58, 237, 0.2),
                        0 20px 40px -10px rgba(0,0,0,0.7) !important;
        }
        [role="option"]:hover,
        [data-baseweb="menu"] li:hover {
            background: rgba(124, 58, 237, 0.18) !important;
            color: #C4B5FD !important;
        }
        [aria-selected="true"][role="option"] {
            background: rgba(124, 58, 237, 0.25) !important;
            color: #A78BFA !important;
        }
        /* Multiselect tags */
        [data-baseweb="tag"] {
            background: rgba(124, 58, 237, 0.25) !important;
            color: #C4B5FD !important;
            border: 1px solid rgba(167, 139, 250, 0.4) !important;
            border-radius: 8px !important;
        }

        /* Sliders */
        [data-testid="stSlider"] > div > div > div {
            background: rgba(124, 58, 237, 0.25) !important;
        }
        [data-testid="stSlider"] [role="slider"] {
            background: linear-gradient(135deg, #7C3AED, #06B6D4) !important;
            box-shadow: 0 0 12px rgba(124, 58, 237, 0.5) !important;
        }

        /* Radio buttons */
        .stRadio label {
            color: #CBD5E1 !important;
        }

        /* Labels */
        label[data-testid="stWidgetLabel"] p,
        .stSelectbox label p,
        .stTextInput label p,
        .stSlider label p,
        .stRadio label p {
            color: #94A3B8 !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
        }

        /* ═══════════════════════════════════════════════
           PAGE LINKS (sidebar navigation)
        ═══════════════════════════════════════════════ */
        [data-testid="stPageLink"] {
            border-radius: 12px !important;
            border: 1px solid rgba(124, 58, 237, 0.25) !important;
            background: rgba(124, 58, 237, 0.06) !important;
            transition: all 0.15s ease !important;
            color: #C4B5FD !important;
        }
        [data-testid="stPageLink"]:hover {
            background: rgba(124, 58, 237, 0.16) !important;
            border-color: rgba(167, 139, 250, 0.55) !important;
            transform: translateY(-1px) !important;
        }
        [data-testid="stPageLink"] p {
            color: #A78BFA !important;
            font-weight: 600 !important;
        }

        /* ═══════════════════════════════════════════════
           BORDERED CONTAINERS
        ═══════════════════════════════════════════════ */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background: rgba(13, 17, 23, 0.8) !important;
            border: 1px solid rgba(124, 58, 237, 0.25) !important;
            border-radius: 18px !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03) !important;
        }

        /* ═══════════════════════════════════════════════
           EXPANDERS
        ═══════════════════════════════════════════════ */
        [data-testid="stExpander"] {
            background: rgba(13, 17, 23, 0.6) !important;
            border: 1px solid rgba(124, 58, 237, 0.2) !important;
            border-radius: 14px !important;
        }
        [data-testid="stExpander"] summary {
            color: #A78BFA !important;
            font-weight: 600 !important;
        }

        /* ═══════════════════════════════════════════════
           ALERTS (info, success, warning, error)
        ═══════════════════════════════════════════════ */
        div[data-testid="stAlert"] {
            border-radius: 14px !important;
            border-left-width: 3px !important;
        }
        div[data-testid="stAlert"][kind="info"] {
            background: rgba(6, 182, 212, 0.08) !important;
            border-color: #06B6D4 !important;
            color: #67E8F9 !important;
        }
        div[data-testid="stAlert"][kind="success"] {
            background: rgba(16, 185, 129, 0.08) !important;
            border-color: #10B981 !important;
            color: #6EE7B7 !important;
        }
        div[data-testid="stAlert"][kind="warning"] {
            background: rgba(245, 158, 11, 0.08) !important;
            border-color: #F59E0B !important;
            color: #FCD34D !important;
        }
        div[data-testid="stAlert"][kind="error"] {
            background: rgba(239, 68, 68, 0.08) !important;
            border-color: #EF4444 !important;
            color: #FCA5A5 !important;
        }

        /* ═══════════════════════════════════════════════
           PROGRESS BAR
        ═══════════════════════════════════════════════ */
        div[data-testid="stProgress"] > div {
            background: rgba(124, 58, 237, 0.15) !important;
            border-radius: 999px !important;
        }
        div[data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, #7C3AED 0%, #06B6D4 100%) !important;
            border-radius: 999px !important;
            box-shadow: 0 0 10px rgba(124, 58, 237, 0.5) !important;
        }
        div[data-testid="stProgress"] p {
            color: #94A3B8 !important;
            font-size: 0.82rem !important;
        }

        /* ═══════════════════════════════════════════════
           DATAFRAME / TABLE
        ═══════════════════════════════════════════════ */
        [data-testid="stDataFrame"] {
            border-radius: 16px !important;
            overflow: hidden !important;
            border: 1px solid rgba(124, 58, 237, 0.25) !important;
        }
        [data-testid="stDataFrame"] * {
            background: #0D1117 !important;
            color: #CBD5E1 !important;
        }

        /* ═══════════════════════════════════════════════
           DIVIDER
        ═══════════════════════════════════════════════ */
        hr {
            border-color: rgba(124, 58, 237, 0.18) !important;
            margin: 1.5rem 0 !important;
        }

        /* ═══════════════════════════════════════════════
           HEADINGS inside page content
        ═══════════════════════════════════════════════ */
        .stMarkdown h2 {
            color: #E2E8F0 !important;
            border-bottom: 1px solid rgba(124, 58, 237, 0.2);
            padding-bottom: 0.4rem;
            margin-top: 1.5rem;
        }
        .stMarkdown h3 {
            color: #C4B5FD !important;
        }
        .stMarkdown h4 {
            color: #A78BFA !important;
        }
        .stMarkdown p, .stMarkdown li {
            color: #CBD5E1 !important;
            line-height: 1.7;
        }
        .stMarkdown strong {
            color: #E2E8F0 !important;
        }
        .stMarkdown blockquote {
            border-left: 3px solid #7C3AED !important;
            background: rgba(124, 58, 237, 0.06) !important;
            border-radius: 0 10px 10px 0 !important;
            padding: 0.6rem 1rem !important;
            margin: 0.5rem 0 !important;
        }
        .stMarkdown blockquote p {
            color: #CBD5E1 !important;
            margin: 0 !important;
        }

        /* ═══════════════════════════════════════════════
           CHAT MESSAGES
        ═══════════════════════════════════════════════ */
        [data-testid="stChatMessage"] {
            background: rgba(13, 17, 23, 0.8) !important;
            border: 1px solid rgba(124, 58, 237, 0.2) !important;
            border-radius: 16px !important;
        }
        /* Chat input sticky bar — target every layer */
        .stChatFloatingInputContainer,
        [data-testid="stChatInputContainer"],
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottom"] > div > div,
        section[data-testid="stBottom"],
        .stChatInput,
        div.stChatInput {
            background: #080B14 !important;
            background-color: #080B14 !important;
        }
        [data-testid="stBottom"] {
            border-top: 1px solid rgba(124, 58, 237, 0.2) !important;
        }
        [data-testid="stChatInputContainer"] > div {
            background: #0D1117 !important;
            border: 1px solid rgba(124, 58, 237, 0.35) !important;
            border-radius: 16px !important;
        }
        /* Target the inner chat input wrapper and baseweb textarea by structure */
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] [data-baseweb="textarea"],
        [data-testid="stChatInput"] [data-baseweb="base-input"],
        [data-testid="stChatInput"] [data-baseweb="textarea"] > div {
            background: #0D1117 !important;
            background-color: #0D1117 !important;
            border-color: rgba(124, 58, 237, 0.35) !important;
        }
        [data-testid="stChatInput"],
        [data-testid="stChatInput"] textarea {
            background: #0D1117 !important;
            color: #E2E8F0 !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #475569 !important;
        }

        /* ═══════════════════════════════════════════════
           CAPTIONS and SMALL TEXT
        ═══════════════════════════════════════════════ */
        .stMarkdown small, caption, [data-testid="stCaptionContainer"] p {
            color: #475569 !important;
        }

        /* ═══════════════════════════════════════════════
           TABS (if used)
        ═══════════════════════════════════════════════ */
        [data-testid="stTabs"] {
            border-bottom: 1px solid rgba(124, 58, 237, 0.2) !important;
        }
        button[role="tab"] {
            color: #64748B !important;
            font-weight: 600 !important;
        }
        button[role="tab"][aria-selected="true"] {
            color: #A78BFA !important;
            border-bottom: 2px solid #7C3AED !important;
        }

        /* ═══════════════════════════════════════════════
           SPINNER
        ═══════════════════════════════════════════════ */
        [data-testid="stSpinner"] > div {
            border-top-color: #7C3AED !important;
        }

        /* ═══════════════════════════════════════════════
           FILE UPLOADER
        ═══════════════════════════════════════════════ */
        [data-testid="stFileUploader"] {
            background: rgba(13, 17, 23, 0.6) !important;
            border: 2px dashed rgba(124, 58, 237, 0.35) !important;
            border-radius: 16px !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: rgba(167, 139, 250, 0.6) !important;
            background: rgba(124, 58, 237, 0.06) !important;
        }
        [data-testid="stFileUploader"] * { color: #94A3B8 !important; }
        [data-testid="stFileUploaderDropzone"] { background: transparent !important; }
        [data-testid="stFileUploaderDropzone"] small { color: #475569 !important; }

        /* ═══════════════════════════════════════════════
           CHECKBOX
        ═══════════════════════════════════════════════ */
        .stCheckbox label span { color: #CBD5E1 !important; }

        /* ═══════════════════════════════════════════════
           SELECT SLIDER (easy/medium/hard)
        ═══════════════════════════════════════════════ */
        [data-testid="stSlider"] div[data-baseweb="slider"] div {
            background: rgba(124, 58, 237, 0.2) !important;
        }

        /* ═══════════════════════════════════════════════
           SUBHEADER styling
        ═══════════════════════════════════════════════ */
        [data-testid="stHeadingWithActionElements"] h2,
        [data-testid="stHeadingWithActionElements"] h3 {
            color: #E2E8F0 !important;
        }

        /* ═══════════════════════════════════════════════
           GLOW UTILITY (applied to key section headings)
        ═══════════════════════════════════════════════ */
        .glow-text {
            background: linear-gradient(90deg, #A78BFA, #67E8F9);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent !important;
        }
        </style>
        """),
        unsafe_allow_html=True,
    )


def render_hero(title, subtitle, badge=None):
    """Large gradient hero banner — home page and login screen."""
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
    """Compact gradient-text page header used on each tool page."""
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
    """Hide the auto-generated multipage nav list before login."""
    st.markdown(
        "<style>[data-testid='stSidebarNav'] { display: none; }</style>",
        unsafe_allow_html=True,
    )
