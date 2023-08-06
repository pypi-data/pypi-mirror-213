from typing import Dict, Type

from langplus.agents.agent import BaseSingleActionAgent
from langplus.agents.agent_types import AgentType
from langplus.agents.chat.base import ChatAgent
from langplus.agents.conversational.base import ConversationalAgent
from langplus.agents.conversational_chat.base import ConversationalChatAgent
from langplus.agents.mrkl.base import ZeroShotAgent
from langplus.agents.react.base import ReActDocstoreAgent
from langplus.agents.self_ask_with_search.base import SelfAskWithSearchAgent
from langplus.agents.structured_chat.base import StructuredChatAgent

AGENT_TO_CLASS: Dict[AgentType, Type[BaseSingleActionAgent]] = {
    AgentType.ZERO_SHOT_REACT_DESCRIPTION: ZeroShotAgent,
    AgentType.REACT_DOCSTORE: ReActDocstoreAgent,
    AgentType.SELF_ASK_WITH_SEARCH: SelfAskWithSearchAgent,
    AgentType.CONVERSATIONAL_REACT_DESCRIPTION: ConversationalAgent,
    AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION: ChatAgent,
    AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION: ConversationalChatAgent,
    AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION: StructuredChatAgent,
}
