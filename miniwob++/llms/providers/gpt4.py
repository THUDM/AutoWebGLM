import openai
openai.api_base="http://40.74.217.35:3000/v1"

async def call_gpt4(prompt, history=None, system=None):
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

    key = 'sk-qhT3mIN29Ca1reky2f7fDa7e9fC048279a2465A143616902'
    
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message,
        api_key=key,
        timeout=1000
    )

    output = resp["choices"][0]["message"]["content"]

    print("[gpt4]", output)

    # import pdb
    # pdb.set_trace()

    return output