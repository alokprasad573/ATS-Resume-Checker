import streamlit as st


def render():
    """Render the resources page"""
    st.markdown(
        """
        <div class="console-hero">
            <div class="eyebrow">Candidate coach</div>
            <h1>Resume resources</h1>
            <p>Use these checklists when editing between analysis runs. They focus on changes that make resumes easier for ATS systems and recruiters to parse.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## ATS optimization checklist")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="resource-panel" style="border-left: 4px solid var(--success-color); background: var(--success-bg); height: 100%;">
            <h3 style="margin-top:0; color:var(--success-color);">Do</h3>
            <div style="display:flex; flex-direction:column; gap:0.6rem; color:var(--text-primary); font-size:0.95rem;">
                <div>Use standard section headings</div>
                <div>Include relevant keywords from the job description</div>
                <div>Use simple, clean formatting</div>
                <div>List skills explicitly</div>
                <div>Quantify achievements with numbers</div>
                <div>Use standard fonts such as Arial, Calibri, or Times New Roman</div>
                <div>Save as PDF or DOCX</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="resource-panel" style="border-left: 4px solid var(--danger-color); background: var(--danger-bg); height: 100%;">
            <h3 style="margin-top:0; color:var(--danger-color);">Avoid</h3>
            <div style="display:flex; flex-direction:column; gap:0.6rem; color:var(--text-primary); font-size:0.95rem;">
                <div>Tables and text boxes for important content</div>
                <div>Headers or footers for contact details</div>
                <div>Images, icons, and decorative graphics</div>
                <div>Unusual fonts</div>
                <div>Multi-column layouts when a single column works</div>
                <div>Keyword stuffing</div>
                <div>Abbreviations without spelling them out first</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Common ATS Keywords
    st.markdown("## Common ATS keywords by industry")
    
    tab1, tab2, tab3 = st.tabs(["Tech", "Business", "Creative"])
    
    with tab1:
        st.markdown(
            """
            <div style="margin-top: 1rem;">
                <h4 style="color:var(--primary-light);">Software Development</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">Python</span>
                    <span class="skill-tag">Java</span>
                    <span class="skill-tag">JavaScript</span>
                    <span class="skill-tag">TypeScript</span>
                    <span class="skill-tag">C++</span>
                </div>
                <h4 style="color:var(--primary-light);">Frameworks & Libraries</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">React</span>
                    <span class="skill-tag">Django</span>
                    <span class="skill-tag">Spring Boot</span>
                    <span class="skill-tag">Angular</span>
                    <span class="skill-tag">Next.js</span>
                </div>
                <h4 style="color:var(--primary-light);">DevOps & Tools</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">Git</span>
                    <span class="skill-tag">Docker</span>
                    <span class="skill-tag">Kubernetes</span>
                    <span class="skill-tag">AWS</span>
                    <span class="skill-tag">CI/CD</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with tab2:
        st.markdown(
            """
            <div style="margin-top: 1rem;">
                <h4 style="color:var(--primary-light);">Core Competencies</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">Project Management</span>
                    <span class="skill-tag">Stakeholder Engagement</span>
                    <span class="skill-tag">Budget Administration</span>
                    <span class="skill-tag">Strategic Planning</span>
                    <span class="skill-tag">Agile / Scrum</span>
                </div>
                <h4 style="color:var(--primary-light);">Leadership & Execution</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">Team Leadership</span>
                    <span class="skill-tag">Process Optimization</span>
                    <span class="skill-tag">Business Analysis</span>
                    <span class="skill-tag">Risk Assessment</span>
                    <span class="skill-tag">Resource Allocation</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with tab3:
        st.markdown(
            """
            <div style="margin-top: 1rem;">
                <h4 style="color:var(--primary-light);">Design Systems & Tools</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">Adobe Creative Suite</span>
                    <span class="skill-tag">Figma</span>
                    <span class="skill-tag">Sketch</span>
                    <span class="skill-tag">Canva</span>
                </div>
                <h4 style="color:var(--primary-light);">Design Practices</h4>
                <div style="margin-bottom:1.5rem;">
                    <span class="skill-tag">UI/UX Design</span>
                    <span class="skill-tag">Wireframing</span>
                    <span class="skill-tag">Prototyping</span>
                    <span class="skill-tag">Brand Identity</span>
                    <span class="skill-tag">Visual Communication</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
