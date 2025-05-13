# Resume Optimization Crew

An AI-powered resume optimization system that analyzes job postings, tailors resumes, generates cover letters, and prepares candidates for interviews.

## 📋 Features

- **Resume Analysis**: Extract and evaluate key information from your resume
- **Job Posting Analysis**: Parse job requirements and match against your qualifications
- **Company Research**: Gather insights about target companies for better application strategy
- **Resume Optimization**: Generate tailored versions of your resume for specific job applications
- **Cover Letter Generation**: Create personalized cover letters highlighting your relevant experience
- **Final Report**: Comprehensive analysis with actionable insights for your job application

## 🔧 Tech Stack

- **Framework**: [CrewAI](https://github.com/joaomdmoura/CrewAI) - Orchestrates multiple AI agents
- **UI**: [Streamlit](https://streamlit.io/) - Provides a clean web interface
- **LLM**: [Google Gemini 1.5 Flash](https://ai.google.dev/gemini-api) - Powers agent reasoning
- **PDF Processing**: [pdfplumber](https://github.com/jsvine/pdfplumber) - Extracts text from resumes

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ installed
- Google Gemini API key
- Serper API key (for web search capabilities)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ennajari/resume-optimization-crew.git
cd resume-optimization-crew
```

2. **Set up a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure environment variables**

Create a `.env` file in the project root with the following content:

```
MODEL=gemini/gemini-1.5-flash
GEMINI_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
CREWAI_TELEMETRY_DISABLED=true
```

### Running the Application

#### Command Line Interface

Run the main script:

```bash
python -m src.resume_crew.main
```

This will use the default sample resume and target the default job at McKinsey & Company.

#### Web Interface

Launch the Streamlit web app:

```bash
streamlit run app.py
```

This will open a browser window with the web interface where you can:
1. Upload your resume (PDF format)
2. Enter a job posting URL
3. Specify the target company
4. Submit and view the optimization results

## 📁 Project Structure

```
resume-optimization-crew/
│
├── .env                          # Environment variables (API keys)
├── .gitignore                    # Git ignore file
├── pyproject.toml                # Python project configuration
├── README.md                     # Project documentation
├── uv.lock                       # Dependency lock file
│
├── docs/                         # Documentation files
│
├── knowledge/                    # Storage for uploaded resumes
│   └── current_resume.pdf        # Active resume being processed
│
├── output/                       # Output directory for generated files
│   ├── company_research.json     # Company insights
│   ├── final_report.md           # Complete application strategy
│   ├── job_analysis.json         # Job requirements breakdown
│   ├── optimized_resume.md       # Tailored resume in markdown
│   ├── resume_optimization.json  # Optimization suggestions
│   └── cover_letter.json         # Generated cover letter
│
└── src/                          # Source code
    └── resume_crew/              # Main package
        ├── __init__.py
        ├── crew.py               # CrewAI implementation
        ├── main.py               # Entry point
        ├── models.py             # Data models
        │
        ├── config/               # Configuration files
        │   ├── agents.yaml       # Agent definitions
        │   └── tasks.yaml        # Task definitions
        │
        └── tools/                # Custom tools
            ├── __init__.py
            └── custom_tool.py    # Resume parser tool
```

## 🧩 Components

### Agents

The system utilizes six specialized AI agents:

1. **Resume Analyzer**: Evaluates existing resume content and structure
2. **Job Analyzer**: Extracts key requirements from job postings
3. **Company Researcher**: Gathers insights about target companies
4. **Resume Writer**: Creates tailored resume content
5. **Report Generator**: Compiles comprehensive application strategy
6. **Cover Letter Writer**: Drafts personalized cover letters

### Workflow

1. Upload your resume (PDF format)
2. Provide job posting URL and company name
3. The system processes your information through all agents
4. View and download your optimized resume, cover letter, and strategic insights

## 📝 Output Files

- **optimized_resume.md**: Your tailored resume in markdown format
- **final_report.md**: Strategic insights and recommendations
- **job_analysis.json**: Structured breakdown of job requirements
- **resume_optimization.json**: Specific improvement suggestions
- **company_research.json**: Company insights for interview preparation
- **cover_letter.json**: Personalized cover letter

## 🔍 Customization

### Using a Different Resume

Replace the default resume in the `knowledge` directory or upload your own through the web interface.

### Targeting Different Jobs

Modify the inputs in `main.py` or use the web interface to specify different job URLs and companies.

## 🛠️ Troubleshooting

### API Key Issues

If you encounter errors related to API keys:
- Ensure your `.env` file exists in the project root
- Verify API keys are correctly formatted with no extra spaces
- Check that you haven't exceeded API rate limits

### PDF Reading Problems

If your resume isn't being properly analyzed:
- Ensure it's a searchable PDF (not a scanned image)
- Try re-saving it with a different PDF creator
- Check for unusual formatting that might confuse the parser

### Output Format Issues

If output files contain formatting errors:
- Check the console for error messages
- Try with a simpler resume format
- Ensure job URLs are accessible to the search tool

## 📣 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/CrewAI) for the agent orchestration framework
- [Streamlit](https://streamlit.io/) for the intuitive web interface
- [Google Gemini](https://ai.google.dev/gemini-api) for the AI capabilities