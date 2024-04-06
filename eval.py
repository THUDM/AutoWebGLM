import json
import sys
import re
import numpy as np

from rouge_chinese import Rouge
import jieba # you can use any other word cutting library

def get_rouge_score(hypothesis, reference):
    if hypothesis is None or reference is None:
        return None

    hypothesis = ' '.join(jieba.cut(hypothesis)) 
    reference = ' '.join(jieba.cut(reference))

    rouge = Rouge()
    scores = rouge.get_scores(hypothesis, reference)

    return scores[0]["rouge-1"]['f']

def parse_function_call(function_call):
    pattern = r"(\w+)\((.*)\)"
    match = re.match(pattern, function_call)

    if match:
        function_name = match.group(1)
        
        def return_args(*args):
            return args
        
        function_args = eval(f'return_args({match.group(2)})')

        return function_name, function_args

    return None

def extract(text):
    ans = {
        'type': None,
        'label': None,
        'param': None
    }
    
    match = parse_function_call(text)
    if match:
        ans['type'] = match[0]
        args = match[1]

    if ans['type']:
        if ans['type'] == 'click':
            ans['label'] = args[0]
        elif ans['type'] == 'hover':
            ans['label'] = args[0]
        elif ans['type'] == 'select':
            ans['label'] = args[0]
            ans['param'] = args[1]
        elif ans['type'] == 'type_string':
            ans['label'] = args[0]
            ans['param'] = args[1]
        elif ans['type'] == 'scroll_page':
            ans['param'] = args[0]
        elif ans['type'] == 'go':
            ans['param'] = args[0]
        elif ans['type'] == 'jump_to':
            ans['param'] = args[0]
        elif ans['type'] == 'switch_tab':
            ans['param'] = args[0]
        elif ans['type'] == 'user_input':
            ans['param'] = args[0]
        elif ans['type'] == 'finish':
            ans['param'] = args[0]

    return ans

if __name__ == '__main__':
    result_path = sys.argv[1]
    res_list = {
        'type': [],
        'label': [],
        'param': [],
        'all': []
    }

    for ix, r_str in enumerate(open(result_path).readlines()):
        r = json.loads(r_str)
        try:
            labels = json.loads(r['labels'])
        except:
            labels = [r['labels']]

        res = {}

        for label in labels:
            pred = r['predict'].split('A: ')[-1].strip()
            try:
                label_ans = extract(label)
                pred_ans = extract(pred)
            except:
                continue

            print(f'{ix}. label:', label_ans)
            print(f'{ix}. pred:', pred_ans)

            if label_ans['type'] is not None:
                if label_ans['type'] == pred_ans['type']:
                    res['type'] = 1
                else:
                    res['type'] = 0
            
            if label_ans['label'] is not None:
                if label_ans['label'] == pred_ans['label']:
                    res['label'] = 1
                else:
                    res['label'] = 0
                
            if label_ans['param'] is not None:
                rouge = get_rouge_score(label_ans['param'], pred_ans['param'])
                if rouge:
                    res['param'] = rouge

            if label_ans['type'] is not None and label_ans['label'] is not None:
                if label_ans['type'] == pred_ans['type'] and label_ans['label'] == pred_ans['label']:
                    res['all'] = 1
                    break
                else:
                    res['all'] = 0
        
        for k, v in res.items():
            res_list[k].append(v)

    for k, v in res_list.items():
        if v:
            res_list[k] = float(np.mean(v))
        else:
            res_list[k] = 0.0
    
    print(res_list)