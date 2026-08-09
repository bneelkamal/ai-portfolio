from __future__ import annotations

import runpy
import sys
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="AI Data Analyst | Neelkamal Badana", page_icon="📊", layout="wide")
st.page_link("portfolio_app.py", label="Back to AI Portfolio", icon="🏠")
st.title("Agentic AI Data Analyst")
st.caption("Portfolio project: automated analysis of files and public data sources.")

project_dir = Path(__file__).resolve().parents[1] / "projects" / "ai-data-analyst"
project_path = project_dir / "app.py"
if str(project_dir) not in sys.path:
    sys.path.insert(0, str(project_dir))

# The project app contains the complete interactive analysis experience.
# It is executed here as an internal portfolio page so the public deployment
# remains a single Streamlit application.
original_set_page_config = st.set_page_config
st.set_page_config = lambda **kwargs: None
try:
    runpy.run_path(str(project_path), run_name="__main__")
finally:
    st.set_page_config = original_set_page_config
