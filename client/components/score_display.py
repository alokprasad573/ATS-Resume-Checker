from typing import Any, Dict

import streamlit as st

from client.components._helpers import get_score_color


# Component max scores match backend/core/config.py SCORE_WEIGHTS.
# (Backend returns each component's score on its own scale, not 0–100.)
COMPONENTS = [
    ("Formatting",        "formatting",        20),
    ("Keywords & Skills", "keywords",          25),
    ("Content Quality",   "content",           25),
    ("Skill Validation",  "skill_validation",  15),
    ("ATS Compatibility", "ats_compatibility", 15),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    """Big colored score card with a short interpretation line."""
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = analysis.get("interpretation", "")
    text_color, bg_color = get_score_color(score)
    band = "Strong" if score >= 80 else "Needs polish" if score >= 60 else "Needs focused edits"

    st.markdown("## Analysis results")
    st.markdown(
        f"""
        <div class="result-summary">
            <div class="app-card" style="text-align:center;">
                <div class="score-badge-circle" style="border-color: {text_color}; box-shadow: 0 0 28px {bg_color}; background: radial-gradient(circle, {bg_color} 0%, var(--surface-raised) 74%);">
                    <div class="score-badge-value" style="color: {text_color};">{score:.0f}</div>
                    <div class="score-badge-lbl">ATS score</div>
                </div>
                <span class="status-chip">{band}</span>
            </div>
            <div class="score-insight">
                <div class="panel-kicker">Recruiter read</div>
                <h3 style="margin:0.35rem 0 0.6rem 0; color:var(--text-primary);">What this score means</h3>
                <p style="color:var(--text-secondary); margin:0; line-height:1.55;">{interpretation or "Review the component scores below to find the highest-leverage edits."}</p>
                <div class="coach-note" style="margin-top:1rem;">
                    Start with critical issues, then improve weak component scores before tuning smaller wording details.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    """Five progress bars, one per scoring component."""
    component_scores = analysis.get("component_scores") or {}
    st.markdown("### Score breakdown")

    left, right = st.columns(2)
    
    # Wrap elements in premium glass container layout
    with left:
        st.markdown('<div class="app-card" style="height: 100%; margin-bottom: 0;">', unsafe_allow_html=True)
        for i, (label, key, max_score) in enumerate(COMPONENTS):
            if i % 2 != 0:
                continue
            value = float(component_scores.get(key, 0))
            percentage = min(max(value / max_score if max_score else 0, 0), 1)
            
            if percentage >= 0.8:
                bar_class = "progress-bar-success"
                val_color = "var(--success-color)"
            elif percentage >= 0.6:
                bar_class = "progress-bar-warning"
                val_color = "var(--warning-color)"
            else:
                bar_class = "progress-bar-danger"
                val_color = "var(--danger-color)"

            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 2px;">
                    <span style="font-weight: 600; color:var(--text-primary);">{label}</span>
                    <span style="font-weight: 700; color:{val_color}; font-size:0.95rem;">{value:.0f}/{max_score}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar {bar_class}" style="width:{percentage * 100}%;"></div>
                </div>
                <div style="margin-bottom: 1.25rem;"></div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="app-card" style="height: 100%; margin-bottom: 0;">', unsafe_allow_html=True)
        for i, (label, key, max_score) in enumerate(COMPONENTS):
            if i % 2 == 0:
                continue
            value = float(component_scores.get(key, 0))
            percentage = min(max(value / max_score if max_score else 0, 0), 1)
            
            if percentage >= 0.8:
                bar_class = "progress-bar-success"
                val_color = "var(--success-color)"
            elif percentage >= 0.6:
                bar_class = "progress-bar-warning"
                val_color = "var(--warning-color)"
            else:
                bar_class = "progress-bar-danger"
                val_color = "var(--danger-color)"

            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 2px;">
                    <span style="font-weight: 600; color:var(--text-primary);">{label}</span>
                    <span style="font-weight: 700; color:{val_color}; font-size:0.95rem;">{value:.0f}/{max_score}</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar {bar_class}" style="width:{percentage * 100}%;"></div>
                </div>
                <div style="margin-bottom: 1.25rem;"></div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)
