"""This module is adapt from https://github.com/zeno-ml/zeno-build"""
from .providers.hf_utils import generate_from_huggingface_completion
from .providers.ours import call_pretrain_model
from .providers.openai_utils import (
    generate_from_openai_chat_completion,
    generate_from_openai_completion,
)
from .utils import call_llm

__all__ = [
    "generate_from_openai_completion",
    "generate_from_openai_chat_completion",
    "generate_from_huggingface_completion",
    "call_llm",
    "call_pretrain_model"
]
