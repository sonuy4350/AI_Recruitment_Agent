from crewai import Agent
from src.tools.file_read_tool import FileReadTool

def create_resume_screener_agent(llm):
    return Agent(
        role=\'Resume Screener\',
        goal=\'Evaluate candidate resumes against job requirements and identify key matches and gaps.\',
        backstory=\'You are a meticulous resume screener, adept at identifying relevant skills, experience, and education from resumes and comparing them to job descriptions.\',
        verbose=True,
        allow_delegation=False,
        tools=[FileReadTool.read_file],
        llm=llm
    )
