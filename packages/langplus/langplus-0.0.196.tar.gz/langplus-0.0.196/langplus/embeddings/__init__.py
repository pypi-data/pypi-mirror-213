"""Wrappers around embedding modules."""
import logging
from typing import Any

from langplus.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from langplus.embeddings.bedrock import BedrockEmbeddings
from langplus.embeddings.cohere import CohereEmbeddings
from langplus.embeddings.deepinfra import DeepInfraEmbeddings
from langplus.embeddings.elasticsearch import ElasticsearchEmbeddings
from langplus.embeddings.fake import FakeEmbeddings
from langplus.embeddings.google_palm import GooglePalmEmbeddings
from langplus.embeddings.huggingface import (
    HuggingFaceEmbeddings,
    HuggingFaceInstructEmbeddings,
)
from langplus.embeddings.huggingface_hub import HuggingFaceHubEmbeddings
from langplus.embeddings.jina import JinaEmbeddings
from langplus.embeddings.llamacpp import LlamaCppEmbeddings
from langplus.embeddings.minimax import MiniMaxEmbeddings
from langplus.embeddings.modelscope_hub import ModelScopeEmbeddings
from langplus.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from langplus.embeddings.openai import OpenAIEmbeddings
from langplus.embeddings.sagemaker_endpoint import SagemakerEndpointEmbeddings
from langplus.embeddings.self_hosted import SelfHostedEmbeddings
from langplus.embeddings.self_hosted_hugging_face import (
    SelfHostedHuggingFaceEmbeddings,
    SelfHostedHuggingFaceInstructEmbeddings,
)
from langplus.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langplus.embeddings.tensorflow_hub import TensorflowHubEmbeddings
from langplus.embeddings.vertexai import VertexAIEmbeddings

logger = logging.getLogger(__name__)

__all__ = [
    "OpenAIEmbeddings",
    "HuggingFaceEmbeddings",
    "CohereEmbeddings",
    "ElasticsearchEmbeddings",
    "JinaEmbeddings",
    "LlamaCppEmbeddings",
    "HuggingFaceHubEmbeddings",
    "ModelScopeEmbeddings",
    "TensorflowHubEmbeddings",
    "SagemakerEndpointEmbeddings",
    "HuggingFaceInstructEmbeddings",
    "MosaicMLInstructorEmbeddings",
    "SelfHostedEmbeddings",
    "SelfHostedHuggingFaceEmbeddings",
    "SelfHostedHuggingFaceInstructEmbeddings",
    "FakeEmbeddings",
    "AlephAlphaAsymmetricSemanticEmbedding",
    "AlephAlphaSymmetricSemanticEmbedding",
    "SentenceTransformerEmbeddings",
    "GooglePalmEmbeddings",
    "MiniMaxEmbeddings",
    "VertexAIEmbeddings",
    "BedrockEmbeddings",
    "DeepInfraEmbeddings",
]


# TODO: this is in here to maintain backwards compatibility
class HypotheticalDocumentEmbedder:
    def __init__(self, *args: Any, **kwargs: Any):
        logger.warning(
            "Using a deprecated class. Please use "
            "`from langchain.chains import HypotheticalDocumentEmbedder` instead"
        )
        from langplus.chains.hyde.base import HypotheticalDocumentEmbedder as H

        return H(*args, **kwargs)  # type: ignore

    @classmethod
    def from_llm(cls, *args: Any, **kwargs: Any) -> Any:
        logger.warning(
            "Using a deprecated class. Please use "
            "`from langchain.chains import HypotheticalDocumentEmbedder` instead"
        )
        from langplus.chains.hyde.base import HypotheticalDocumentEmbedder as H

        return H.from_llm(*args, **kwargs)
