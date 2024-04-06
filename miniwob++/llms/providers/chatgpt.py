import aiohttp
import requests

def call_chatgpt(prompt, history=None, system=None):
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
    
    endpoint = "http://40.74.217.35:10014/api/v1/chat/completions"
    
    payload = {
            "model": "gpt-3.5-turbo",
            "messages": message,
            "temperature": 0.9
        }
    
    headers = {
        "Authorization": "bd91cab0bac53e6e3bb091f308ab23e9",
    }

    try:
        resp = requests.post(endpoint, headers=headers, json=payload)
        resp = resp.json()
        output = resp["choices"][0]["message"]["content"]
    except:
        output = ''
    
    print("[chatgpt]", output)
        
    return output