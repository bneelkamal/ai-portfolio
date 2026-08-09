from __future__ import annotations

from pathlib import Path
import runpy

import streamlit as st


st.set_page_config(
    page_title="Agentic AI Data Analyst",
    page_icon="📊",
    layout="wide",
)

project_path = (
    Path(__file__).resolve().parents[1]
    / "projects"
    / "ai-data-analyst"
    / "app.py"
)

runpy.run_path(str(project_path), run_name="__main__")
