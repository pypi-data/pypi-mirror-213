"""Wrappers on top of large language models APIs."""
from typing import Dict, Type

from langplus.llms.ai21 import AI21
from langplus.llms.aleph_alpha import AlephAlpha
from langplus.llms.anthropic import Anthropic
from langplus.llms.anyscale import Anyscale
from langplus.llms.aviary import Aviary
from langplus.llms.bananadev import Banana
from langplus.llms.base import BaseLLM
from langplus.llms.baseten import Baseten
from langplus.llms.beam import Beam
from langplus.llms.bedrock import Bedrock
from langplus.llms.cerebriumai import CerebriumAI
from langplus.llms.cohere import Cohere
from langplus.llms.ctransformers import CTransformers
from langplus.llms.databricks import Databricks
from langplus.llms.deepinfra import DeepInfra
from langplus.llms.fake import FakeListLLM
from langplus.llms.forefrontai import ForefrontAI
from langplus.llms.google_palm import GooglePalm
from langplus.llms.gooseai import GooseAI
from langplus.llms.gpt4all import GPT4All
from langplus.llms.huggingface_endpoint import HuggingFaceEndpoint
from langplus.llms.huggingface_hub import HuggingFaceHub
from langplus.llms.huggingface_pipeline import HuggingFacePipeline
from langplus.llms.huggingface_text_gen_inference import HuggingFaceTextGenInference
from langplus.llms.human import HumanInputLLM
from langplus.llms.llamacpp import LlamaCpp
from langplus.llms.modal import Modal
from langplus.llms.mosaicml import MosaicML
from langplus.llms.nlpcloud import NLPCloud
from langplus.llms.openai import AzureOpenAI, OpenAI, OpenAIChat
from langplus.llms.openlm import OpenLM
from langplus.llms.petals import Petals
from langplus.llms.pipelineai import PipelineAI
from langplus.llms.predictionguard import PredictionGuard
from langplus.llms.promptlayer_openai import PromptLayerOpenAI, PromptLayerOpenAIChat
from langplus.llms.replicate import Replicate
from langplus.llms.rwkv import RWKV
from langplus.llms.sagemaker_endpoint import SagemakerEndpoint
from langplus.llms.self_hosted import SelfHostedPipeline
from langplus.llms.self_hosted_hugging_face import SelfHostedHuggingFaceLLM
from langplus.llms.stochasticai import StochasticAI
from langplus.llms.vertexai import VertexAI
from langplus.llms.writer import Writer

__all__ = [
    "Anthropic",
    "AlephAlpha",
    "Anyscale",
    "Aviary",
    "Banana",
    "Baseten",
    "Beam",
    "Bedrock",
    "CerebriumAI",
    "Cohere",
    "CTransformers",
    "Databricks",
    "DeepInfra",
    "ForefrontAI",
    "GooglePalm",
    "GooseAI",
    "GPT4All",
    "LlamaCpp",
    "Modal",
    "MosaicML",
    "NLPCloud",
    "OpenAI",
    "OpenAIChat",
    "OpenLM",
    "Petals",
    "PipelineAI",
    "HuggingFaceEndpoint",
    "HuggingFaceHub",
    "SagemakerEndpoint",
    "HuggingFacePipeline",
    "AI21",
    "AzureOpenAI",
    "Replicate",
    "SelfHostedPipeline",
    "SelfHostedHuggingFaceLLM",
    "PromptLayerOpenAI",
    "PromptLayerOpenAIChat",
    "StochasticAI",
    "Writer",
    "RWKV",
    "PredictionGuard",
    "HumanInputLLM",
    "HuggingFaceTextGenInference",
    "FakeListLLM",
    "VertexAI",
]

type_to_cls_dict: Dict[str, Type[BaseLLM]] = {
    "ai21": AI21,
    "aleph_alpha": AlephAlpha,
    "anthropic": Anthropic,
    "anyscale": Anyscale,
    "aviary": Aviary,
    "bananadev": Banana,
    "baseten": Baseten,
    "beam": Beam,
    "cerebriumai": CerebriumAI,
    "cohere": Cohere,
    "ctransformers": CTransformers,
    "databricks": Databricks,
    "deepinfra": DeepInfra,
    "forefrontai": ForefrontAI,
    "google_palm": GooglePalm,
    "gooseai": GooseAI,
    "gpt4all": GPT4All,
    "huggingface_hub": HuggingFaceHub,
    "huggingface_endpoint": HuggingFaceEndpoint,
    "llamacpp": LlamaCpp,
    "modal": Modal,
    "mosaic": MosaicML,
    "sagemaker_endpoint": SagemakerEndpoint,
    "nlpcloud": NLPCloud,
    "human-input": HumanInputLLM,
    "openai": OpenAI,
    "openlm": OpenLM,
    "petals": Petals,
    "pipelineai": PipelineAI,
    "huggingface_pipeline": HuggingFacePipeline,
    "azure": AzureOpenAI,
    "replicate": Replicate,
    "self_hosted": SelfHostedPipeline,
    "self_hosted_hugging_face": SelfHostedHuggingFaceLLM,
    "stochasticai": StochasticAI,
    "writer": Writer,
    "rwkv": RWKV,
    "huggingface_textgen_inference": HuggingFaceTextGenInference,
    "fake-list": FakeListLLM,
    "vertexai": VertexAI,
}
