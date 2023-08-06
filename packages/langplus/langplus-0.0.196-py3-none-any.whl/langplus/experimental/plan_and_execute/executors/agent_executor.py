from typing import List

from langplus.agents.agent import AgentExecutor
from langplus.agents.structured_chat.base import StructuredChatAgent
from langplus.base_language import BaseLanguageModel
from langplus.experimental.plan_and_execute.executors.base import ChainExecutor
from langplus.tools import BaseTool

HUMAN_MESSAGE_TEMPLATE = """Previous steps: {previous_steps}

Current objective: {current_step}

{agent_scratchpad}"""

TASK_PREFIX = """{objective}

"""


def load_agent_executor(
    llm: BaseLanguageModel,
    tools: List[BaseTool],
    verbose: bool = False,
    include_task_in_prompt: bool = False,
) -> ChainExecutor:
    input_variables = ["previous_steps", "current_step", "agent_scratchpad"]
    template = HUMAN_MESSAGE_TEMPLATE

    if include_task_in_prompt:
        input_variables.append("objective")
        template = TASK_PREFIX + template

    agent = StructuredChatAgent.from_llm_and_tools(
        llm,
        tools,
        human_message_template=template,
        input_variables=input_variables,
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=verbose
    )
    return ChainExecutor(chain=agent_executor)
