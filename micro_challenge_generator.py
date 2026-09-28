import json

def run_challenge_generator():
    print("MicroChallengeGenerator: Analyzing priority jobs for technical challenge framing...")
    
    try:
        with open("qualified_jobs.json", "r") as f:
             jobs = json.load(f)
        target = jobs[0] # Targeting the TopTier Hedge Fund role
    except:
        target = {"title": "AI Quant Developer", "company": "Tier 1 Hedge Fund"}
    
    challenge_md = f"""# Daily Micro-Challenge 🧠

**Target Role:** {target['title']} at {target['company']}
**Time Limit:** 15 Minutes
**Focus Area:** High-Concurrency AI Inference & Streaming Data

### The Scenario:
You are designing the backend for a real-time trading engine. The engine ingests two data streams:
1. **L2 Order Book Data:** Very fast, high volume (requires sub-10ms processing).
2. **News Sentiment Analysis:** You are running a local LLM to gauge sentiment on breaking news. This inference takes ~300ms.

Currently, the system is designed synchronously. When a news article drops, the entire event loop blocks waiting for the LLM inference, causing the order book stream to buffer and miss critical micro-second arbitrage windows.

### The Challenge:
Leveraging your experience with `Python`, `asyncio`, and `FastAPI` (as seen in your APP Fraud Detection engine), how would you re-architect this pipeline?

**Required Deliverables:**
1. **Decoupling Strategy:** How do you prevent the 300ms LLM inference from blocking the sub-10ms order book processing in Python? 
2. **Handling Stale Data:** If the LLM sentiment arrives 300ms later, how do you reconcile it with the fast-moving order book data that has already changed?
"""
    
    with open("daily_challenge.md", "w", encoding='utf-8') as f:
        f.write(challenge_md)
        
    print("MicroChallengeGenerator: Challenge generated and saved to daily_challenge.md")

if __name__ == "__main__":
    run_challenge_generator()
