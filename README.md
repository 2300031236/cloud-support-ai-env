# Cloud Support AI Environment
An OpenEnv-compliant environment for training AI agents to perform autonomous cloud triage.

### Tasks:
1. **Storage Triage (Easy):** Clear full disks.
2. **Network Triage (Medium):** Open firewall ports.
3. **Full System Repair (Hard):** Combined troubleshooting.

### Setup:
`pip install .`
`uvicorn server.app:app --port 8000`