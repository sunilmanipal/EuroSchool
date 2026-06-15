"""Simple household login + per-student profile selection."""
import os

APP_PASSWORD = os.environ.get("APP_PASSWORD", "euroschool7")

GRADES = list(range(1, 11))  # Grade 1 to Grade 10
