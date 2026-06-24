from typing import Any, Dict, Optional

import streamlit as st


def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return  # caller decides whether to render the section at all

    st.markdown("### Job description match")

    match_pct = float(jd_comparison.get("match_percentage", 0))
    semantic = float(jd_comparison.get("semantic_similarity", 0))
    matched = jd_comparison.get("matched_keywords", []) or []
    missing = jd_comparison.get("missing_keywords", []) or []
    gap = jd_comparison.get("skills_gap", []) or []

    top_l, top_r = st.columns(2)
    with top_l:
        st.markdown(
            f"""
            <div class="app-card">
                <div class="metric-row">
                    <span>Match percentage</span>
                    <strong style="color:var(--primary-light);">{match_pct:.0f}%</strong>
                </div>
                <div class="progress-container" style="margin:0.5rem 0 1rem 0;">
                    <div class="progress-bar progress-bar-primary" style="width:{min(max(match_pct, 0), 100)}%;"></div>
                </div>
                <div class="metric-row">
                    <span>Semantic similarity</span>
                    <strong style="color:var(--coach-light);">{semantic * 100:.0f}%</strong>
                </div>
                <div class="progress-container" style="margin-top:0.5rem;">
                    <div class="progress-bar progress-bar-info" style="width:{min(max(semantic * 100, 0), 100)}%;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_r:
        st.markdown("**Matched keywords**")
        if matched:
            st.markdown(" ".join(f'<span class="skill-tag skill-tag-validated">{kw}</span>' for kw in matched[:15]), unsafe_allow_html=True)
        else:
            st.markdown("_None matched yet_")

    st.markdown("---")
    bot_l, bot_r = st.columns(2)
    with bot_l:
        st.markdown("**Missing keywords**")
        if missing:
            st.markdown(" ".join(f'<span class="skill-tag skill-tag-unvalidated">{kw}</span>' for kw in missing[:10]), unsafe_allow_html=True)
        else:
            st.markdown("_All key terms are present!_")
    with bot_r:
        st.markdown("**Skills gap**")
        if gap:
            st.markdown(" ".join(f'<span class="skill-tag">{skill}</span>' for skill in gap[:10]), unsafe_allow_html=True)
        else:
            st.markdown("_No significant skills gap detected_")
