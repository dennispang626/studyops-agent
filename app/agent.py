"""ADK entry point for StudyOps Agent."""

from app.agents.studyops_agents import create_app, create_root_agent


root_agent = create_root_agent()
app = create_app(root_agent)
