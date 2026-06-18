from crewai import Task

def screen_resume_task(agent, resume_path, job_description_analysis):
    return Task(
        description=f"Screen the resume provided in the file: {resume_path}. "
                    "Compare the candidate's skills, experience, and education against the job requirements "
                    "derived from the job description analysis: {job_description_analysis}. "
                    "Provide a detailed report on how well the resume matches the job description, highlighting strengths and gaps.",
        agent=agent,
        expected_output="A detailed report comparing the resume to the job description, highlighting strengths and gaps, and a match score."
    )
