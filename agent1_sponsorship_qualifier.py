import json
import time

def run_agent1():
    print("Agent 1 [Sponsorship Qualifier]: Initializing semantic filter (Sponsorship & 2027 Grad Schemes)...")
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
             "id": "JOB_005",
             "title": "AI Quant Developer - Graduate Scheme (Sept 2027)",
             "company": "TopTier Hedge Fund",
             "location": "London, UK",
             "description": "Our September 2027 Graduate Scheme is now open for applications. Seeking exceptional talent with Python, SQL, and AI modeling skills. We provide full visa sponsorship for our international graduate cohort.",
             "required_skills": ["Python", "SQL", "AI Modeling"]
        }
    ]
    
    print(f"Agent 1: Scraped {len(mock_jobs)} job postings. Analyzing for explicit sponsorship flags, 2027 Grad Schemes, and skill overlap...\n")
    time.sleep(1)
    
    qualified_jobs = []
    
    for job in mock_jobs:
        desc = job['description'].lower()
        title = job['title'].lower()
        full_text = desc + " " + title
        
        # 1. Negative Guardrail
        if "unable to provide" in desc or "no sponsorship" in desc or "must have right to work" in desc:
            print(f"[-] {job['id']} | {job['company']} - {job['title']}")
            print("    Status: PRUNED_NO_SPONSORSHIP (Explicitly denied)")
            continue
            
        # 2. Positive Identification (Sponsorship or 2027 Grad Scheme)
        is_sponsored = "visa sponsorship" in full_text or "tier 2" in full_text or "licensed sponsor" in full_text
        is_grad_scheme = "graduate scheme" in full_text or "graduate program" in full_text
        is_2027 = "2027" in full_text
        
        if is_sponsored and is_grad_scheme and is_2027:
            sponsorship_flag = "GRAD_SCHEME_2027_WITH_SPONSORSHIP"
        elif is_grad_scheme and is_2027:
             sponsorship_flag = "GRAD_SCHEME_2027_ASSUMED_SPONSOR" # Many top grad schemes sponsor, worth keeping
        elif is_sponsored:
            sponsorship_flag = "EXPLICIT_SPONSORSHIP"
        else:
            print(f"[-] {job['id']} | {job['company']} - {job['title']}")
            print("    Status: PRUNED_AMBIGUOUS (No explicit sponsorship or 2027 grad scheme identified.)")
            continue
            
        # 3. Skill Overlap Check
        user_skills = {"python", "aws", "sql", "fastapi", "langgraph", "rag", "xgboost", "shap", "ai modeling"}
        job_skills = {s.lower() for s in job['required_skills']}
        overlap = user_skills.intersection(job_skills)
        match_score = len(overlap) / len(job_skills) if job_skills else 0
        
        if match_score >= 0.5:
            print(f"[+] {job['id']} | {job['company']} - {job['title']}")
            print(f"    Status: QUALIFIED (Category: {sponsorship_flag} | Skill Match: {match_score*100:.0f}%)")
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
            
        with open("qualified_jobs.json", "w") as f:
            json.dump(qualified_jobs, f, indent=2)
            
        print(f"\nAgent 1: Run complete. {len(qualified_jobs)} jobs qualified. State metrics updated.")
        
    except Exception as e:
         print(f"Error updating state: {e}")

if __name__ == "__main__":
    run_agent1()
