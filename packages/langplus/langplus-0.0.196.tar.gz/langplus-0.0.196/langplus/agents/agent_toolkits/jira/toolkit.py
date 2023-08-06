"""Jira Toolkit."""
from typing import List

from langplus.agents.agent_toolkits.base import BaseToolkit
from langplus.tools import BaseTool
from langplus.tools.jira.tool import JiraAction
from langplus.utilities.jira import JiraAPIWrapper


class JiraToolkit(BaseToolkit):
    """Jira Toolkit."""

    tools: List[BaseTool] = []

    @classmethod
    def from_jira_api_wrapper(cls, jira_api_wrapper: JiraAPIWrapper) -> "JiraToolkit":
        actions = jira_api_wrapper.list()
        tools = [
            JiraAction(
                name=action["name"],
                description=action["description"],
                mode=action["mode"],
                api_wrapper=jira_api_wrapper,
            )
            for action in actions
        ]
        return cls(tools=tools)

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return self.tools
