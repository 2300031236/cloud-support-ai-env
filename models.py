from pydantic import BaseModel, Field
from typing import Dict, Any

class Action(BaseModel):
    command: str = Field(description="The shell command to run in the terminal.")

class Observation(BaseModel):
    text: str = Field(description="The terminal output/system status.")
    disk_usage: float = Field(description="Current disk usage percentage.")
    port_80_status: str = Field(description="Status of the web port (OPEN/CLOSED).")

class Reward(BaseModel):
    score: float = Field(ge=0.0, le=1.0, description="The programmatic score for this step.")
    reason: str = Field(description="Explanation of the reward given.")

class State(BaseModel):
    internal_variables: Dict[str, Any]