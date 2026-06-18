from crewai import Task

def generate_interview_questions_task(agent, job_description_analysis, candidate_report):
    return Task(
        description=f"Based on the job description analysis: {job_description_analysis} "
                    f"and the candidate's screening report: {candidate_report}, "
                    "generate a list of 5-7 insightful interview questions. "
                    "These questions should assess the candidate's skills, experience, and problem-solving abilities relevant to the role.",
        agent=agent,
        expected_output="A list of 5-7 tailored interview questions for the candidate."
    )
