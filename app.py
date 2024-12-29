import streamlit as st
# import time
# import random
from src.pdf_parcer import process_resumes
# Set page configuration
st.set_page_config(
    page_title="Resume Matching App",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50; 
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>input {
        border: 2px solid #ddd;
        padding: 8px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for user instructions
st.sidebar.title("📑 Instructions")
st.sidebar.write(
    """
    1. Upload one or more resumes in PDF format.
    2. Enter the Job Description (JD) in the text box.
    3. Click **Submit** to analyze the resumes.
    4. Wait for results while enjoying the animation!
    """
)

# Main App Title
st.title("🎯 Resume Matching System")

# Resume Upload
st.header("📤 Upload Resumes")
uploaded_files = st.file_uploader(
    "Upload your resumes (PDF format only):",
    type=["pdf"],
    accept_multiple_files=True
)

# Job Description Input
st.header("📝 Enter Job Description")
job_description = st.text_area("Enter the Job Description (JD) below:")

# Submit Button
if st.button("Submit"):
    if not uploaded_files or not job_description.strip():
        st.error("Please upload resumes and provide a Job Description.")
    else:
        st.info("Analyzing resumes against the Job Description. Please wait...")

        results = []
        for file in uploaded_files:
            save_path = "./pdf_data/"+file.name
            with open(save_path, "wb") as f:
                    f.write(file.getbuffer())

            resume_results = process_resumes(file=save_path,job_description=job_description)
            # score = random.randint(60, 100)  # Mock scoring
            results.append({"file_name": file.name, 
                            "score": resume_results["score"],
                            "resume_missing_requirements":resume_results["resume_missing_requirements"],
                            "key_skill_matches":resume_results["key_skill_matches"],
                            "outside_task":resume_results["outside_task"]
                            })

        # Display Results
        st.success("Analysis Complete! Here are the results:")
        for result in results:
            st.markdown(f"### 📄 **{result['file_name']}**")
            st.markdown(f"**Match Score:** `{result['score']}` %")

            # Missing Requirements
            st.markdown("**Resume Missing Requirements:**")
            if result["resume_missing_requirements"]:
                st.markdown( body="- " + "\n - ".join(result["resume_missing_requirements"].split("\n")).replace("•",""))
            else:
                st.markdown("✅ No missing requirements!")

            # Key Skill Matches
            st.markdown("**Key Skill Matches:**")
            if result["key_skill_matches"]:
                st.markdown( body="- " + "\n - ".join(result["key_skill_matches"].split("\n")).replace("•",""))
                # st.markdown(result["key_skill_matches"])
            else:
                st.markdown("❌ No key skills matched!")

            # Outside Tasks
            st.markdown("**Outside Tasks Mentioned:**")
            if result["outside_task"]:
                st.markdown(result["outside_task"])
            else:
                st.markdown("✅ No outside tasks identified!")

            st.markdown("---")  # Separator for each resume

st.markdown(
    """
    ---
    🛠️ Built with **Streamlit** | © 2024 Resume Matcher
    """,
    unsafe_allow_html=True
)
