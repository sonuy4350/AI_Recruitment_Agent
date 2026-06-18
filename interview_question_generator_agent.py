from crewai import Agent

def create_interview_question_generator_agent(llm):
    return Agent(
        role=\'Interview Question Generator\',
        goal=\'Generate relevant and insightful interview questions based on job description and candidate\'s resume.\',
        backstory=\'You are an expert interviewer who can craft targeted questions to assess a candidate\'s skills, experience, and cultural fit, drawing insights from both the job description and their resume.\',
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
