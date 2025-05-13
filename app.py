import streamlit as st
import os
import sys
import json
import tempfile
import shutil
import re
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(current_dir)

# Import crew after adding to path
from src.resume_crew.crew import ResumeCrew

# Load environment variables
load_dotenv()

# Create output directory if it doesn't exist
output_dir = Path(current_dir) / "output"
output_dir.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Resume Optimization Crew",
    page_icon="📝",
    layout="wide"
)

def extract_json_from_content(content):
    """Extract JSON content from LLM response that might contain markdown codeblocks"""
    # Try to extract JSON from markdown code blocks
    json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
    matches = re.findall(json_pattern, content)
    
    if matches:
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue
    
    # If no valid JSON in code blocks, try parsing the whole content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # As a last resort, try to clean the content
        # Remove any non-JSON content at beginning/end
        clean_content = re.sub(r'^[^{]*', '', content)
        clean_content = re.sub(r'[^}]*$', '', clean_content)
        try:
            return json.loads(clean_content)
        except json.JSONDecodeError:
            return None

def display_markdown_file(file_path):
    """Display markdown file content"""
    try:
        if not os.path.exists(file_path):
            st.warning(f"File not found: {file_path}")
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            st.markdown(content)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.error(f"File path: {file_path}")

def display_json_file(file_path, title):
    """Display JSON file content in an expandable section"""
    try:
        if not os.path.exists(file_path):
            st.warning(f"File not found: {file_path}")
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            try:
                # Try standard JSON parsing first
                data = json.loads(content)
                with st.expander(title):
                    st.json(data)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from LLM response
                data = extract_json_from_content(content)
                if data:
                    with st.expander(title):
                        st.json(data)
                else:
                    with st.expander(title):
                        st.error("Invalid JSON format in the file")
                        st.text(content[:500] + "..." if len(content) > 500 else content)
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
        st.error(f"File path: {file_path}")

def process_json_output(file_path):
    """Process JSON output files to ensure valid JSON"""
    try:
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to extract valid JSON
        data = extract_json_from_content(content)
        
        if data:
            # Write back valid JSON
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        return False
    except Exception as e:
        print(f"Error processing JSON file {file_path}: {e}")
        return False

def format_cover_letter_from_json(data):
    """Format cover letter JSON into a readable markdown text with improved error handling"""
    if not data or not isinstance(data, dict):
        return "No cover letter data found."

    try:
        letter = ""

        # Header
        if data.get('name'):
            letter += f"**{data['name']}**  \n"
        if data.get('address'):
            letter += f"{data['address']}  \n"
        contact = []
        if data.get('email'):
            contact.append(data['email'])
        if data.get('phone'):
            contact.append(data['phone'])
        if contact:
            letter += " | ".join(contact) + "\n\n"

        # Company info and date
        if data.get('company_contact'):
            letter += f"{data['company_contact']}\n"
        if data.get('company_name'):
            letter += f"{data['company_name']}\n"
        if data.get('company_address'):
            letter += f"{data['company_address']}\n\n"
        if data.get('date'):
            letter += f"Written in [Your City], on {data['date']}\n\n"

        # Subject
        if data.get('subject'):
            letter += f"**Subject:** {data['subject']}\n\n"

        # Body
        letter += "Dear Sir or Madam,\n\n"
        if data.get('opening_paragraph'):
            letter += data['opening_paragraph'].strip() + "\n\n"
        for para in data.get('experience_paragraphs', []):
            letter += para.strip() + "\n\n"
        if data.get('company_alignment_paragraph'):
            letter += data['company_alignment_paragraph'].strip() + "\n\n"
        if data.get('closing_paragraph'):
            letter += data['closing_paragraph'].strip() + "\n\n"

        letter += "Yours sincerely,\n"
        letter += f"{data['name']}"

        return letter.strip()

    except Exception as e:
        return f"Error formatting letter: {e}"

def run_resume_crew(resume_path, job_url, company_name):
    """Run the resume optimization crew process"""
    # Create output directory if it doesn't exist
    output_dir = Path(current_dir) / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Create a knowledge directory if it doesn't exist
    knowledge_dir = Path(current_dir) / "knowledge"
    knowledge_dir.mkdir(exist_ok=True)
    
    # Copy the resume to the knowledge directory with a fixed name
    resume_filename = "current_resume.pdf"
    resume_knowledge_path = knowledge_dir / resume_filename
    
    try:
        shutil.copy2(resume_path, resume_knowledge_path)
        st.info(f"Resume copied to knowledge directory: {resume_knowledge_path}")
    except Exception as e:
        st.error(f"Error copying resume: {str(e)}")
        return False
    
    # Create a ResumeCrew instance with the uploaded resume
    resume_crew = ResumeCrew()
    # Update the resume path
    resume_crew.resume_path = str(resume_knowledge_path)
    
    # Run the crew with the provided inputs
    inputs = {
        'job_url': job_url,
        'company_name': company_name,
        'resume_path': str(resume_knowledge_path)
    }
    
    with st.spinner("Processing your resume... This might take a few minutes"):
        try:
            # Define output file paths
            job_analysis_path = output_dir / "job_analysis.json"
            resume_optimization_path = output_dir / "resume_optimization.json"
            company_research_path = output_dir / "company_research.json"
            optimized_resume_path = output_dir / "optimized_resume.md"
            final_report_path = output_dir / "final_report.md"
            cover_letter_path = output_dir / "cover_letter.json"
            
            # Run the crew
            resume_crew.crew().kickoff(inputs=inputs)
            
            # Process JSON outputs to ensure valid JSON
            json_files = [job_analysis_path, resume_optimization_path, company_research_path, cover_letter_path]
            for file_path in json_files:
                process_json_output(file_path)
            
            # Verify outputs exist
            output_files = [job_analysis_path, resume_optimization_path, company_research_path, 
                            optimized_resume_path, final_report_path, cover_letter_path]
            missing_files = [f for f in output_files if not f.exists()]
            
            if missing_files:
                st.warning(f"Some output files are missing: {[f.name for f in missing_files]}")
            
            st.success("Resume optimization completed successfully!")
            return True
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return False

def main():
    st.title("Resume Optimization Crew")
    st.write("Upload your resume, enter a job URL, and company name to optimize your resume.")
    
    # Check for API keys
    if not os.getenv("GEMINI_API_KEY"):
        st.error("Error: GEMINI_API_KEY not found in environment variables.")
        st.info("Please add your Gemini API key to the .env file.")
        return
    
    # File uploader for resume
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    
    job_url = st.text_input("Job URL", placeholder="https://example.com/jobs/position")
    company_name = st.text_input("Company Name", placeholder="Company Inc.")
    
    submit_button = st.button("Optimize Resume")
    
    if submit_button and uploaded_file and job_url and company_name:
        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            resume_path = Path(tmp_file.name)
        
        # Run the resume crew
        success = run_resume_crew(resume_path, job_url, company_name)
        
        # Clean up the temporary file after copying
        try:
            os.unlink(resume_path)
        except Exception as e:
            st.warning(f"Could not remove temporary file: {e}")
            
        if success:
            # Create paths for output files
            optimized_resume_path = os.path.join(current_dir, "output", "optimized_resume.md")
            final_report_path = os.path.join(current_dir, "output", "final_report.md")
            job_analysis_path = os.path.join(current_dir, "output", "job_analysis.json")
            resume_optimization_path = os.path.join(current_dir, "output", "resume_optimization.json")
            company_research_path = os.path.join(current_dir, "output", "company_research.json")
            cover_letter_path = os.path.join(current_dir, "output", "cover_letter.json")
            
            # Display the results
            st.header("Results")
            
            # Display tabs for different results
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                "Optimized Resume", 
                "Final Report", 
                "Job Analysis", 
                "Resume Optimization", 
                "Company Research",
                "Cover Letter"
            ])
            
            with tab1:
                display_markdown_file(optimized_resume_path)
            
            with tab2:
                display_markdown_file(final_report_path)
            
            with tab3:
                display_json_file(job_analysis_path, "Job Analysis Details")
            
            with tab4:
                display_json_file(resume_optimization_path, "Resume Optimization Details")
            
            with tab5:
                display_json_file(company_research_path, "Company Research Details")
            
            with tab6:
                # Cover Letter Display
                try:
                    if os.path.exists(cover_letter_path):
                        with open(cover_letter_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            cover_letter_data = extract_json_from_content(content)
                            if cover_letter_data:
                                # Format and display cover letter
                                cover_letter_text = format_cover_letter_from_json(cover_letter_data)
                                st.markdown(cover_letter_text)
                                
                                # Add a text area for editing
                                edited_cover_letter = st.text_area(
                                    "Edit your cover letter", 
                                    value=cover_letter_text,
                                    height=600
                                )
                                
                                # Add download button for edited version
                                st.download_button(
                                    label="Download Edited Cover Letter",
                                    data=edited_cover_letter,
                                    file_name="edited_cover_letter.md",
                                    mime="text/markdown"
                                )
                            else:
                                st.warning("Unable to extract cover letter data.")
                    else:
                        st.warning("Cover letter file not found.")
                except Exception as e:
                    st.error(f"Error reading cover letter: {e}")
            
            # Add download buttons for the results
            st.subheader("Download Results")
            col1, col2 = st.columns(2)
            
            try:
                # First column of download buttons
                with col1:
                    if os.path.exists(optimized_resume_path):
                        with open(optimized_resume_path, "r", encoding="utf-8") as f:
                            st.download_button(
                                label="Download Optimized Resume",
                                data=f.read(),
                                file_name="optimized_resume.md",
                                mime="text/markdown"
                            )
                    else:
                        st.warning("Optimized resume file not found")
                    
                    if os.path.exists(job_analysis_path):
                        with open(job_analysis_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Process JSON if needed for download
                            try:
                                json_data = json.loads(content)
                                formatted_json = json.dumps(json_data, indent=2)
                                st.download_button(
                                    label="Download Job Analysis",
                                    data=formatted_json,
                                    file_name="job_analysis.json",
                                    mime="application/json"
                                )
                            except:
                                data = extract_json_from_content(content)
                                if data:
                                    formatted_json = json.dumps(data, indent=2)
                                    st.download_button(
                                        label="Download Job Analysis",
                                        data=formatted_json,
                                        file_name="job_analysis.json",
                                        mime="application/json"
                                    )
                                else:
                                    st.warning("Invalid JSON format in job analysis file")
                    else:
                        st.warning("Job analysis file not found")
                
                # Second column of download buttons
                with col2:
                    if os.path.exists(final_report_path):
                        with open(final_report_path, "r", encoding="utf-8") as f:
                            st.download_button(
                                label="Download Final Report",
                                data=f.read(),
                                file_name="final_report.md",
                                mime="text/markdown"
                            )
                    else:
                        st.warning("Final report file not found")
                    
                    if os.path.exists(company_research_path):
                        with open(company_research_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # Process JSON if needed for download
                            try:
                                json_data = json.loads(content)
                                formatted_json = json.dumps(json_data, indent=2)
                                st.download_button(
                                    label="Download Company Research",
                                    data=formatted_json,
                                    file_name="company_research.json",
                                    mime="application/json"
                                )
                            except:
                                data = extract_json_from_content(content)
                                if data:
                                    formatted_json = json.dumps(data, indent=2)
                                    st.download_button(
                                        label="Download Company Research",
                                        data=formatted_json,
                                        file_name="company_research.json",
                                        mime="application/json"
                                    )
                                else:
                                    st.warning("Invalid JSON format in company research file")
                    else:
                        st.warning("Company research file not found")

                    # Add download button for Cover Letter
                    if os.path.exists(cover_letter_path):
                        try:
                            with open(cover_letter_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                cover_letter_data = extract_json_from_content(content)
                                if cover_letter_data:
                                    # Convert cover letter JSON to markdown for download
                                    cover_letter_markdown = format_cover_letter_from_json(cover_letter_data)
                                    st.download_button(
                                        label="Download Cover Letter",
                                        data=cover_letter_markdown,
                                        file_name="cover_letter.md",
                                        mime="text/markdown"
                                    )
                                else:
                                    st.warning("Invalid cover letter data")
                        except Exception as e:
                            st.error(f"Error processing cover letter: {e}")
                    else:
                        st.warning("Cover letter file not found")

            except Exception as e:
                st.error(f"Error with download buttons: {e}")
                import traceback
                st.error(traceback.format_exc())
    elif submit_button:
        if not uploaded_file:
            st.error("Please upload your resume.")
        if not job_url:
            st.error("Please enter a job URL.")
        if not company_name:
            st.error("Please enter a company name.")

if __name__ == "__main__":
    main()