import os 
from .llm_manager import openai_llm
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field, confloat
import matplotlib.pyplot as plt
llm = openai_llm.get_llm_instance(model_name = 'gpt-4o')


class ResumeMatchScores(BaseModel):
    """
    Represents the alignment scores of a resume against a given Job Description (JD) across various categories:
    - skills
    - experience
    - education
    - other criteria
    """
    skill_match: confloat(ge=0, le=1) = Field(
        ...,
        description=(
            "A float between 0 and 1 indicating the degree to which the skills listed in the resume "
            "align with the job description. 0 signifies no match, while 1 signifies a perfect match."
        )
    )
    experience_match: confloat(ge=0, le=1) = Field(
        ...,
        description=(
            "A float between 0 and 1 representing how well the candidate's work experience matches "
            "the job description. 0 indicates no match; 1 indicates a perfect match."
        )
    )
    education_match: confloat(ge=0, le=1) = Field(
        ...,
        description=(
            "A float between 0 and 1 denoting the extent to which the candidate's educational background "
            "aligns with the job requirements. 0 means no match; 1 means a perfect match."
        )
    )
    other_match: confloat(ge=0, le=1) = Field(
        ...,
        description=(
            "A float between 0 and 1 reflecting the alignment of other factors (e.g., soft skills, location, "
            "languages) between the resume and the job description. 0 signifies no match; 1 signifies a perfect match."
        )
    )
    resume_missing_requirements: str = Field(
        ...,
        description=(
            "A string detailing the requirements specified in the Job Description that are "
            "present in the JD but not found in the candidate's resume. This helps identify "
            "gaps in the candidate's qualifications relative to the job requirements."
        )
    )
    key_matches: str = Field(
        ...,
        description=(
            "A string detailing the key requirements specified in the Job Description that are "
            "present in both the JD and the candidate's resume. This helps identify the areas where "
            "the candidate's qualifications align with the job requirements."
        )
    )

    outside_task: str = Field(
        ...,
        description=(
            "Recommended tasks for the candidate post-selection to assess real-world abilities. "
            "These tasks should align with the job description and address gaps identified in the resume(e.g., learning specific tools, gaining experience in a certain domain)."
        )
    )

class ResumeJDAnalyzer:
    """
    A class to analyze resumes against job descriptions (JDs) and provide insights on alignment scores,
    missing requirements, and key matches.
    """
    def __init__(self):
        """
        Initializes the ResumeJDAnalyzer class and sets up the analysis pipeline.
        """
        self.resume_pipeline = self._generate_pipeline()
    def analyze(self,resume:str,jd:str)->dict[str,int]:
        """
        Analyzes a single resume against a job description.
        
        Args:
            resume (str): The content of the candidate's resume.
            jd (str): The content of the job description.

        Returns:
            dictionary[str, int]: A dictionary containing the analysis results.
        """
        result = self._analyze_single_resume(resume_content=resume,jd=jd)
        return result
    def _analyze_single_resume(self, resume_content,jd)->dict:
        """
        Internal method to perform analysis on a single resume.

        Args:
            resume_content (str): The content of the resume.
            jd (str): The content of the job description.

        Returns:
            dict: A dictionary with analysis results.
        """
        return self.resume_pipeline.invoke({"jd_content":jd,"resume_content":resume_content})

    def _generate_pipeline(self):

        template = """Act like an expert in human resources, specializing in matching resumes to job descriptions using structured data models. You have decades of experience in analyzing resumes, identifying key strengths, and recommending improvements to candidates. Your goal is to provide an evaluation of the alignment between a candidate's resume and a job description.
        #### **Steps**:
        1. **Skill Analysis**:
        - Identify the key skills required in the job description.
        - Assess how well the resume matches these skills.
        - Score `skill_match`.

        2. **Experience Analysis**:
        - Review the professional experience listed in the resume.
        - Compare it with the requirements and responsibilities outlined in the job description.
        - Score `experience_match` and justify your reasoning.

        3. **Education Analysis**:
        - Compare the candidate’s educational qualifications with the requirements in the job description.
        - Score `education_match` and describe your rationale.

        4. **Other Match Factors**:
        - Evaluate additional factors such as certifications, projects, extracurricular activities,soft skill and any other relevant information.
        - Score `other_match` and explain how these elements contribute to the overall fit.

        5. **Recommendations for Post-Selection Tasks(outside_task)**:
        - Propose tasks (`outside_task`) to evaluate the candidate's abilities in real-world scenarios.
        - Ensure tasks align with the job requirements and address identified gaps.
        6. **Key matches**
        - Give you description where candidate resume align with the JD.
        Context are below : 
        - Job Description: {jd_content}
        - Resume: {resume_content}
    """
        
        prompt = PromptTemplate(template=template,input_variables=["jd_content","resume_content"]) 
        
        return prompt|llm.with_structured_output(ResumeMatchScores)

    def calculate_score(self,scores):
        """
        Calculates a total suitability score based on weighted factors.

        Args:
            scores (ResumeMatchScores): The analysis scores.

        Returns:
            float: The total weighted suitability score (out of 100).
        """
        matches = scores.__dict__
        skills_score = matches.get("skill_match", 0) * 0.4
        experience_score = matches.get("experience_match", 0) * 0.3
        certifications_score = matches.get("education_match", 0) * 0.2
        other_factors_score = matches.get("other_match", 0) * 0.1
        total_score = skills_score + experience_score + certifications_score + other_factors_score
        return total_score*100
    
    def calculate_scores_list(self, analyses)->list[dict[str,int]]:
        """
        Calculates suitability scores for multiple analyses.

        Args:
            analyses (list): A list of analysis results.

        Returns:
            list[float]: A list of suitability scores for each candidate.
        """
        scores = []
        for analysis in analyses:
            matches = analysis.__dict__
            skills_score = matches.get("skill_match", 0) * 0.4
            experience_score = matches.get("experience_match", 0) * 0.3
            certifications_score = matches.get("education_match", 0) * 0.2
            other_factors_score = matches.get("other_match", 0) * 0.1

            total_score = skills_score + experience_score + certifications_score + other_factors_score
            scores.append(total_score)
        return scores
    
    def visualize_scores(self, candidates,scores):
        """
        Visualizes suitability scores for candidates using a bar chart.

        Args:
            candidates (list[str]): List of candidate names.
            scores (list[float]): List of suitability scores for each candidate.
        """
        plt.bar(candidates, scores, color='skyblue')
        plt.xlabel("Candidates")
        plt.ylabel("Suitability Scores")
        plt.title("Suitability Scores by Candidate")
        plt.show()