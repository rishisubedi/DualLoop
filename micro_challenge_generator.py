import json
import random
from datetime import datetime

def run_challenge_generator():
    print("MicroChallengeGenerator: Analyzing priority jobs for technical challenge framing...")
    
    try:
        with open("qualified_jobs.json", "r") as f:
             jobs = json.load(f)
             gold_jobs = [j for j in jobs if 'GOLD' in j.get('priority_label', '')]
    except:
        gold_jobs = []

    date_str = datetime.now().strftime("%d %B %Y - %H:%M")

    challenges = [
        # Challenge 1: Asyncio
        """### 1. Market Intel & Trends
* **The Demise of Pure Data Science:** Firms are no longer hiring pure predictive modeling data scientists at the graduate level. The roles have evolved into "FinTech AI Research Analyst".
* **Latency is King:** Financial institutions are migrating to WebSockets. The ability to manage non-blocking I/O in Python (`asyncio`) is now a baseline requirement.

### 💻 Coding Knowledge: Decoupling CPU-Heavy Tasks
**Mistake:** Running `model.predict()` directly inside an `async def` function blocks the loop.
**Gold Standard Solution:** Offload to `asyncio.to_thread`.
```python
import asyncio, time
def run_heavy_ai_inference(data):
    time.sleep(0.3)
    return {"sentiment": "BULLISH"}

async def process_market_tick(tick_data):
    result = await asyncio.to_thread(run_heavy_ai_inference, tick_data)
    print(f"Processed: {result}")
```
### ⚡ Your Daily Micro-Challenge
**Target:** FinTech AI Research Analyst
**The Task:** Write a Python decorator using `pydantic` that forcefully intercepts an LLM's output and triggers a fallback regex parser on failure before throwing a `ComplianceError`.""",

        # Challenge 2: LangGraph & Multi-Agent
        """### 1. Market Intel & Trends
* **Agentic Workflows over RAG:** Simple RAG is dead in tier-1 banking. 2027 demands **Multi-Agent orchestration** (LangGraph) with strict deterministic boundaries.
* **Audit Trails:** Regulators require explicit graph-state tracing for algorithmic transparency.

### 💻 Coding Knowledge: LangGraph State Management
When building Fan-Out/Fan-In architectures, you must ensure state is not mutated unpredictably.
**Gold Standard Solution:** Use `TypedDict` and explicit reducer functions for parallel agent merging.
```python
from typing import TypedDict, Annotated
import operator

class GraphState(TypedDict):
    # The 'operator.add' reducer ensures parallel agent responses append to the list
    risk_assessments: Annotated[list[str], operator.add]
    final_score: int
```
### ⚡ Your Daily Micro-Challenge
**Target:** Quantitative Analytics Associate
**The Task:** Architect a LangGraph node that receives a list of `risk_assessments` from 3 parallel LLM agents. If any agent flags "HIGH RISK", the node must instantly route the graph to a `human_review` node. Otherwise, it proceeds to `approve_credit`.""",

        # Challenge 3: XGBoost & Explainability
        """### 1. Market Intel & Trends
* **Explainable AI (XAI) is Law:** Due to the FCA Consumer Duty, black-box AI is banned for credit decisions. Models must be interpretable.
* **XGBoost Dominance:** Neural networks are often too opaque for tabular financial data; XGBoost paired with SHAP remains the Gold Standard for risk engines.

### 💻 Coding Knowledge: Fast SHAP Value Extraction
Generating SHAP values can bottleneck production APIs.
**Gold Standard Solution:** Use `TreeExplainer` and cache the explainer object at startup.
```python
import shap
import xgboost as xgb

model = xgb.Booster(model_file='risk_model.json')
# Initialize explainer ONCE during FastAPI startup, not per request
explainer = shap.TreeExplainer(model)

def get_explanation(features):
    shap_values = explainer.shap_values(features)
    return shap_values
```
### ⚡ Your Daily Micro-Challenge
**Target:** Analytics & Risk Full-Time Analyst
**The Task:** Write a FastAPI endpoint that receives a gig-worker's income profile, runs XGBoost inference, and returns both the risk score AND the top 3 contributing SHAP features in the JSON response.""",

        # Challenge 4: Pinecone & Advanced RAG
        """### 1. Market Intel & Trends
* **Domain-Specific RAG:** Financial firms are moving beyond generic OpenAI embeddings. They want fine-tuned vector spaces (Pinecone, Milvus) that understand the difference between 'interest rate swap' and 'interest rate cap'.
* **Hybrid Search:** Dense embeddings (semantic) + Sparse vectors (BM25 keyword search) are now standard for high-accuracy financial retrieval.

### 💻 Coding Knowledge: Pinecone Hybrid Search
Semantic search alone fails on exact ID lookups (like a CUSIP bond identifier).
**Gold Standard Solution:** Combine alpha weighting for hybrid queries.
```python
from pinecone import Pinecone

pc = Pinecone(api_key="your_key")
index = pc.Index("fintech-docs")

# Alpha=0.7 favors semantic, Alpha=0.3 favors strict keyword
results = index.query(
    vector=dense_embedding,
    sparse_vector=sparse_bm25_vector,
    top_k=5,
    alpha=0.7 
)
```
### ⚡ Your Daily Micro-Challenge
**Target:** AI & Data Graduate Programme
**The Task:** Design a Python class that chunks a 500-page PDF financial prospectus using `LangChain`, generates both dense and sparse vectors, and upserts them into a Pinecone index in parallel batches."""
    ]

    selected = random.choice(challenges)

    analysis_md = f"""# 🏆 Gold Standard Job Market Analysis & Prep
**Generated:** {date_str}

{selected}

*Run the generator again anytime to receive a fresh coding challenge!*
"""
    
    with open("daily_challenge.md", "w", encoding='utf-8') as f:
        f.write(analysis_md)
        
    print("MicroChallengeGenerator: Market Analysis and Challenge generated and saved to daily_challenge.md")

if __name__ == "__main__":
    run_challenge_generator()
