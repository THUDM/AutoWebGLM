import openai
import os

async def call_gpt(model, prompt, history=None, system=None):
    message = []
    if system:
        message.append({
            "role": "system",
            "content": system
        })
    
    if history:
        for chat in history:
            message.append({
                "role": "user",
                "content": chat[0]
            })
            message.append({
                "role": "assistant",
                "content": chat[1]
            })
    
    message.append({
        "role": "user",
        "content": prompt
    })

    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set when using OpenAI API."
        )
    key = os.environ["OPENAI_API_KEY"]
    
    resp = openai.ChatCompletion.create(
        model=model,
        messages=message,
        api_key=key,
        timeout=1000
    )

    output = resp["choices"][0]["message"]["content"]

    return output