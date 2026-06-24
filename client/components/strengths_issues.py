from typing import Any, Dict, List
import streamlit as st


def display_strengths(strengths: List[str]) -> None:
    st.markdown("### Strengths")
    if not strengths:
        st.info("Keep improving your resume to unlock strengths!")
        return
    
    html_items = "".join(
        f'<div style="display:flex; align-items:flex-start; margin-bottom:0.75rem; gap:0.5rem;">'
        f'<span class="status-chip success">Good</span>'
        f'<span style="color:var(--text-primary); font-size:0.95rem;">{item}</span>'
        f'</div>'
        for item in strengths
    )
    st.markdown(
        f"""
        <div class="app-card" style="border-left: 4px solid var(--success-color); background: var(--success-bg);">
            {html_items}
        </div>
        """,
        unsafe_allow_html=True
    )


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary = analysis.get("issues_summary") or []

    if not critical and not summary:
        st.markdown(
            """
            <div class="app-card" style="border-left: 4px solid var(--success-color); background: var(--success-bg); text-align: center; padding: 2rem;">
                <span class="status-chip success">Clear</span>
                <h4 style="margin:0.75rem 0 0 0; color:var(--success-color);">No critical issues found</h4>
                <p style="color:var(--text-secondary); font-size: 0.95rem; margin-top: 0.5rem; margin-bottom:0;">Your resume doesn't have any urgent ATS compatibility issues. Excellent job!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    st.markdown("### Critical issues")
    
    html_items = "".join(
        f'<div style="display:flex; align-items:flex-start; margin-bottom:0.75rem; gap:0.5rem;">'
        f'<span class="status-chip danger">Fix first</span>'
        f'<span style="color:var(--text-primary); font-size:0.95rem;">{item}</span>'
        f'</div>'
        for item in critical
    )
    st.markdown(
        f"""
        <div class="app-card" style="border-left: 4px solid var(--danger-color); background: var(--danger-bg); margin-bottom: 1rem;">
            <div class="panel-kicker" style="color: var(--danger-light); margin-bottom: 0.75rem;">Address these first</div>
            {html_items}
        </div>
        """,
        unsafe_allow_html=True
    )

    extra = [s for s in summary if s not in critical]
    if extra:
        with st.expander("Additional flagged items", expanded=False):
            for item in extra:
                st.markdown(f"- {item}")
