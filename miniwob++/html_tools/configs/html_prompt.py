refine_prompt = {
    'dom': '<{tag}{label}|{attr}{content}{subtree} >',
    'label': '[{label}]',
    'attr': '{attr}',
    'attr_splitter': '; ',
    'subtree_splitter': ' ',
}

xml_prompt = {
    'dom': '<{tag}{label}{attr}>{content}{subtree} </{tag}>',
    'label': ' id="{label}"',
    'attr': '{key}="{attr}"',
    'attr_splitter': ' ',
    'subtree_splitter': ' ',
}

prompts = {
    'refine': refine_prompt,
    'xml': xml_prompt,
    'new_data': refine_prompt, 
}
    