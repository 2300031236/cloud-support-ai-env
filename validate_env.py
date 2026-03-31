import requests

BASE_URL = "http://127.0.0.1:8000"

def validate():
    print("🔍 Starting OpenEnv Compliance Check...")
    
    # 1. Test Reset
    print("\n[1/3] Testing /reset...")
    resp = requests.post(f"{BASE_URL}/reset").json()
    if "observation" in resp and "disk_usage" in resp["observation"]:
        print("✅ Reset returned structured Observation.")
    else:
        print("❌ Reset failed. Check your Observation model.")

    # 2. Test Step & Reward Shaping
    print("\n[2/3] Testing /step & Reward Logic...")
    action = {"command": "rm /var/log/syslog.old"}
    step_resp = requests.post(f"{BASE_URL}/step", json=action).json()
    
    reward = step_resp.get("reward", {})
    score = reward.get("score", 0.0)
    
    if score == 0.5:
        print(f"✅ Reward Shaping working! Score: {score}")
    else:
        print(f"❌ Reward Logic failed. Expected 0.5, got {score}")

    # 3. Test State Endpoint (Meta Requirement)
    print("\n[3/3] Testing /state...")
    state_resp = requests.get(f"{BASE_URL}/state")
    if state_resp.status_code == 200:
        print("✅ /state endpoint is LIVE.")
    else:
        print("❌ /state endpoint MISSING or BROKEN.")

if __name__ == "__main__":
    validate()