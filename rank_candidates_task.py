from crewai import Task

def rank_candidates_task(agent, job_description_analysis, screened_resumes_reports):
    return Task(
        description=f"Given the job description analysis: {job_description_analysis} "
                    f"and the screened resumes reports: {screened_resumes_reports}, "
                    "rank the candidates from most suitable to least suitable. "
                    "Provide a clear justification for each candidate's ranking and a final ranked list.",
        agent=agent,
        expected_output="A ranked list of candidates with justifications for each ranking, based on their suitability for the job."
    )
