#!/usr/bin/env python
import sys
import os
import warnings
from pathlib import Path
from resume_crew.crew import ResumeCrew
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Silence SyntaxWarning from pysbd
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the resume optimization crew.
    """
    # Check if GEMINI_API_KEY is present
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please make sure your .env file is properly set up.")
        sys.exit(1)
        
    # Create output directory if it doesn't exist
    output_dir = Path(__file__).parent.parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    inputs = {
        'job_url': 'https://www.mckinsey.com/careers/search-jobs/jobs/associate-15178',
        'company_name': 'McKinsey & Co.'
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