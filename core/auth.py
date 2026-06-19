"""Simple household login + per-student profile selection."""
import os


def _get_password() -> str:
    try:
        import streamlit as st
        v = st.secrets.get("APP_PASSWORD")
        if v:
            return v
    except Exception:
        pass
    return os.environ.get("APP_PASSWORD", "euroschool7")


APP_PASSWORD = _get_password()

GRADES = list(range(1, 11))  # Grade 1 to Grade 10
