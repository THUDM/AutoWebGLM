import argparse
from typing import Any
from transformers import AutoTokenizer, AutoModel

from llms import (
    generate_from_huggingface_completion,
    generate_from_openai_chat_completion,
    generate_from_openai_completion,
    call_pretrain_model,
    lm_config,
)

APIInput = str | list[Any] | dict[str, Any]

model = None
tokenizer = None

def call_llm(
    lm_config: lm_config.LMConfig,
    prompt: APIInput,
) -> str:
    global model
    global tokenizer
    
    response: str
    
    if lm_config.provider == "openai":
        if lm_config.mode == "chat":
            assert isinstance(prompt, list)
            response = generate_from_openai_chat_completion(
                messages=prompt,
                model=lm_config.model,
                temperature=lm_config.gen_config["temperature"],
                top_p=lm_config.gen_config["top_p"],
                context_length=lm_config.gen_config["context_length"],
                max_tokens=lm_config.gen_config["max_tokens"],
                stop_token=None,
            )
        elif lm_config.mode == "completion":
            assert isinstance(prompt, str)
            response = generate_from_openai_completion(
                prompt=prompt,
                engine=lm_config.model,
                temperature=lm_config.gen_config["temperature"],
                max_tokens=lm_config.gen_config["max_tokens"],
                top_p=lm_config.gen_config["top_p"],
                stop_token=lm_config.gen_config["stop_token"],
            )
        else:
            raise ValueError(
                f"OpenAI models do not support mode {lm_config.mode}"
            )
    elif lm_config.provider == "huggingface":
        assert isinstance(prompt, str)
        response = generate_from_huggingface_completion(
            prompt=prompt,
            model_endpoint=lm_config.gen_config["model_endpoint"],
            temperature=lm_config.gen_config["temperature"],
            top_p=lm_config.gen_config["top_p"],
            stop_sequences=lm_config.gen_config["stop_sequences"],
            max_new_tokens=lm_config.gen_config["max_new_tokens"],
        )
    elif lm_config.provider == "ours":
        # print(prompt)
        if lm_config.model == 'manual':
            response = input("Command > ")
        else:
            if not model:
                model = AutoModel.from_pretrained(lm_config.model, trust_remote_code=True, device=f'cuda:{lm_config.cuda}')
                tokenizer = AutoTokenizer.from_pretrained(lm_config.model, trust_remote_code=True)
                model.eval()
            response = call_pretrain_model(prompt, model, tokenizer, lm_config.cuda)
    else:
        raise NotImplementedError(
            f"Provider {lm_config.provider} not implemented"
        )

    return response
