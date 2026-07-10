import streamlit as st
import pandas as pd

from utils.pdf_parser import extract_text_from_pdf
from utils.preprocess import preprocess_text
from utils.skill_extractor import extract_skills
from utils.ranking import rank_resumes

st.set_page_config(
    page_title="Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Screening & Candidate Ranking System")

st.markdown("---")

# ==========================
# Input Section
# ==========================

col1, col2 = st.columns([2, 1])

with col1:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste Job Description",
        height=250,
        placeholder="Paste the complete job description here..."
    )

with col2:

    st.subheader("📄 Upload Resume(s)")

    uploaded_files = st.file_uploader(
        "Upload PDF Resume(s)",
        type=["pdf"],
        accept_multiple_files=True
    )

st.markdown("---")

analyze = st.button(
    "🚀 Analyze Candidates",
    use_container_width=True
)

# ==========================
# Analysis
# ==========================

if analyze:

    if not job_description:
        st.warning("⚠ Please enter a Job Description.")

    elif not uploaded_files:
        st.warning("⚠ Please upload at least one resume.")

    else:

        clean_job = preprocess_text(job_description)
        job_skills = extract_skills(clean_job)

        resume_names = []
        resume_texts = []
        resume_skills = []
        original_texts = []

        with st.spinner("Analyzing resumes..."):

            for pdf in uploaded_files:

                text = extract_text_from_pdf(pdf)
                clean_resume = preprocess_text(text)
                skills = extract_skills(clean_resume)

                original_texts.append(text)
                resume_names.append(pdf.name)
                resume_texts.append(clean_resume)
                resume_skills.append(skills)

            scores = rank_resumes(
                resume_texts,
                clean_job
            )

        results = pd.DataFrame({
            "Resume": resume_names,
            "Score": scores,
            "Skills": resume_skills,
            "Preview": original_texts
        })

        results["Match %"] = (
            results["Score"] * 100
        ).round(2)

        results = results.sort_values(
            by="Score",
            ascending=False
        ).reset_index(drop=True)

        st.success("✅ Analysis Complete!")

        st.markdown("## 🏆 Candidate Rankings")

        st.dataframe(
            results[["Resume", "Match %"]],
            use_container_width=True
        )

        st.markdown("---")

        # ==========================
        # Display Each Resume
        # ==========================

        for i in range(len(results)):

            row = results.iloc[i]

            st.subheader(
                f"#{i+1} {row['Resume']} — {row['Match %']}%"
            )

            matched = sorted(
                list(
                    set(row["Skills"]) &
                    set(job_skills)
                )
            )

            missing = sorted(
                list(
                    set(job_skills) -
                    set(row["Skills"])
                )
            )

            colA, colB = st.columns(2)

            with colA:

                st.markdown("### ✅ Detected Skills")

                if row["Skills"]:
                    st.success(", ".join(row["Skills"]))
                else:
                    st.info("No known skills detected.")

                st.markdown("### 🟢 Matched Skills")

                if matched:
                    st.success(", ".join(matched))
                else:
                    st.warning("No matched skills.")

            with colB:

                st.markdown("### 🎯 Required Skills")

                if job_skills:
                    st.info(", ".join(job_skills))
                else:
                    st.warning("No skills detected in job description.")

                st.markdown("### 🔴 Missing Skills")

                if missing:
                    st.error(", ".join(missing))
                else:
                    st.success("No missing skills 🎉")

            with st.expander("📄 Resume Preview"):

                preview = row["Preview"]

                if len(preview) > 2000:
                    st.text(preview[:2000] + "...")
                else:
                    st.text(preview)

            st.markdown("---")