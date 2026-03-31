import requests
import time
import os
from openai import OpenAI

# 1. Setup OpenAI (Meta's required Env Variables)
client = OpenAI(
    base_url=os.getenv("API_BASE_URL"), 
    api_key=os.getenv("OPENAI_API_KEY")
)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o")
BASE_URL = "http://127.0.0.1:8000"

def get_ai_command(obs_text):
    """The AI reads the 'text' field of the observation and decides the fix."""
    system_prompt = "You are a Cloud Support AI. Output ONLY the one linux command needed to fix the issue. No explanation."
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Server Status: {obs_text}"}
        ]
    )
    return response.choices[0].message.content.strip()

def run_evaluation():
    print("🚀 Starting Meta OpenEnv Evaluation...")
    
    # Reset to get the initial structured observation
    resp = requests.post(f"{BASE_URL}/reset").json()
    obs = resp['observation'] # This is now a Dict: {'text': '...', 'disk_usage': 98.5, ...}
    
    for i in range(5):
        # AI looks at the 'text' part of our new Observation model
        cmd = get_ai_command(obs['text'])
        print(f"\n🤖 Step {i+1} | AI Command: {cmd}")

        # Send structured Action
        step_resp = requests.post(f"{BASE_URL}/step", json={"command": cmd}).json()
        
        obs = step_resp['observation']
        reward = step_resp['reward']
        done = step_resp['done']

        print(f"📊 State: Disk {obs['disk_usage']}% | Port: {obs['port_80_status']}")
        print(f"🏆 Reward: {reward['score']} ({reward['reason']})")
        
        if done:
            print("\n✅ TASK SUCCESS: 1.0 Reward Achieved!")
            break
        time.sleep(1)

if __name__ == "__main__":
    run_evaluation()