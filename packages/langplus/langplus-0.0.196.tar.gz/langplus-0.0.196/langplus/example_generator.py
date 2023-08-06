"""Utility functions for working with prompts."""
from typing import List

from langplus.base_language import BaseLanguageModel
from langplus.chains.llm import LLMChain
from langplus.prompts.few_shot import FewShotPromptTemplate
from langplus.prompts.prompt import PromptTemplate

TEST_GEN_TEMPLATE_SUFFIX = "Add another example."


def generate_example(
    examples: List[dict], llm: BaseLanguageModel, prompt_template: PromptTemplate
) -> str:
    """Return another example given a list of examples for a prompt."""
    prompt = FewShotPromptTemplate(
        examples=examples,
        suffix=TEST_GEN_TEMPLATE_SUFFIX,
        input_variables=[],
        example_prompt=prompt_template,
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.predict()
