from __future__ import annotations

import sys
from pathlib import Path
import runpy

import streamlit as st


st.set_page_config(
    page_title="Agentic AI Data Analyst",
    page_icon="📊",
    layout="wide",
)

project_dir = (
    Path(__file__).resolve().parents[1]
    / "projects"
    / "ai-data-analyst"
)

project_path = project_dir / "app.py"

# Allow app.py to import neighboring project modules such as agent_graph.py
sys.path.insert(0, str(project_dir))

runpy.run_path(str(project_path), run_name="__main__")
