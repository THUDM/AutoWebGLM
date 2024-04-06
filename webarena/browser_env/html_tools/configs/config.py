basic_attrs = [
    'title',
    'value',
    'placeholder',
    'selected',
]
    
mind2web_keep_attrs = [
    'alt',
    'aria_description',
    'aria_label',
    'aria_role',
    'input_checked',
    'input_value',
    'label',
    'name',
    'option_selected',
    'placeholder',
    'role',
    'text_value',
    'title',
    'type',
    'value',
]

miniwob_attrs = [
    'id',
    'type',
    'value',
]

config_meta = """
======= Configs =======
Columns:
  - id:        {id_attr}
  - label:     {label_attr}
Position:      {use_position}
  - window:    {window_size}
  - rect_dict: {rect}
Keep:
  - parents:   {parent_chain}
  - attrs:     {keep_attrs}
  - elems:     {keep_elem}
  - obs_elem:  {obs_elem}
Generator:
  - prompt:    {prompt_name}
  - label:     {identifier_name}
========================
"""