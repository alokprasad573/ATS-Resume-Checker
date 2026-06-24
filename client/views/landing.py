import streamlit as st


def render():
    st.markdown("""
    <div class="console-hero">
        <div class="eyebrow">Resume intelligence workspace</div>
        <h1>Stackscore</h1>
        <p>Review your resume like a recruiter and improve it like a coach is sitting beside you. Upload a resume, compare it with a job description, and leave with a prioritized fix list.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start resume review", use_container_width=True, type="primary"):
            st.session_state.current_view = 'scorer'
            st.rerun()

    st.markdown("## What you get")
    st.markdown("""
    <div class="console-grid">
        <div class="feature-panel">
            <div class="panel-kicker">Recruiter lens</div>
            <h3 class="panel-title">Five-part ATS score</h3>
            <p style="color:var(--text-secondary); margin-bottom:0;">Formatting, keywords, content quality, skill evidence, and ATS compatibility are scored separately so weak areas are easy to spot.</p>
        </div>
        <div class="feature-panel">
            <div class="panel-kicker">Candidate coach</div>
            <h3 class="panel-title">Prioritized fixes</h3>
            <p style="color:var(--text-secondary); margin-bottom:0;">Issues are grouped by urgency with concrete action items, not vague advice that leaves you guessing what to edit first.</p>
        </div>
        <div class="feature-panel">
            <div class="panel-kicker">Targeted match</div>
            <h3 class="panel-title">JD comparison</h3>
            <p style="color:var(--text-secondary); margin-bottom:0;">Paste a job description to compare semantic fit, matched keywords, missing terms, and skill gaps for that exact role.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Workflow")
    st.markdown("""
    <div class="console-grid">
        <div class="workflow-panel">
            <div class="panel-number">1</div>
            <h3 class="panel-title">Upload</h3>
            <p style="color:var(--text-secondary); margin-bottom:0;">Start with a resume PDF, DOC, or DOCX.</p>
        </div>
        <div class="workflow-panel">
            <div class="panel-number">2</div>
            <h3 class="panel-title">Compare</h3>
            <p style="color:var(--text-secondary); margin-bottom:0;">Use general ATS scoring or add a job description for a role-specific review.</p>
        </div>
        <div class="workflow-panel">
            <div class="panel-number">3</div>
            <h3 class="panel-title">Improve</h3>
            <p style="color:var(--text-secondary); margin-bottom:0;">Work through the fix list, export the report, and track progress in history.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
