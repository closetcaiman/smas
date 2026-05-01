from pydantic import BaseModel

from .behaviours import AgentBehaviourConfig


class BehaviourConfig(BaseModel):
    """Configuration for the simulation behaviour component of the application."""

    agent: AgentBehaviourConfig = AgentBehaviourConfig()
