import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pathlib import Path
import yaml
from typing import Dict, Any

@CrewBase
class ResumeCrew:
    """ResumeCrew for resume optimization and interview preparation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        """Initialize the crew with configurations"""
        # Get the base directory for the project
        self.base_dir = Path(__file__).parent.parent.parent
        self.knowledge_dir = self.base_dir / "knowledge"
        self.resume_path = str(self.knowledge_dir / "Ennajari.pdf")
        
        # Load configurations
        agents_path = Path(__file__).parent / self.agents_config
        with open(agents_path, 'r') as f:
            self.agents_yaml = yaml.safe_load(f)
            
        tasks_path = Path(__file__).parent / self.tasks_config
        with open(tasks_path, 'r') as f:
            self.tasks_yaml = yaml.safe_load(f)

    def _create_task_config(self, task_name: str) -> Dict[str, Any]:
        """Helper method to convert task YAML to proper dict config"""
        task_data = self.tasks_yaml[task_name]
        return {
            "description": task_data.get("description", ""),
            "expected_output": task_data.get("expected_output", ""),
            "agent": task_data.get("agent", None),
            "context": task_data.get("context", [])
        }

    @agent
    def resume_analyzer(self) -> Agent:
        return Agent(
            role=self.agents_yaml['resume_analyzer']['role'],
            goal=self.agents_yaml['resume_analyzer']['goal'],
            backstory=self.agents_yaml['resume_analyzer']['backstory'],
            verbose=True,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GEMINI_API_KEY")
            )
        )
    
    @agent
    def job_analyzer(self) -> Agent:
        return Agent(
            role=self.agents_yaml['job_analyzer']['role'],
            goal=self.agents_yaml['job_analyzer']['goal'],
            backstory=self.agents_yaml['job_analyzer']['backstory'],
            verbose=True,
            tools=[ScrapeWebsiteTool()],
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GEMINI_API_KEY")
            )
        )

    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            role=self.agents_yaml['company_researcher']['role'],
            goal=self.agents_yaml['company_researcher']['goal'],
            backstory=self.agents_yaml['company_researcher']['backstory'],
            verbose=True,
            tools=[SerperDevTool()],
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GEMINI_API_KEY")
            )
        )

    @agent
    def resume_writer(self) -> Agent:
        return Agent(
            role=self.agents_yaml['resume_writer']['role'],
            goal=self.agents_yaml['resume_writer']['goal'],
            backstory=self.agents_yaml['resume_writer']['backstory'],
            verbose=True,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GEMINI_API_KEY")
            )
        )

    @agent
    def report_generator(self) -> Agent:
        return Agent(
            role=self.agents_yaml['report_generator']['role'],
            goal=self.agents_yaml['report_generator']['goal'],
            backstory=self.agents_yaml['report_generator']['backstory'],
            verbose=True,
            llm=LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.getenv("GEMINI_API_KEY")
            )
        )

    @task
    def analyze_job_task(self) -> Task:
        task_config = self._create_task_config('analyze_job_task')
        
        return Task(
            description=task_config["description"],
            expected_output=task_config["expected_output"],
            agent=self.job_analyzer(),
            output_file='output/job_analysis.json'
        )

    @task
    def optimize_resume_task(self) -> Task:
        task_config = self._create_task_config('optimize_resume_task')
        
        return Task(
            description=task_config["description"],
            expected_output=task_config["expected_output"],
            agent=self.resume_analyzer(),
            context=[self.analyze_job_task()],
            output_file='output/resume_optimization.json'
        )

    @task
    def research_company_task(self) -> Task:
        task_config = self._create_task_config('research_company_task')
        
        return Task(
            description=task_config["description"],
            expected_output=task_config["expected_output"],
            agent=self.company_researcher(),
            context=[self.analyze_job_task(), self.optimize_resume_task()],
            output_file='output/company_research.json'
        )

    @task
    def generate_resume_task(self) -> Task:
        task_config = self._create_task_config('generate_resume_task')
        
        return Task(
            description=task_config["description"],
            expected_output=task_config["expected_output"],
            agent=self.resume_writer(),
            context=[self.optimize_resume_task(), self.analyze_job_task(), self.research_company_task()],
            output_file='output/optimized_resume.md'
        )

    @task
    def generate_report_task(self) -> Task:
        task_config = self._create_task_config('generate_report_task')
        
        return Task(
            description=task_config["description"],
            expected_output=task_config["expected_output"],
            agent=self.report_generator(),
            context=[self.analyze_job_task(), self.optimize_resume_task(), self.research_company_task()],
            output_file='output/final_report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.resume_analyzer(),
                self.job_analyzer(),
                self.company_researcher(),
                self.resume_writer(),
                self.report_generator()
            ],
            tasks=[
                self.analyze_job_task(),
                self.optimize_resume_task(),
                self.research_company_task(),
                self.generate_resume_task(),
                self.generate_report_task()
            ],
            verbose=True,
            process=Process.sequential
        )