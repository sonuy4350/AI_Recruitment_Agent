from crewai import Task

def analyze_job_description_task(agent, job_description_path):
    return Task(
        description=f"Analyze the job description provided in the file: {job_description_path}. "
                    "Extract key responsibilities, required skills, qualifications, and experience levels. "
                    "Provide a structured summary of these requirements.",
        agent=agent,
        expected_output="A structured summary of key responsibilities, required skills, qualifications, and experience levels extracted from the job description."
    )
