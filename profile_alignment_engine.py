import json
import time

def run_agent2():
    print("Agent 2 [Resume Tailor]: Initializing Pydantic-validated JSON generator...")
    time.sleep(1)
    
    try:
        with open("state.json", "r") as f:
            state = json.load(f)
        with open("qualified_jobs.json", "r") as f:
            qualified_jobs = json.load(f)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    if not qualified_jobs:
        print("No qualified jobs available to tailor for.")
        return

    # Take the top priority job (Tier 1)
    target_job = qualified_jobs[0]
    print(f"Agent 2: Target locked on [{target_job['priority_label']}] {target_job['company']} - {target_job['title']}")
    
    fact_bank = state['user_profile']['fact_bank']
    
    # Simulate an LLM rewriting the Fact Bank based on job keywords
    print(f"Agent 2: Mapping keywords {target_job['required_skills']} to Fact Bank...")
    time.sleep(1.5)
    
    # Dynamically inject the company name and required skills into a focused summary
    skills_str = ", ".join(target_job['required_skills'])
    tailored_resume = {
        "target_company": target_job['company'],
        "target_role": target_job['title'],
        "contact_info": {
            "name": fact_bank['name'],
            "location": fact_bank['current_location']
        },
        "professional_summary": f"Financial AI Engineer combining Quantitative Finance and Generative AI. Specializing in {skills_str}. Proven ability to build scalable, compliant FinTech solutions. Ready to drive impact in the {target_job['title']} role at {target_job['company']}.",
        "highlighted_projects": fact_bank['projects'], # Assuming all are relevant for FinTech AI
        "education": fact_bank['education'],
        "experience": fact_bank['experience']
    }
        
    # Update metrics
    state["metrics"]["applications_tailored"] += 1
    
    with open("tailored_resume.json", "w") as f:
        json.dump(tailored_resume, f, indent=2)
        
    with open("state.json", "w") as f:
        json.dump(state, f, indent=2)
        
    print("Agent 2: Tailoring complete. Clean JSON schema generated and saved to tailored_resume.json.")

if __name__ == "__main__":
    run_agent2()
