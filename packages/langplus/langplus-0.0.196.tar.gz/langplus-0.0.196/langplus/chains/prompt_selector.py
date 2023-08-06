from abc import ABC, abstractmethod
from typing import Callable, List, Tuple

from pydantic import BaseModel, Field

from langplus.base_language import BaseLanguageModel
from langplus.chat_models.base import BaseChatModel
from langplus.llms.base import BaseLLM
from langplus.prompts.base import BasePromptTemplate


class BasePromptSelector(BaseModel, ABC):
    @abstractmethod
    def get_prompt(self, llm: BaseLanguageModel) -> BasePromptTemplate:
        """Get default prompt for a language model."""


class ConditionalPromptSelector(BasePromptSelector):
    """Prompt collection that goes through conditionals."""

    default_prompt: BasePromptTemplate
    conditionals: List[
        Tuple[Callable[[BaseLanguageModel], bool], BasePromptTemplate]
    ] = Field(default_factory=list)

    def get_prompt(self, llm: BaseLanguageModel) -> BasePromptTemplate:
        for condition, prompt in self.conditionals:
            if condition(llm):
                return prompt
        return self.default_prompt


def is_llm(llm: BaseLanguageModel) -> bool:
    return isinstance(llm, BaseLLM)


def is_chat_model(llm: BaseLanguageModel) -> bool:
    return isinstance(llm, BaseChatModel)
