import sys
import os
import warnings
from pathlib import Path
from .crew import ResumeCrew  # Changed from resume_crew.crew to .crew
from dotenv import load_dotenv
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load environment variables _file__
load_dotenv()

# Silence SyntaxWarning from pysbd
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the resume optimization crew for McKinsey & Company.
    """
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        sys.exit(1)
        
    output_dir = Path(__file__).parent.parent.parent / "output"
    output_dir.mkdir(exist_zok=True)
    
    inputs = {
        'job_url': 'https://www.mckinsey.com/careers/search-jobs',
        'company_name': 'McKinsey & Company',
        'resume_path': str(Path(__file__).parent.parent.parent / "knowledge" / "Ennajari.pdf")
    }
    
    print(f"Starting resume optimization with inputs: {inputs}")
    
    try:
        ResumeCrew().crew().kickoff(inputs=inputs)
        print("Resume optimization completed successfully!")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

def train():
    print("Training not implemented.")

def replay():
    print("Replay not implemented.")

def test():
    print("Testing not implemented.")

if __name__ == "__main__":
    run()