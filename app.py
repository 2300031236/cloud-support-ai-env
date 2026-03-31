from fastapi import FastAPI
from environment import CloudSupportEnv
from models import Action

app = FastAPI()
env = CloudSupportEnv()

@app.get("/")
def health():
    return {"status": "OpenEnv Cloud Environment Active"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs.model_dump()} # MUST be model_dump() or .dict()
    
@app.post("/step")
def step_endpoint(action: Action):
    obs, reward, done, info = env.step(action.command)
    
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info
    }

@app.get("/state")
def get_state():
    return {
        "disk_usage": env.disk_usage,
        "port_80_open": env.port_80_open,
        "logs_cleared": env.logs_cleared
    }