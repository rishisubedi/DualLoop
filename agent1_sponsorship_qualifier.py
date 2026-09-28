import json
import time

def determine_priority(company, description, title):
    full_text = f"{company} {description} {title}".lower()
    
    # Tier 1: FinTech & Banks
    fintech_keywords = ["bank", "fintech", "capital", "quant", "hedge fund", "finance", "payment", "trading"]
    if any(kw in full_text for kw in fintech_keywords):
        return 1, "Tier 1 (FinTech/Bank)"
        
    # Tier 2: Pure Tech
    tech_keywords = ["ai", "tech", "software", "platform", "cloud", "startup", "data"]
    if any(kw in full_text for kw in tech_keywords):
        return 2, "Tier 2 (Pure Tech)"
        
    # Tier 3: General
    return 3, "Tier 3 (General)"

def run_agent1():
    print("Agent 1 [Sponsorship Qualifier]: Initializing semantic filter...")
    time.sleep(1)
    
    # Note: In a production environment, this mock data array would be replaced 
    # with a call to a live job board API (e.g., Adzuna, Reed, or a RapidAPI job scraper).
    # Direct HTML scraping of LinkedIn/Indeed from a local cron job often gets IP blocked.
    mock_jobs = [
        {
            "id": "JOB_001",
            "title": "Senior AI Engineer",
            "company": "QuantEdge Capital",
            "location": "London, UK",
            "description": "Building financial risk models. Visa sponsorship available.",
            "required_skills": ["Python", "AWS", "RAG", "Financial Risk"]
        },
        {
             "id": "JOB_005",
             "title": "AI Quant Developer - Graduate Scheme (Sept 2027)",
             "company": "TopTier Hedge Fund",
             "location": "London, UK",
             "description": "Our September 2027 Graduate Scheme is open. Full visa sponsorship.",
             "required_skills": ["Python", "SQL", "AI Modeling"]
        },
        {
             "id": "JOB_006",
             "title": "Machine Learning Engineer",
             "company": "DeepMind Startup",
             "location": "London, UK",
             "description": "Pure AI research platform. Licensed sponsor.",
             "required_skills": ["Python", "AWS", "XGBoost"]
        },
        {
             "id": "JOB_007",
             "title": "Data Scientist",
             "company": "UK Supermarket Retail",
             "location": "London, UK",
             "description": "General retail analytics. Tier 2 sponsorship offered.",
             "required_skills": ["Python", "SQL"]
        }
    ]
    
    qualified_jobs = []
    
    for job in mock_jobs:
        desc = job['description'].lower()
        title = job['title'].lower()
        full_text = desc + " " + title
        
        # 1. Negative Guardrail
        if "unable to provide" in desc or "no sponsorship" in desc or "must have right to work" in desc:
            continue
            
        # 2. Positive Identification
        is_sponsored = "visa sponsorship" in full_text or "tier 2" in full_text or "licensed sponsor" in full_text
        is_grad_scheme = "graduate scheme" in full_text or "graduate program" in full_text
        is_2027 = "2027" in full_text
        
        if not (is_sponsored or (is_grad_scheme and is_2027)):
            continue
            
        # 3. Skill Overlap Check
        user_skills = {"python", "aws", "sql", "fastapi", "langgraph", "rag", "xgboost", "shap", "ai modeling"}
        job_skills = {s.lower() for s in job['required_skills']}
        overlap = user_skills.intersection(job_skills)
        match_score = len(overlap) / len(job_skills) if job_skills else 0
        
        if match_score >= 0.5:
            # 4. Apply Prioritization
            priority_level, priority_label = determine_priority(job['company'], job['description'], job['title'])
            
            job['priority_level'] = priority_level
            job['priority_label'] = priority_label
            job['match_score'] = match_score
            qualified_jobs.append(job)

    # Sort by Priority (1 is highest) then by Skill Match (Descending)
    qualified_jobs.sort(key=lambda x: (x['priority_level'], -x['match_score']))
    
    print(f"Agent 1: Prioritized Qualified Roles:\n")
    for j in qualified_jobs:
        print(f"[{j['priority_label']}] {j['company']} - {j['title']} (Skill Match: {j['match_score']*100:.0f}%)")

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
            
    except Exception as e:
         print(f"Error updating state: {e}")

if __name__ == "__main__":
    run_agent1()
