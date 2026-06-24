import requests
import streamlit as st

from client.services import api_client


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"Backend returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"Unexpected error: {exc}")


def render() -> None:
    st.markdown(
        """
        <div class="console-hero">
            <div class="eyebrow">Progress archive</div>
            <h1>Analysis history</h1>
            <p>Review saved analyses, compare past scores, and spot whether your resume edits are moving in the right direction.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("Sign in from the sidebar to view your history.")
        return

    try:
        history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    if not history:
        st.info("No analyses yet for this account. Run a scoring on the ATS Scorer page first.")
        if st.button("Go to ATS Scorer"):
            st.session_state.current_view = "scorer"
            st.rerun()
        return

    st.markdown(f'<span class="status-chip coach">Total analyses: {len(history)}</span>', unsafe_allow_html=True)
    st.markdown("---")

    for idx, entry in enumerate(history):
        filename = entry.get("filename", "resume")
        ats_score = float(entry.get("ats_score", 0))
        created_at = entry.get("created_at", "")
        analysis = entry.get("analysis_result", {}) or {}

        component_scores = analysis.get("component_scores", {}) or {}
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")

        with st.expander(f"{filename} | Score: {ats_score:.0f}/100 | {created_at}"):
            st.markdown(
                f"""
                <div class="history-panel" style="margin-bottom:1rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap;">
                        <div>
                            <div class="panel-kicker">Saved review</div>
                            <h4 style="margin:0.15rem 0 0 0; color:var(--text-primary);">{filename}</h4>
                        </div>
                        <span class="score-chip">Score: {ats_score:.0f}/100</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(
                    f"""
                    <div class="history-panel" style="margin-bottom:0.5rem; padding: 1rem; height: 100%;">
                        <strong class="panel-kicker">Score breakdown</strong>
                        <div style="margin-top:0.5rem; display:flex; flex-direction:column; gap:0.5rem;">
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                                <span>Formatting</span>
                                <span style="font-weight:700; color:var(--primary-light);">{component_scores.get('formatting', 0):.0f}/20</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                                <span>Keywords & Skills</span>
                                <span style="font-weight:700; color:var(--primary-light);">{component_scores.get('keywords', 0):.0f}/25</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                                <span>Content Quality</span>
                                <span style="font-weight:700; color:var(--primary-light);">{component_scores.get('content', 0):.0f}/25</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c2:
                st.markdown(
                    f"""
                    <div class="history-panel" style="margin-bottom:0.5rem; padding: 1rem; height: 100%;">
                        <strong class="panel-kicker">ATS metrics</strong>
                        <div style="margin-top:0.5rem; display:flex; flex-direction:column; gap:0.5rem;">
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                                <span>Skill Validation</span>
                                <span style="font-weight:700; color:var(--primary-light);">{component_scores.get('skill_validation', 0):.0f}/15</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                                <span>ATS Compatibility</span>
                                <span style="font-weight:700; color:var(--primary-light);">{component_scores.get('ats_compatibility', 0):.0f}/15</span>
                            </div>
                            <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                                <span>JD Match</span>
                                <span style="font-weight:700; color:var(--primary-light);">{f"{jd_comparison.get('match_percentage', 0):.0f}%" if jd_comparison else "N/A"}</span>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
            entry_id = entry.get("id")
            if entry_id:
                if st.button("Delete analysis", key=f"delete_{idx}"):
                    try:
                        api_client.delete_history_entry(str(entry_id), access_token)
                        st.success("Deleted successfully.")
                        st.rerun()
                    except requests.RequestException as exc:
                        _show_backend_error(exc)
