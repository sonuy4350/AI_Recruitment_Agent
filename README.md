# AI Recruitment Agent

This project implements an AI Recruitment Agent using the `crewAI` framework and `Streamlit` for an interactive user interface. It automates the process of analyzing job descriptions, screening resumes, ranking candidates, and generating interview questions.

## Features

- **Job Description Analysis**: Extracts key skills, responsibilities, and qualifications.
- **Resume Screening**: Compares resumes against job requirements.
- **Candidate Ranking**: Ranks candidates based on suitability with justifications.
- **Interview Question Generation**: Creates tailored interview questions for top candidates.
- **Interactive Streamlit UI**: User-friendly interface for file uploads and result visualization.
- **Multiple LLM Provider Support**: Choose between OpenAI, Groq, and Google Gemini for your AI models.

## Project Structure

```
ai_recruitment_agent/
├── app.py                 # Main Streamlit application entry point
├── src/
│   ├── agents/            # Definitions for specialized AI agents
│   │   ├── __init__.py
│   │   ├── job_analyzer_agent.py
│   │   ├── resume_screener_agent.py
│   │   ├── candidate_ranker_agent.py
│   │   └── interview_question_generator_agent.py
│   ├── tasks/             # Task definitions for each agent
│   │   ├── __init__.py
│   │   ├── analyze_job_description_task.py
│   │   ├── screen_resume_task.py
│   │   ├── rank_candidates_task.py
│   │   └── generate_interview_questions_task.py
│   ├── tools/             # Custom tools (e.g., file reading)
│   │   ├── __init__.py
│   │   └── file_read_tool.py
│   ├── llm_config.py      # LLM provider configuration
│   └── crew.py            # Crew orchestration logic
├── data/
│   ├── job_descriptions/  # Placeholder for job description files
│   └── resumes/           # Placeholder for candidate resumes
├── .env.example           # Example environment variables
├── .gitignore
├── README.md
├── requirements.txt       # Project dependencies
└── SKILL.md
```

## Setup Guide (macOS)

Follow these steps to set up and run the AI Recruitment Agent on your macOS machine.

### Prerequisites

*   **Python 3.9+**: Ensure Python is installed. You can download it from [python.org](https://www.python.org/downloads/) or use Homebrew (`brew install python`).
*   **pip**: Python's package installer, usually comes with Python.
*   **API Keys**: Depending on your chosen LLM provider, you will need an API key:
    *   **Groq**: Recommended for fast, free inference. Get your API key from [console.groq.com](https://console.groq.com).
    *   **Google Gemini**: Offers free API access. Get your API key from [ai.google.dev](https://ai.google.dev).
    *   **OpenAI**: Requires a paid API key. Get one from [platform.openai.com](https://platform.openai.com/account/api-keys).

### 1. Clone the Repository (or create project structure)

If you received this project as a zip file, extract it. Otherwise, if you are setting up from scratch, create the project directory and subdirectories as described in the `Project Structure` section.

```bash
mkdir -p ai_recruitment_agent/src/agents \
         ai_recruitment_agent/src/tasks \
         ai_recruitment_agent/src/tools \
         ai_recruitment_agent/data/job_descriptions \
         ai_recruitment_agent/data/resumes
```

### 2. Navigate to the Project Directory

```bash
cd ai_recruitment_agent
```

### 3. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all required Python packages using `pip`.

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Rename `.env.example` to `.env` and add your chosen API key(s).

```bash
mv .env.example .env
```

Open the newly created `.env` file with a text editor and add your API key. For example:

```ini
# .env
GROQ_API_KEY=your_groq_api_key_here
# GOOGLE_API_KEY=your_google_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
```

### 6. Run the Streamlit Application

Start the Streamlit application from the project root directory.

```bash
streamlit run app.py
```

This will open the application in your default web browser. You can then upload job descriptions and resumes to start the recruitment process.

## Usage

1.  **Select LLM Provider**: In the sidebar, choose your preferred LLM provider (Groq, Gemini, or OpenAI) and model.
2.  **Upload Job Description**: Upload a `.txt`, `.md`, `.pdf`, or `.docx` file containing the job description.
3.  **Upload Resumes**: Upload one or more `.pdf`, `.docx`, or `.txt` files for candidate resumes.
4.  **Start Process**: Click the "Start Recruitment Process" button.
5.  **View Results**: The application will display the job analysis, resume screening reports, candidate rankings, and interview questions in separate tabs.

## Troubleshooting

*   **API Key Not Found**: Ensure your API key (e.g., `GROQ_API_KEY`) is correctly set in the `.env` file for the selected provider.
*   **Dependency Issues**: Make sure all packages from `requirements.txt` are installed in your virtual environment.
*   **File Upload Errors**: Check the file types and ensure they are supported (`.txt`, `.md`, `.pdf`, `.docx`).
*   **`unstructured` library**: If you encounter issues with PDF/DOCX parsing, ensure all necessary system dependencies for `unstructured[all-docs]` are installed. For macOS, this typically involves `poppler` for PDFs. You can install it via Homebrew: `brew install poppler`.

## Contributing

Feel free to fork the repository, submit pull requests, or open issues for any bugs or feature requests.

## License

This project is open-source and available under the MIT License.
