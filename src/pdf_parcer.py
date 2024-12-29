
from docling.document_converter import DocumentConverter
from .chain_function import ResumeJDAnalyzer
pdf_loader = DocumentConverter()

resume_obj = ResumeJDAnalyzer()

def process_resumes(file, job_description ):
    """
    Simulates processing resumes against a job description.
    
    Args:
        file (str) : local file path in string.
        job_description (str): Job Description provided by the user.
    
    Returns:
        dict: dictionary containing resume key_skill_matches resume_missing_requirements,and a mock score.
    """
    # results = []
    try:
        pdf_process_obj = pdf_loader.convert(file)
        pdf_reader = pdf_process_obj.document.export_to_markdown()
        resume_details = resume_obj.analyze(resume=pdf_reader,jd=job_description)
        resume_scores = resume_obj.calculate_score(scores=resume_details)
        print("resume_scores ==> ",resume_scores)
        print("resume_details ==> ",resume_details)
        return({"key_skill_matches": resume_details.key_matches,        "resume_missing_requirements":resume_details.resume_missing_requirements, 
                "score": resume_scores,"outside_task":resume_details.outside_task})
    except Exception as e:
        print(f"error occured at backend due to {e}")
        # results.append({"file_name": file, "score": 0, "error": str(e)})
