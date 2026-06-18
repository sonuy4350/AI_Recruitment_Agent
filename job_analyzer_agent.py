from crewai import Agent
from src.tools.file_read_tool import FileReadTool

def create_job_analyzer_agent(llm):
    return Agent(
        role='Senior Job Description Analyst',
        goal='Analyze job descriptions to extract key requirements, skills, and qualifications.',
        backstory='You are an expert HR analyst with years of experience in decoding job descriptions. You can quickly identify the core competencies and essential qualifications required for any role.',
        verbose=True,
        allow_delegation=False,
        tools=[FileReadTool.read_file],
        llm=llm
    )
