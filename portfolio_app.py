from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Neelkamal Badana | AI Product Manager", page_icon="◈", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.block-container {max-width: 1180px; padding-top: 2.5rem; padding-bottom: 3rem;}
.hero {background: linear-gradient(135deg, #eff6ff, #f8fafc); border: 1px solid #dbeafe; border-radius: 20px; padding: 2.4rem; margin-bottom: 1.5rem;}
.eyebrow {color: #2563eb; font-size: .82rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;}
.hero h1 {font-size: 3rem; line-height: 1.1; color: #0f172a; margin: .35rem 0 .7rem;}
.hero p {font-size: 1.15rem; color: #475569; max-width: 760px;}
.card {background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.2rem; min-height: 180px; box-shadow: 0 4px 16px rgba(15,23,42,.04);}
.card h3 {color: #0f172a; margin-top: 0; font-size: 1.12rem;}
.card p {color: #475569; line-height: 1.55;}
.tag {display: inline-block; background: #eff6ff; color: #1d4ed8; border-radius: 999px; padding: .25rem .55rem; margin: .15rem; font-size: .8rem;}
.section-note {color: #64748b; margin-top: -.45rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">AI Portfolio · Product Management · Responsible Innovation</div>
  <h1>Neelkamal Badana</h1>
  <p><strong>Product Manager with 14 years of experience</strong> building business outcomes through technology, now combining product leadership with advanced AI research.</p>
  <p>I design practical, explainable, and responsible AI systems for decision support, analytics, risk, and organizational intelligence.</p>
</div>
""", unsafe_allow_html=True)

links = st.columns(4)
links[0].link_button("GitHub", "https://github.com/bneelkamal", use_container_width=True)
links[1].link_button("AI Portfolio", "https://github.com/bneelkamal/ai-portfolio", use_container_width=True)
links[2].link_button("LinkedIn", "https://www.linkedin.com/in/bneelkamal/", use_container_width=True)
links[3].link_button("Contact", "mailto:bneelkamal@outlook.com", use_container_width=True)

st.header("About")
st.markdown("I am a Product Manager with 14 years of experience and a Master's student in Artificial Intelligence, aspiring to pursue doctoral research at the intersection of AI and business management. My work connects product strategy, stakeholder communication, business-value analysis, AI system design, and responsible deployment.")

st.header("Research interests")
st.markdown('<div>' + ''.join(f'<span class="tag">{tag}</span>' for tag in ["Federated Learning", "Vertical FL", "Neuro-symbolic AI", "Agentic AI", "Multi-agent Systems", "Explainable AI", "AI Governance", "Cloud AI/ML", "Fraud Detection", "Anomaly Detection", "MARL", "AI for Business"]) + '</div>', unsafe_allow_html=True)

st.header("Experience and strengths")
st.markdown('<p class="section-note">A product-led approach to building and evaluating intelligent systems.</p>', unsafe_allow_html=True)
strengths = st.columns(3)
for column, title, text in zip(strengths, ["Product leadership", "AI systems thinking", "Responsible delivery"], ["Problem discovery, roadmap definition, stakeholder alignment, prioritization, and value realization.", "Translating research concepts into architectures, prototypes, workflows, and measurable experiments.", "Explainability, governance, security, evaluation, human oversight, and practical adoption constraints."]):
    column.markdown(f'<div class="card"><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

st.header("Featured AI portfolio projects")
st.markdown('<p class="section-note">Focused projects showing how AI capabilities become useful, testable products.</p>', unsafe_allow_html=True)
projects = [
    ("Agentic AI Data Analyst", "Upload CSV/XLSX files or paste public URLs. A LangGraph workflow profiles the source, recommends reports, and presents charts and evidence-grounded insights.", "In development", "https://github.com/bneelkamal/ai-portfolio/tree/main/projects/ai-data-analyst", None),
    ("RAG Document Intelligence Assistant", "An enterprise-style assistant for grounded document search, citations, and knowledge workflows.", "Planned", None, None),
    ("Explainable Fraud Detection", "Risk analytics with imbalance handling, anomaly detection, threshold decisions, and interpretable explanations.", "Planned", None, None),
    ("Agentic Business Research Assistant", "A multi-agent workflow for research planning, evidence collection, synthesis, and review.", "Planned", None, None),
    ("Responsible AI Evaluation Toolkit", "Practical checks for reliability, traceability, explainability, selected fairness risks, and governance readiness.", "Planned", None, None),
    ("Federated Learning Research", "Privacy-preserving collaborative learning and fraud-risk research maintained in a separate research repository.", "Research repository", None, None),
]
for start in range(0, len(projects), 3):
    row = st.columns(3)
    for column, project in zip(row, projects[start:start + 3]):
        title, description, status, source, demo = project
        card = f'<div class="card"><h3>{title}</h3><p>{description}</p><span class="tag">{status}</span></div>'
        column.markdown(card, unsafe_allow_html=True)
        button_cols = column.columns(2)
        if source:
            button_cols[0].link_button("Source", source, use_container_width=True)
        else:
            button_cols[0].markdown("<small>Source coming soon</small>", unsafe_allow_html=True)
        if demo:
            button_cols[1].link_button("Live demo", demo, use_container_width=True)
        else:
            button_cols[1].markdown("<small>Demo coming soon</small>", unsafe_allow_html=True)

st.header("How I approach AI products")
steps = st.columns(4)
for column, number, title, text in zip(steps, ["01", "02", "03", "04"], ["Frame", "Design", "Evaluate", "Adopt"], ["Define the user problem, business value, and constraints.", "Choose the data, architecture, model, tools, and human-oversight boundaries.", "Measure technical quality, usefulness, trust, safety, and limitations.", "Plan rollout, governance, stakeholder enablement, and continuous improvement."]):
    column.markdown(f'<div class="card"><div class="eyebrow">{number}</div><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

st.header("Connect")
st.markdown("For product leadership, AI research, collaboration, or responsible AI opportunities, connect with me through GitHub or LinkedIn.")
st.caption("© Neelkamal Badana · AI Product Management and Research Portfolio")
