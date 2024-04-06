from .configs import prompts

class HtmlPrompt:    
    def __init__(self, prompt: str='') -> None:
        prompt = self.extract(prompt, 'xml')
        if prompt not in prompts:
            raise Exception('Unknown prompt: ' + prompt)
        
        constructors = {
            'refine': self.normal_prompt_constructor,
            'xml': self.normal_prompt_constructor,
            'new_data': self.new_data_prompt_constructor,
        }

        self.name = prompt
        self.prompt = prompts[prompt]
        self.constructor = constructors[prompt]

    @staticmethod
    def extract(data, default=''):
        return data if data is not None else default
    
    def subtree_constructor(self, subtree: list[str]=[]) -> str:
        return self.prompt['subtree_splitter'].join(subtree)

    def normal_prompt_constructor(self, tag: str='', label: str='', content: str='', subtree_str: str='', class_dict: dict[str]={}) -> str:
        def add_prefix(data, prefix):
            return prefix + data if len(data) > 0 else ''
        
        tag = self.extract(tag)
        label = self.extract(label)
        content = self.extract(content)
        subtree_str = self.extract(subtree_str, '')
        class_dict = self.extract(class_dict, {})
        
        label_str = ''
        if len(label) > 0:
            label_str = self.prompt['label'].format(label=label)
        
        classes = []
        values = set()
        for key, val in class_dict.items():
            if val in values:
                continue
            values.add(val)
            classes.append(self.prompt['attr'].format(key=key, attr=val))
        classes_str = self.prompt['attr_splitter'].join(classes)
        
        content_splitter = ' ' if len(classes_str) == 0 else self.prompt['attr_splitter']
        classes_str = add_prefix(classes_str, ' ')
        content_str = add_prefix(content, content_splitter)
        subtree_str = add_prefix(subtree_str, ' ')

        return self.prompt['dom'].format(tag=tag, label=label_str, attr=classes_str, content=content_str, subtree=subtree_str)
    
    def new_data_prompt_constructor(self, tag: str='', label: str='', content: str='', subtree_str: str='', class_dict: dict[str]={}) -> str:
        def add_prefix(data, prefix):
            return prefix + data if len(data) > 0 else ''
        
        tag = self.extract(tag)
        label = self.extract(label)
        content = self.extract(content)
        subtree_str = self.extract(subtree_str, '')
        class_dict = self.extract(class_dict, {})
        
        label_str = ''
        if len(label) > 0:
            label_str = self.prompt['label'].format(label=label)
        
        classes = []
        values = set()
        
        message = []
        for key, val in class_dict.items():
            if val == '':
                message.append(key)
                continue
            if val in values:
                continue
            values.add(val)
            classes.append(self.prompt['attr'].format(key=key, attr=val))
        
        if len(message) > 0:
            message_str = ' '.join(message)
            classes.append(self.prompt['attr'].format(key='message', attr=message_str))
            
        classes_str = self.prompt['attr_splitter'].join(classes)
        
        content_splitter = ' ' if len(classes_str) == 0 else self.prompt['attr_splitter']
        classes_str = add_prefix(classes_str, ' ')
        content_str = add_prefix(content, content_splitter)
        subtree_str = add_prefix(subtree_str, ' ')

        return self.prompt['dom'].format(tag=tag, label=label_str, attr=classes_str, content=content_str, subtree=subtree_str)

    def prompt_constructor(self, tag: str='', label: str='', content: str='', subtree_str: str='', class_dict: dict[str]={}) -> str:
        return self.constructor(tag, label, content, subtree_str, class_dict)