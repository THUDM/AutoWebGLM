from .gpt import call_gpt
from functools import partial

def call_manual(prompt, history=None, system=None):
    return input()

call_method = {
    'chatgpt': partial(call_gpt, 'gpt-3.5-turbo'),
    'gpt4': partial(call_gpt, 'gpt-4'),
    'manual': call_manual,
}