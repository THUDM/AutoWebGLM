from .chatgpt import call_chatgpt
from .gpt4 import call_gpt4

def call_manual(prompt, history=None, system=None):
    return input()

call_method = {
    'chatgpt': call_chatgpt,
    'gpt4': call_gpt4,
    'manual': call_manual,
}