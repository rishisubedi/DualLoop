import json
import time

def run_agent1():
    print("Agent 1 [Sponsorship Qualifier]: Initializing semantic sponsorship filter...")
    time.sleep(1)
    
    # Mocking real-world scraped jobs for demonstration
    mock_jobs = [
        {
            "id": "JOB_001",
            "title": "Senior AI Engineer (FinTech)",
            "company": "QuantEdge Capital",
            "location": "London, UK",
            "description": "We are seeking an AI engineer with deep knowledge of Python, AWS, and RAG architectures. You will build financial risk models using LLMs and LangGraph. Visa sponsorship (Tier 2 Skilled Worker) is available for outstanding international candidates.",
            "required_skills": ["Python", "AWS", "RAG", "LangGraph", "Financial Risk"]
        },
        {
            "id": "JOB_002",
            "title": "Backend Python Developer",
            "company": "UK Retail Bank",
            "location": "Edinburgh, UK",
            "description": "Looking for a strong Python backend dev with FastAPI and SQL experience. Note: We are currently unable to provide skilled worker visa sponsorship for this role. Must have right to work in the UK.",
            "required_skills": ["Python", "FastAPI", "SQL"]
        },
        {
            "id": "JOB_003",
            "title": "Machine Learning Engineer (Fraud & AML)",
            "company": "Global Payments Ltd",
            "location": "London, UK",
            "description": "Join our anti-fraud team. Experience with XGBoost, Python, and AWS is required. We are a licensed UK visa sponsor and can offer full relocation assistance and Tier 2 sponsorship.",
            "required_skills": ["XGBoost", "Python", "AWS", "Fraud Detection"]
        },
        {
             "id": "JOB_004",
             "title": "AI Platform Engineer",
             "company": "HealthTech Startup",
             "location": "Remote, UK",
             "description": "Seeking an AI Platform engineer. Must be proficient in Kubernetes and GCP. Competitive salary. Immediate start.",
             "required_skills": ["Kubernetes", "GCP", "Python"]
        }
    ]
    
    print(f"Agent 1: Scraped {len(mock_jobs)} job postings. Analyzing for explicit sponsorship flags and skill overlap...\n")
    time.sleep(1)
    
    qualified_jobs = []
    
    for job in mock_jobs:
        desc = job['description'].lower()
        
        # 1. Sponsorship Guardrail
        if "unable to provide" in desc or "no sponsorship" in desc or "must have right to work" in desc:
            print(f"[-] {job['id']} | {job['company']} - {job['title']}")
            print("    Status: PRUNED_NO_SPONSORSHIP (Explicitly denied)")
            continue
            
        if "visa sponsorship" in desc or "tier 2" in desc or "licensed sponsor" in desc:
            sponsorship_flag = "EXPLICIT_SPONSORSHIP"
        else:
            print(f"[-] {job['id']} | {job['company']} - {job['title']}")
            print("    Status: PRUNED_AMBIGUOUS (No explicitly mentioned sponsorship. Saving compute.)")
            continue
            
        # 2. Skill Overlap Check (Baseline check vs User Stack)
        # Note: A real agent would use embedding similarity here. We simulate a fast keyword match.
        user_skills = {"python", "aws", "sql", "fastapi", "langgraph", "rag", "xgboost", "shap"}
        job_skills = {s.lower() for s in job['required_skills']}
        overlap = user_skills.intersection(job_skills)
        match_score = len(overlap) / len(job_skills) if job_skills else 0
        
        if match_score >= 0.5:
            print(f"[+] {job['id']} | {job['company']} - {job['title']}")
            print(f"    Status: QUALIFIED (Sponsorship: {sponsorship_flag} | Skill Match: {match_score*100:.0f}%)")
            qualified_jobs.append(job)
        else:
            print(f"[-] {job['id']} | {job['company']} - {job['title']}")
            print(f"    Status: PRUNED_LOW_SKILL_MATCH (Skill Match: {match_score*100:.0f}%)")
            
    # Update state
    try:
        with open("state.json", "r") as f:
            state = json.load(f)
            
        state["metrics"]["jobs_scraped"] += len(mock_jobs)
        state["metrics"]["jobs_qualified"] += len(qualified_jobs)
        
        with open("state.json", "w") as f:
            json.dump(state, f, indent=2)
            
        # Output qualified jobs
        with open("qualified_jobs.json", "w") as f:
            json.dump(qualified_jobs, f, indent=2)
            
        print(f"\nAgent 1: Run complete. {len(qualified_jobs)} jobs qualified. State metrics updated.")
        
    except Exception as e:
         print(f"Error updating state: {e}")

if __name__ == "__main__":
    run_agent1()
