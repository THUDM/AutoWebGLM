from .configs import miniwob_prompt, miniwob_prompt_with_tp, miniwob_prompt_new_action_space

class ActionParser:
    operation_pattern = {
        'Click': r'#Click#\s*([A-Z]{1,3})',
        'Hover': r'#Hover#\s*([A-Z]{1,3})',
        'Scroll_up': r'#Scroll_up#',
        'Scroll_down': r'#Scroll_down#',
        'Type': r'#Type#\s*([A-Z]{1,3})\s*"{0,1}(.+)"{0,1}',
    }
    
    new_action_space_pattern = {
        'Click': r'click\([\'\"]([A-Z]{1,3})[\'\"]\)',
        'Hover': r'hover\([\'\"]([A-Z]{1,3})[\'\"]\)',
        'Scroll_up': r'scroll_page\([\'\"]up[\'\"]\)',
        'Scroll_down': r'scroll_page\([\'\"]down[\'\"]\)',
        'Type': r'type_string\([\'\"]([A-Z]{1,3})[\'\"]\s*,\s*[\'\"](.+)[\'\"]\s*,\s*(True|False)\)',
    }
    
    prompts = {
        'basic': miniwob_prompt,
        'tp': miniwob_prompt_with_tp,
        'new_action_space': miniwob_prompt_new_action_space,
    }
    
    def __init__(self, prompt: str='basic') -> None:
        if prompt not in self.prompts:
            raise ValueError('Invalid prompt type.')
        
        funcs = {
            'basic': self.extract_operation,
            'tp': self.extract_operation_with_tp,
            'new_action_space': self.extract_operation_new_action_space,
        }
        
        self.prompt = self.prompts[prompt]
        self.func = funcs[prompt]
    
    def get_prompt(self) -> str:
        return self.prompt

    def extract(self, result: str='') -> (None, tuple):
        return self.func(result)
            
    @staticmethod
    def extract_operation(result: str='') -> (str, str):
        import re
        # match = re.search(r'#Operation:\s*(.+)', result)
        # if not match:
        #     return None
        # opstr = match.group(1)
        opstr = result
        
        for op, pattern in ActionParser.operation_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                param.append(param[1])
            return '', op, param
            
        return None
    
    @staticmethod
    def extract_operation_with_tp(result: str='') -> (str, str):
        import re
        match = re.search(r'#Thinking Process:\s*(.+)\s*#Operation:\s*(.+)', result)
        if not match:
            return None
        tpstr = match.group(1)
        opstr = match.group(2)
        
        for op, pattern in ActionParser.operation_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                param.append(False)
            return tpstr, op, match.groups()
            
        return None

    @staticmethod
    def extract_operation(result: str='') -> (str, str):
        import re
        # match = re.search(r'#Operation:\s*(.+)', result)
        # if not match:
        #     return None
        # opstr = match.group(1)
        opstr = result
        
        for op, pattern in ActionParser.operation_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                param.append(False)
            return '', op, param
            
        return None
    
    @staticmethod
    def extract_operation_new_action_space(result: str='') -> (str, str):
        import re
        opstr = result
        
        for op, pattern in ActionParser.new_action_space_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                if param[1] == 'True':
                    param[1] = True
                elif param[1] == 'False':
                    param[1] = False
                    
            return '', op, param
            
        return None