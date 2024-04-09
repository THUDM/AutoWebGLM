import secrets

class IdentifierTool:
    def __init__(self, method: str='order', existing_labels: dict[str]={}) -> None:
        self.methods = {
            'order': self.get_identifier_in_order,
            'random': self.get_random_identifier,
        }
        
        if method is None:
            method = 'order'
            
        self.func = self.methods.get(method, None)
        self.name = method
        if self.func is None:
            raise ValueError(f'Invalid method for identifier: {method}')
        
        self.reset(existing_labels)
    
    def reset(self, exists: dict[str]={}) -> None:
        self.identifier = -1
        self.exists = {} if exists is None else exists
        
    def get_identifier_in_order(self) -> str:
        def id2str(id: int) -> str:
            if id < 26:
                return chr(id + 65)
            id -= 26
            c0 = id // 676
            c1 = (id // 26) % 26
            c2 = id % 26
            label = f'{chr(c1 + 65)}{chr(c2 + 65)}'
            return label if c0 == 0 else f'{chr(c0 + 64)}{label}'
        
        self.identifier += 1
        label = id2str(self.identifier)
        
        while label in self.exists:
            self.identifier += 1
            label = id2str(self.identifier)
        
        self.exists[label] = True
        return label
    
    def get_random_identifier(self) -> str:
        secret_generator = secrets.SystemRandom()
        
        def get_random_label(n: int=2) -> str:
            tmp = ''
            for _ in range(n):
                tmp += chr(secret_generator.randint(65, 90))
            return tmp

        wc = 3 if len(self.exists) > 280 else 2

        label = get_random_label(wc)
        while label in self.exists:
            label = get_random_label(wc)
        
        self.exists[label] = True
        return label
        
    def generate(self):
        return self.func()