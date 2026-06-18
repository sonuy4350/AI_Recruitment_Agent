import os
os.environ["CREWAI_CACHE"] = "false"
os.environ["LITELLM_DISABLE_CACHE"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
import crewai
import litellm
import sys
import streamlit as st
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import tempfile
from pathlib import Path
import json
from datetime import datetime
from src.llm_config import LLMConfig
import nltk
import litellm
litellm.set_verbose = True
litellm.cache = None
# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    import ssl
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="AI Recruitment Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "crew_results" not in st.session_state:
    st.session_state.crew_results = None
if "job_analysis" not in st.session_state:
    st.session_state.job_analysis = None
if "resume_screenings" not in st.session_state:
    st.session_state.resume_screenings = []
if "candidate_rankings" not in st.session_state:
    st.session_state.candidate_rankings = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None

# Agent Creation Functions
def create_job_analyzer_agent(llm):
    return Agent(
        role='Senior Job Description Analyst',
        goal='Analyze job descriptions to extract key requirements, skills, and qualifications.',
        backstory='You are an expert HR analyst with years of experience in decoding job descriptions. You can quickly identify the core competencies and essential qualifications required for any role.',
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

def create_resume_screener_agent(llm):
    return Agent(
        role='Resume Screener',
        goal='Evaluate candidate resumes against job requirements and identify key matches and gaps.',
        backstory='You are a meticulous resume screener, adept at identifying relevant skills, experience, and education from resumes and comparing them to job descriptions.',
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

def create_candidate_ranker_agent(llm):
    return Agent(
        role='Candidate Ranker',
        goal='Rank candidates based on their suitability for a given job description, providing a score and justification.',
        backstory='You are an experienced recruitment consultant who can objectively assess and rank candidates based on their resumes and the job requirements. You provide clear, concise justifications for your rankings.',
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

def create_interview_question_generator_agent(llm):
    return Agent(
        role='Interview Question Generator',
        goal='Generate relevant and insightful interview questions based on job description and candidate\'s resume.',
        backstory='You are an expert interviewer who can craft targeted questions to assess a candidate\'s skills, experience, and cultural fit, drawing insights from both the job description and their resume.',
        verbose=False,
        allow_delegation=False,
        llm=llm
    )

# Task Creation Functions
def create_job_analysis_task(agent, job_description_content):
    return Task(
        description=f"Analyze the following job description and extract key requirements, skills, and qualifications:\n\n{job_description_content}\n\nProvide a structured summary of these requirements.",
        agent=agent,
        expected_output="A structured summary of key responsibilities, required skills, qualifications, and experience levels extracted from the job description."
    )

def create_resume_screening_task(agent, resume_content, job_analysis):
    return Task(
        description=f"Screen the following resume and compare it against the job requirements:\n\nResume:\n{resume_content}\n\nJob Requirements:\n{job_analysis}\n\nProvide a detailed report on how well the resume matches the job description, highlighting strengths and gaps.",
        agent=agent,
        expected_output="A detailed report comparing the resume to the job description, highlighting strengths and gaps, and a match score."
    )

def create_candidate_ranking_task(agent, job_analysis, resume_screenings):
    return Task(
        description=f"Given the job description analysis and the screened resumes reports, rank the candidates from most suitable to least suitable.\n\nJob Analysis:\n{job_analysis}\n\nResume Screenings:\n{resume_screenings}\n\nProvide a clear justification for each candidate's ranking and a final ranked list.",
        agent=agent,
        expected_output="A ranked list of candidates with justifications for each ranking, based on their suitability for the job."
    )

def create_interview_questions_task(agent, job_analysis, top_candidate_report):
    return Task(
        description=f"Based on the job description analysis and the top candidate's screening report, generate a list of 5-7 insightful interview questions.\n\nJob Analysis:\n{job_analysis}\n\nCandidate Report:\n{top_candidate_report}\n\nThese questions should assess the candidate's skills, experience, and problem-solving abilities relevant to the role.",
        agent=agent,
        expected_output="A list of 5-7 tailored interview questions for the top candidate."
    )

# Main App
st.markdown("<h1 class='main-header'>🤖 AI Recruitment Agent</h1>", unsafe_allow_html=True)

st.markdown("""
This application automates the recruitment process using **crewAI** and **Streamlit**:
- 📄 **Analyze Job Descriptions**: Extract key requirements and qualifications
- 📋 **Screen Resumes**: Compare candidate qualifications against job requirements
- 🏆 **Rank Candidates**: Score and rank candidates based on suitability
- ❓ **Generate Interview Questions**: Create tailored questions for top candidates
""")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    # LLM Provider Selection
    provider = st.selectbox(
        "Select LLM Provider",
        ["groq", "gemini", "openai"],
        help="Choose the LLM provider to use. Groq and Gemini offer free tiers."
    )
    
    # Get available models for the selected provider
    available_models = LLMConfig.get_available_models(provider)
    model = st.selectbox(
        "Select Model",
        available_models,
        help="Choose the model for the selected provider"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative"
    )
    
    st.markdown("---")
    
    # API Key Status Check
    st.subheader("📋 API Key Status")
    
    if provider == "groq":
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            st.success("✅ Groq API Key found")
        else:
            st.error("❌ Groq API Key not found. Add GROQ_API_KEY to .env")
    elif provider == "gemini":
        gemini_key = os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            st.success("✅ Google Gemini API Key found")
        else:
            st.error("❌ Gemini API Key not found. Add GOOGLE_API_KEY to .env")
    elif provider == "openai":
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            st.success("✅ OpenAI API Key found")
        else:
            st.error("❌ OpenAI API Key not found. Add OPENAI_API_KEY to .env")
    
    st.markdown("---")
    
    # Provider Information
    st.subheader("ℹ️ Provider Info")
    
    if provider == "groq":
        st.info("""
        **Groq** offers free API access with generous rate limits.
        - Get API key: [console.groq.com](https://console.groq.com)
        - Fast inference with Mixtral and Llama models
        """)
    elif provider == "gemini":
        st.info("""
        **Google Gemini** offers free API access.
        - Get API key: [ai.google.dev](https://ai.google.dev)
        - Powerful multimodal models
        """)
    else:
        st.info("""
        **OpenAI** requires a paid API key.
        - Get API key: [platform.openai.com](https://platform.openai.com/account/api-keys)
        """)

# Main Content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<h2 class='sub-header'>📄 Job Description</h2>", unsafe_allow_html=True)
    job_description_file = st.file_uploader(
        "Upload Job Description",
        type=["txt", "md", "pdf", "docx"],
        key="job_description"
    )

with col2:
    st.markdown("<h2 class='sub-header'>📋 Resumes</h2>", unsafe_allow_html=True)
    resume_files = st.file_uploader(
        "Upload Resumes (Multiple files allowed)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="resumes"
    )

# Process Button
if st.button("🚀 Start Recruitment Process", use_container_width=True):
    if job_description_file is None:
        st.error("❌ Please upload a Job Description file.")
    elif not resume_files:
        st.error("❌ Please upload at least one Resume file.")
    else:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Initialize LLM
            status_text.text(f"🔧 Initializing {provider.upper()} LLM...")
            progress_bar.progress(5)
            
            llm = LLMConfig.get_llm(provider=provider, model=model, temperature=temperature)
            
            # Save uploaded files to temporary directory
            temp_dir = tempfile.mkdtemp()
            
            # Read job description
            status_text.text("📖 Reading job description...")
            progress_bar.progress(10)
            
            job_description_path = os.path.join(temp_dir, job_description_file.name)
            with open(job_description_path, "wb") as f:
                f.write(job_description_file.getbuffer())
            
            # Read job description content
            from unstructured.partition.auto import partition
            job_elements = partition(filename=job_description_path)
            job_description_content = "\n".join([str(el) for el in job_elements])
            
            # Read resumes
            status_text.text("📋 Reading resumes...")
            progress_bar.progress(20)
            
            resume_paths = []
            resume_contents = {}
            for resume_file in resume_files:
                path = os.path.join(temp_dir, resume_file.name)
                with open(path, "wb") as f:
                    f.write(resume_file.getbuffer())
                resume_paths.append(path)
                
                # Read resume content
                resume_elements = partition(filename=path)
                resume_contents[resume_file.name] = "\n".join([str(el) for el in resume_elements])
            
            # Create Agents
            status_text.text("🤖 Creating AI Agents...")
            progress_bar.progress(30)
            
            job_analyzer = create_job_analyzer_agent(llm)
            resume_screener = create_resume_screener_agent(llm)
            candidate_ranker = create_candidate_ranker_agent(llm)
            interview_generator = create_interview_question_generator_agent(llm)
            
            # Create Tasks
            status_text.text("📝 Creating tasks...")
            progress_bar.progress(40)
            
            job_analysis_task = create_job_analysis_task(job_analyzer, job_description_content)
            
            # Execute job analysis
            status_text.text("🔍 Analyzing job description...")
            progress_bar.progress(50)
            
            job_analysis_crew = Crew(
                agents=[job_analyzer],
                tasks=[job_analysis_task],
                process=Process.sequential,
                verbose=False,
                cache=False # Disable caching to fix Groq compatibility
            )
            job_analysis_result = job_analysis_crew.kickoff()
            st.session_state.job_analysis = str(job_analysis_result)
            
            # Screen resumes
            status_text.text("📋 Screening resumes...")
            progress_bar.progress(60)
            
            resume_screening_results = []
            for resume_name, resume_content in resume_contents.items():
                resume_screening_task = create_resume_screening_task(
                    resume_screener,
                    resume_content,
                    st.session_state.job_analysis
                )
                
                resume_crew = Crew(
                    agents=[resume_screener],
                    tasks=[resume_screening_task],
                    process=Process.sequential,
                    verbose=False,
                    cache=False # Disable caching to fix Groq compatibility
                )
                
                screening_result = resume_crew.kickoff()
                resume_screening_results.append({
                    "resume": resume_name,
                    "screening": str(screening_result)
                })
            
            st.session_state.resume_screenings = resume_screening_results
            
            # Rank candidates
            status_text.text("🏆 Ranking candidates...")
            progress_bar.progress(75)
            
            screening_summary = "\n\n".join([
                f"Resume: {item['resume']}\n{item['screening']}"
                for item in resume_screening_results
            ])
            
            ranking_task = create_candidate_ranking_task(
                candidate_ranker,
                st.session_state.job_analysis,
                screening_summary
            )
            
            ranking_crew = Crew(
                agents=[candidate_ranker],
                tasks=[ranking_task],
                process=Process.sequential,
                verbose=False,
                cache=False # Disable caching to fix Groq compatibility
            )
            
            ranking_result = ranking_crew.kickoff()
            st.session_state.candidate_rankings = str(ranking_result)
            
            # Generate interview questions for top candidate
            status_text.text("❓ Generating interview questions...")
            progress_bar.progress(90)
            
            top_candidate_report = resume_screening_results[0]["screening"] if resume_screening_results else ""
            
            interview_task = create_interview_questions_task(
                interview_generator,
                st.session_state.job_analysis,
                top_candidate_report
            )
            
            interview_crew = Crew(
                agents=[interview_generator],
                tasks=[interview_task],
                process=Process.sequential,
                verbose=False,
                cache=False # Disable caching to fix Groq compatibility
            )
            
            interview_result = interview_crew.kickoff()
            st.session_state.interview_questions = str(interview_result)
            
            status_text.text("✅ Recruitment process completed!")
            progress_bar.progress(100)
            
            # Clean up temporary files
            import shutil
            shutil.rmtree(temp_dir)
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            import traceback
            st.error(traceback.format_exc())

# Display Results
if st.session_state.job_analysis:
    st.markdown("<h2 class='sub-header'>📊 Results</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Job Analysis", "Resume Screening", "Candidate Rankings", "Interview Questions"])
    
    with tab1:
        st.markdown("### Job Description Analysis")
        st.markdown(st.session_state.job_analysis.replace("\\n", "\n"))
    
    with tab2:
        st.markdown("### Resume Screening Reports")
        for item in st.session_state.resume_screenings:
            with st.expander(f"📄 {item['resume']}"):
                st.markdown(item['screening'].replace("\\n", "\n"))
    
    with tab3:
        st.markdown("### Candidate Rankings")
        st.markdown(st.session_state.candidate_rankings.replace("\\n", "\n"))
    
    with tab4:
        st.markdown("### Interview Questions for Top Candidate")
        st.markdown(st.session_state.interview_questions.replace("\\n", "\n"))
    
    # Export Results
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Results as JSON"):
            results = {
                "timestamp": datetime.now().isoformat(),
                "llm_provider": provider,
                "llm_model": model,
                "job_analysis": st.session_state.job_analysis,
                "resume_screenings": st.session_state.resume_screenings,
                "candidate_rankings": st.session_state.candidate_rankings,
                "interview_questions": st.session_state.interview_questions
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(results, indent=2),
                file_name=f"recruitment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Clear Results"):
            st.session_state.crew_results = None
            st.session_state.job_analysis = None
            st.session_state.resume_screenings = []
            st.session_state.candidate_rankings = None
            st.session_state.interview_questions = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Powered by <strong>crewAI</strong> and <strong>Streamlit</strong></p>
    <p>🤖 AI Recruitment Agent v2.0 (Multi-Provider LLM Support)</p>
</div>
""", unsafe_allow_html=True)
