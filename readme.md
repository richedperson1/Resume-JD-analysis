Here's a comprehensive `README.md` file for your Streamlit Resume Matching application:

---

# 🎯 Resume Matching System

A visually engaging and functional **Streamlit** application for matching resumes against a given Job Description (JD). This app allows users to upload multiple resumes in PDF format, input a JD, and receive an analysis of how well the resumes align with the provided requirements.

---

## 🌟 Features

- **📤 Resume Upload**: Upload multiple resumes in PDF format.
- **📝 Job Description Input**: Enter the JD for comparison.
- **⚙️ Backend Integration**: Simulates a backend process for analyzing resumes.
- **⏳ Interactive Loading Animation**: Displays a spinner while processing.
- **📊 Detailed Results**:
  - **Match Score**: Overall alignment score between the resume and JD.
  - **Missing Requirements**: Highlights missing qualifications.
  - **Key Skill Matches**: Lists the matched skills.
  - **Outside Tasks**: Identifies irrelevant tasks mentioned in the resume.

---

## 🚀 How It Works

1. **Upload Resumes**: Drag and drop one or more PDF resumes into the uploader.
2. **Enter Job Description**: Provide the job description in the text input box.
3. **Submit**: Click the "Submit" button to start the analysis.
4. **View Results**:
   - Each resume is scored and analyzed.
   - Detailed feedback is displayed for missing requirements, key skills, and outside tasks.

---

## 🛠️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/resume-matching-system.git
   cd resume-matching-system
   ```

2. Create a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## 📦 Requirements

- Python 3.12 or higher
- Libraries:
  - `streamlit`
  - `docling`
  - `openai`
  - `langchain`

---

## 📊 Example Output

### **Match Score:** `85%`

#### **Resume Missing Requirements:**

- Project Management Certification
- Experience with SQL databases

#### **Key Skill Matches:**

- Python
- Machine Learning
- Data Analysis

#### **Outside Tasks Mentioned:**

- Graphic Design
- Social Media Management

---

## 📁 File Structure

```
resume-matching-system/
│
├── app.py
├── src           # Main Streamlit application script
    ├── chain_function.py  # Backend logic for processing resumes
    ├── llm_manager.py  # managing of llm
    ├── pdf_parcer.py # handling parcing the pdf
├── requirements.txt    # List of dependencies
├── README.md           # Project documentation
```

---

## 🖥️ Deployment

To deploy the app:

1. Host on **Streamlit Community Cloud**:

   - Push your repository to GitHub.
   - Deploy via Streamlit Sharing: [https://share.streamlit.io](https://share.streamlit.io).

---

## 🔧 Customization

- Update the `process_resumes` function in `process_resumes.py` to integrate your backend logic.
- Customize the frontend design using CSS in the `app.py` script.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the app.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🛠️ Built With

- **Python**
- **Streamlit**
- **Docling**
- **Langchain**

---

Let me know if you'd like to adjust the structure or content further!
