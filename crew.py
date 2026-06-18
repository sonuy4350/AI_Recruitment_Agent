from crewai import Crew, Process
from src.agents.job_analyzer_agent import create_job_analyzer_agent
from src.agents.resume_screener_agent import create_resume_screener_agent
from src.agents.candidate_ranker_agent import create_candidate_ranker_agent
from src.agents.interview_question_generator_agent import create_interview_question_generator_agent
from src.tasks.analyze_job_description_task import analyze_job_description_task
from src.tasks.screen_resume_task import screen_resume_task
from src.tasks.rank_candidates_task import rank_candidates_task
from src.tasks.generate_interview_questions_task import generate_interview_questions_task

class RecruitmentCrew:
    def __init__(self, llm):
        self.llm = llm

    def run(self, job_description_path, resume_paths):
        # Create Agents
        job_analyzer = create_job_analyzer_agent(self.llm)
        resume_screener = create_resume_screener_agent(self.llm)
        candidate_ranker = create_candidate_ranker_agent(self.llm)
        interview_question_generator = create_interview_question_generator_agent(self.llm)

        # Create Tasks
        task_analyze_job = analyze_job_description_task(job_analyzer, job_description_path)

        screened_reports = []
        for i, resume_path in enumerate(resume_paths):
            task_screen_resume = screen_resume_task(resume_screener, resume_path, task_analyze_job.output)
            screened_reports.append(task_screen_resume)

        task_rank_candidates = rank_candidates_task(candidate_ranker, task_analyze_job.output, [report.output for report in screened_reports])

        # For simplicity, let's generate interview questions for the top candidate (assuming the ranker output is a list of ranked candidates)
        # In a real scenario, you might parse the ranked list to get the top candidate's report
        # For now, we'll just take the first screened report as an example for interview questions
        task_generate_interview_questions = generate_interview_questions_task(
            interview_question_generator,
            task_analyze_job.output,
            screened_reports[0].output if screened_reports else "No resumes screened."
        )

        # Create Crew
        crew = Crew(
            agents=[
                job_analyzer,
                resume_screener,
                candidate_ranker,
                interview_question_generator
            ],
            tasks=[
                task_analyze_job,
                *screened_reports, # Unpack the list of resume screening tasks
                task_rank_candidates,
                task_generate_interview_questions
            ],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result
