"""LLM Chain specifically for generating examples for question answering."""
from __future__ import annotations

from typing import Any

from langplus.base_language import BaseLanguageModel
from langplus.chains.llm import LLMChain
from langplus.evaluation.qa.generate_prompt import PROMPT


class QAGenerateChain(LLMChain):
    """LLM Chain specifically for generating examples for question answering."""

    @classmethod
    def from_llm(cls, llm: BaseLanguageModel, **kwargs: Any) -> QAGenerateChain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT, **kwargs)
