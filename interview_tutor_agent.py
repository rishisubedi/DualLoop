import os
import time

def run_interview_tutor():
    print("==================================================")
    print(" StrictInterviewSim / Tutor Agent (Local CLI)     ")
    print("==================================================")
    
    # Ensure a challenge exists
    if not os.path.exists("daily_challenge.md"):
        print("Error: daily_challenge.md not found. Run MicroChallengeGenerator first.")
        return
        
    with open("daily_challenge.md", "r", encoding="utf-8") as f:
        challenge = f.read()
        
    print("\n" + challenge)
    print("==================================================")
    print("This agent is running entirely on your local machine.")
    print("Type your answer below. If you need a hint, type 'stuck'.")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("\nYour Answer (or 'stuck'): ").strip()
        except KeyboardInterrupt:
            break
            
        if user_input.lower() == 'exit':
            print("Interview ended. Keep practicing!")
            break
            
        elif user_input.lower() in ['stuck', 'hint', 'help']:
            print("\n💡 [Tutor Recommendation]:")
            print("1. Decoupling: Python's `asyncio` event loop gets blocked by heavy compute (like LLM inference). Look into offloading that work using `asyncio.to_thread()` or a `concurrent.futures.ProcessPoolExecutor`.")
            print("2. Stale Data: Think about Event Sourcing or timestamping. If you capture the exact timestamp of the L2 book when the news arrives, you can reconcile it later.")
            
        elif len(user_input) < 15:
            print("\n⚠️ [Feedback]: That answer is too brief for a Senior/Quant role. Try to elaborate on specific Python modules or architectural patterns.")
            
        else:
            print("\n⚙️ [Evaluation Engine]: Analyzing your architectural response...")
            time.sleep(1.5)
            
            # Simulated heuristic evaluation (In a real setup, this would ping a local LLM via Ollama)
            user_lower = user_input.lower()
            good_keywords = ["thread", "process", "queue", "kafka", "redis", "celery", "to_thread", "executor"]
            
            if any(kw in user_lower for kw in good_keywords):
                print("✅ [Result]: STRONG. You successfully identified asynchronous decoupling mechanics. Offloading the 300ms inference ensures the sub-10ms L2 order book loop remains unblocked.")
                print("📌 [Next Step]: Consider how you would scale this across multiple Kubernetes pods.")
            else:
                print("⚠️ [Result]: PARTIAL. Your logic makes sense, but you need to explicitly name the Python concurrency models (e.g., Task queues, ThreadPool, or ProcessPool) to pass a strict engineering screen.")
                print("💡 [Suggestion]: Type 'stuck' to see the recommended approach.")
                
if __name__ == "__main__":
    run_interview_tutor()
