# Resume Optimization Crew

A powerful AI-powered resume optimization system that helps job seekers tailor their resumes for specific positions, analyze job requirements, research companies, and prepare for interviews.

![CrewAI Logo](docs/crewai_logo.svg)

## Project Overview

The Resume Optimization Crew uses a team of specialized AI agents working together to:

1. **Analyze Job Requirements** - Extract and categorize technical skills, soft skills, and experience requirements
2. **Optimize Resumes** - Provide tailored suggestions to improve content and formatting
3. **Research Companies** - Gather insights about company culture, recent developments, and interview preparation
4. **Generate Optimized Resumes** - Create beautifully formatted, ATS-optimized resumes in markdown
5. **Create Comprehensive Reports** - Produce detailed reports with actionable recommendations

## System Architecture


The project uses [CrewAI](https://github.com/crewai/crewai), a framework for orchestrating role-playing AI agents. These specialized agents work together sequentially to complete the resume optimization process:

- **Resume Analyzer** - Analyzes PDF resumes and provides structured optimization suggestions
- **Job Analyzer** - Breaks down job descriptions and scores candidate fit
- **Company Researcher** - Gathers intelligence on target companies
- **Resume Writer** - Creates beautifully formatted, ATS-optimized resumes
- **Report Generator** - Produces comprehensive, actionable reports

## Setup and Installation

### Prerequisites

- Python 3.10+ 
- Google Gemini Pro API key 
- (Optional) SerperDev API key for enhanced company research

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/resume-optimization-crew.git
   cd resume-optimization-crew
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   pip install pyyaml crewai-tools python-dotenv
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   MODEL=gemini/gemini-1.5-flash
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPER_API_KEY=your_serper_api_key_here  # Optional
   ```

5. Place a resume PDF file in the knowledge directory:
   ```bash
   mkdir -p knowledge
   # Add a resume PDF to the knowledge directory named CV_Mohan.pdf
   # or modify the code to use your own filename
   ```

### Running the Application

Run the application with:

```bash
python src/resume_crew/main.py
```

The process will analyze a job posting for McKinsey & Co, compare it with the provided resume, and generate:

1. Job analysis (output/job_analysis.json)
2. Resume optimization suggestions (output/resume_optimization.json)
3. Company research (output/company_research.json)
4. Optimized resume (output/optimized_resume.md)
5. Comprehensive report (output/final_report.md)

## Customization

### Using Your Own Resume

To use your own resume, place your PDF file in the `knowledge` directory and update the `resume_path` variable in `src/resume_crew/crew.py`.

### Targeting Different Jobs

Modify the inputs in `src/resume_crew/main.py`:

```python
inputs = {
    'job_url': 'https://your-job-posting-url.com',
    'company_name': 'Target Company Name'
}
```

### Configuring Agents and Tasks

Agents and tasks are configured via YAML files in `src/resume_crew/config/`:

- `agents.yaml` - Define roles, goals, and backstories for agents
- `tasks.yaml` - Define detailed instructions for each task

## Output Examples

### Job Analysis

The job analysis provides detailed insights about job requirements and candidate fit:

```json
{
  "technical_skills": ["data analysis", "project management", "consulting"],
  "soft_skills": ["communication", "leadership", "teamwork"],
  "experience_requirements": ["2+ years in consulting or related field"],
  "key_responsibilities": ["client engagement", "problem solving", "analysis"],
  "match_score": {
    "overall_match": 85.5,
    "technical_skills_match": 90.0,
    "soft_skills_match": 85.0
  }
}
```

