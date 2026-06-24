from typing import Optional

import requests
import streamlit as st

from client.services import api_client
from client.components.dashboard import display_results_dashboard


def _read_jd(jd_file, jd_text: str) -> str:
    """
    Turn whatever the user provided into a plain JD string for the backend.

    For .txt files we decode in-process — that's a trivial operation, no need
    for a backend round-trip. For PDF/DOCX, we'd need the backend's parser;
    we don't have a public endpoint for that, so we ask the user to paste text
    instead for non-txt JDs.
    """
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore")
    st.warning(
        "Job description files must be `.txt` for now — paste the JD text instead "
        "if you have a PDF or DOCX."
    )
    return ""


def _show_backend_error(exc: Exception) -> None:
    """Translate a `requests` exception into a friendly Streamlit error."""
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is `uvicorn backend.main:app` running on port 8000?")
    elif isinstance(exc, requests.Timeout):
        st.error("The backend took too long to respond. Try a smaller resume or check the server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"Backend returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")


def _summary_text(analysis: dict) -> str:
    """Tiny client-side text summary for the Download button."""
    score = analysis.get("ATS_score", analysis.get("ats_score", 0))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.append("STRENGTHS:")
        lines.extend(f"  - {s}" for s in analysis["strengths"])
        lines.append("")
    if analysis.get("critical_issues"):
        lines.append("CRITICAL ISSUES:")
        lines.extend(f"  - {s}" for s in analysis["critical_issues"])
        lines.append("")
    if analysis.get("suggestions"):
        lines.append("SUGGESTIONS:")
        lines.extend(f"  - {s}" for s in analysis["suggestions"])
    return "\n".join(lines)


def _render_upload_area(analysis_mode: str):
    """Two-column upload widgets. Returns (resume_file, jd_file, jd_text)."""
    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="upload-panel" style="margin-bottom:0.75rem; min-height: 164px;">
                <div class="panel-kicker">Required input</div>
                <h3 class="panel-title">Resume file</h3>
                <p style="color:var(--text-secondary); font-size:0.92rem; margin-bottom: 0;">Upload the resume you want scored for formatting, keywords, content quality, skill evidence, and parser compatibility.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        resume_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "doc", "docx"],
            help="Supported: PDF, DOC, DOCX (max 5 MB)",
            key="resume_upload",
            label_visibility="collapsed"
        )
        if resume_file:
            st.success(f"✅ {resume_file.name} ({resume_file.size / 1024:.1f} KB)")

    jd_file: Optional[object] = None
    jd_text = ""

    with right:
        if analysis_mode == "Job Description Comparison":
            st.markdown(
                """
                <div class="upload-panel" style="margin-bottom:0.75rem; min-height: 164px;">
                    <div class="panel-kicker">Optional targeting</div>
                    <h3 class="panel-title">Job description</h3>
                    <p style="color:var(--text-secondary); font-size:0.92rem; margin-bottom: 0;">Add the target role to measure keyword coverage, semantic fit, and skill gaps against a specific hiring screen.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            jd_method = st.radio(
                "Input method:",
                ["Paste Text", "Upload .txt File"],
                horizontal=True,
                key="jd_input_method",
                label_visibility="collapsed"
            )
            if jd_method == "Upload .txt File":
                jd_file = st.file_uploader(
                    "Choose JD file (.txt only)",
                    type=["txt"],
                    key="jd_upload",
                    label_visibility="collapsed"
                )
                if jd_file:
                    st.success(f"✅ {jd_file.name}")
            else:
                jd_text = st.text_area(
                    "Paste job description text:",
                    height=95,
                    placeholder="Paste the JD here...",
                    key="jd_text",
                    label_visibility="collapsed"
                )
                if jd_text:
                    st.success(f"✅ {len(jd_text)} characters")
        else:
            st.markdown(
                """
                <div class="upload-panel" style="height: 100%; min-height: 238px; display: flex; flex-direction: column; justify-content: center; margin-bottom: 0;">
                    <span class="status-chip coach" style="width: fit-content;">JD comparison available</span>
                    <h4 style="margin:0.9rem 0 0.4rem 0; color:var(--text-primary);">Target a specific role</h4>
                    <p style="color:var(--text-muted); font-size:0.9rem; max-width: 360px; margin-bottom: 0;">Switch to Job Description Comparison when you want role-specific missing keywords and fit analysis.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    return resume_file, jd_file, jd_text


def _render_export_buttons(analysis: dict) -> None:
    st.markdown("### 📥 Export Results")
    c1, c2 = st.columns(2)

    with c1:
        # Lazy: only call the backend the first time the user clicks expand.
        if st.button("📑 Generate PDF Report", use_container_width=True, type="primary"):
            try:
                with st.spinner("Generating PDF on backend..."):
                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state["access_token"],
                    )
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
            except requests.RequestException as exc:
                _show_backend_error(exc)

        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                "⬇️ Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="ats_resume_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )

    with c2:
        st.download_button(
            "📄 Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="ats_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )


def render() -> None:
    st.markdown(
        """
        <div class="console-hero">
            <div class="eyebrow">Analysis console</div>
            <h1>Resume review</h1>
            <p>Upload a resume, choose the review mode, and get a scored dashboard with the next edits ranked by urgency.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("---")
        st.markdown("## Analysis Options")
        st.info(
            "**General ATS Score**: resume only — overall compatibility.\n\n"
            "**JD Comparison**: resume + job description — targeted match analysis."
        )

    st.markdown("---")

    analysis_mode = st.radio(
        "Select analysis mode:",
        ["General ATS Score", "Job Description Comparison"],
        horizontal=True,
    )

    st.markdown("---")

    resume_file, jd_file, jd_text = _render_upload_area(analysis_mode)

    st.markdown("---")

    if not resume_file:
        st.info("Upload your resume to begin.")
        # If we have a prior result in session, render it again.
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
        return

    access_token = st.session_state.get("access_token")
    if not access_token:
        st.warning("Sign in from the sidebar to analyze a resume.")
        return

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        analyze = st.button("Analyze resume", use_container_width=True, type="primary")

    if not analyze:
        # Re-show previous result on rerun (e.g. after PDF generation).
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    # Fresh analysis — drop any cached PDF/result.
    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)

    job_description = _read_jd(jd_file, jd_text) if analysis_mode == "Job Description Comparison" else ""

    try:
        with st.spinner("Analyzing your resume... this can take 10–30 seconds."):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    st.session_state["scorer_analysis"] = analysis
    st.success("Analysis complete.")
    display_results_dashboard(analysis)
    _render_export_buttons(analysis)
