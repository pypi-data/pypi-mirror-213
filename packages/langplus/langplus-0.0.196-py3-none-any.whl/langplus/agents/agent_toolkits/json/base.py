"""Json agent."""
from typing import Any, Dict, List, Optional

from langplus.agents.agent import AgentExecutor
from langplus.agents.agent_toolkits.json.prompt import JSON_PREFIX, JSON_SUFFIX
from langplus.agents.agent_toolkits.json.toolkit import JsonToolkit
from langplus.agents.mrkl.base import ZeroShotAgent
from langplus.agents.mrkl.prompt import FORMAT_INSTRUCTIONS
from langplus.base_language import BaseLanguageModel
from langplus.callbacks.base import BaseCallbackManager
from langplus.chains.llm import LLMChain


def create_json_agent(
    llm: BaseLanguageModel,
    toolkit: JsonToolkit,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = JSON_PREFIX,
    suffix: str = JSON_SUFFIX,
    format_instructions: str = FORMAT_INSTRUCTIONS,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a json agent from an LLM and tools."""
    tools = toolkit.get_tools()
    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        format_instructions=format_instructions,
        input_variables=input_variables,
    )
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
