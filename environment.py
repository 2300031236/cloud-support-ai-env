import time
from models import Observation, Reward

class CloudSupportEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.disk_usage = 98.5 
        self.port_80_open = False
        self.logs_cleared = False
        return self._get_observation()

    def _get_observation(self):
        status_msg = f"ALERT: Disk at {self.disk_usage}%. Port 80: {'OPEN' if self.port_80_open else 'CLOSED'}."
        return Observation(
            text=status_msg,
            disk_usage=self.disk_usage,
            port_80_status="OPEN" if self.port_80_open else "CLOSED"
        )

    def step(self, command: str):
        cmd = command.lower().strip()
        
        # Simulation Logic
        if "rm" in cmd and "/var/log" in cmd:
            self.disk_usage = 35.0
            self.logs_cleared = True
            
        if "ufw allow 80" in cmd:
            self.port_80_open = True

        # Reward Grader
        score = 0.0
        if self.logs_cleared: score += 0.5
        if self.port_80_open: score += 0.5
        
        done = (score >= 1.0)
        reward_obj = Reward(score=score, reason=f"System {int(score*100)}% recovered.")
        
        return self._get_observation(), reward_obj, done, {}