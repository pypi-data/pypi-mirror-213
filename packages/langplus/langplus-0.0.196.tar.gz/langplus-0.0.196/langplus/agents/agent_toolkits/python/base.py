"""Python agent."""

from typing import Any, Dict, Optional

from langplus.agents.agent import AgentExecutor
from langplus.agents.agent_toolkits.python.prompt import PREFIX
from langplus.agents.mrkl.base import ZeroShotAgent
from langplus.base_language import BaseLanguageModel
from langplus.callbacks.base import BaseCallbackManager
from langplus.chains.llm import LLMChain
from langplus.tools.python.tool import PythonREPLTool


def create_python_agent(
    llm: BaseLanguageModel,
    tool: PythonREPLTool,
    callback_manager: Optional[BaseCallbackManager] = None,
    verbose: bool = False,
    prefix: str = PREFIX,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a python agent from an LLM and tool."""
    tools = [tool]
    prompt = ZeroShotAgent.create_prompt(tools, prefix=prefix)
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        callback_manager=callback_manager,
    )
    tool_names = [tool.name for tool in tools]
    agent = ZeroShotAgent(llm_chain=llm_chain, allowed_tools=tool_names, **kwargs)
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        **(agent_executor_kwargs or {}),
    )
