import time, json, os, sys, copy
import gymnasium
from miniwob.action import ActionTypes, ActionSpaceConfig
from miniwob.reward import get_binary_reward

import numpy as np
from html_tools import HtmlParser, basic_attrs
from miniwob_tools import ActionParser, testcases, mwpp_attrs, not_clickable_tag, miniwob_attrs
from miniwob_tools import save_pixel_array, get_dom_list, get_html, update_dom_list, get_position_bar, get_position_info, process_dom_list
from llms import CallLLM

import multiprocessing as mp

import logging, time, random, secrets
from pathlib import Path

LOG_FOLDER = 'log_files'
Path(LOG_FOLDER).mkdir(parents=True, exist_ok=True)
LOG_ID = f"{time.strftime('%Y%m%d_%H%M%S', time.localtime())}_{random.randint(0, 10000)}"

LOG_FILE_NAME = f'{LOG_FOLDER}/log_{LOG_ID}.log'
LOG_CONTENT = f'{LOG_FOLDER}/result/'
Path(LOG_CONTENT).mkdir(parents=True, exist_ok=True)

logger = logging.getLogger('logger')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(LOG_FILE_NAME)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# Set the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

class TestMiniwob:
    def __init__(self, model_path='chatgpt', result_path=LOG_CONTENT, cuda: str='0', log_path='logs/', prompt='new_action_space'):
        self.action_parser = ActionParser(prompt=prompt)
        self.result_path = result_path
        self.llm = CallLLM(model_path, cuda)
    
    def get_operation(self, prompt: str):
        res = self.llm.model_call(prompt)
        act = self.action_parser.extract(res)
        return act, res
    
    def policy(self, obs, env, prev_ops):      
        def get_position_by_bid(dom_list: list, bid: int) -> tuple:
            for elem in dom_list:
                if elem['ref'] == bid:
                    x = float(elem['left'] + elem['width'] * 0.5)
                    y = min(max(float(elem['top'] + elem['height'] * 0.5), 55.0), 200.0)
                    return np.array([x, y], dtype=float)
            return (0, 0)
        
        save_pixel_array(obs.get('screenshot', ''), '1.png')
        target = obs.get('utterance', '')
        
        dom_list = obs.get('dom_elements', [])
        action = env.unwrapped.create_action(ActionTypes.NONE)
        if len(dom_list) <= 0:
            return action, {}
        
        rhtml, obs_elem = get_html(copy.deepcopy(dom_list))
        
        args = {
            'use_position': False,
            'id_attr': 'ref',
            'label_attr': 'label',
            'label_generator': 'order',
            'attr_list': miniwob_attrs,
            'obs_elem': obs_elem,
            'prompt': 'refine',
        }
        hp = HtmlParser(rhtml, args)
        res = hp.parse_tree()
        html = res.get('html', '')
        
        ndom_list = update_dom_list(dom_list)
        
        # pos_bar = get_position_bar(ndom_list)
        # prev_str = '\n'.join(prev_ops[-10:]) if len(prev_ops) > 0 else 'None'
        # prompt = self.action_parser.get_prompt() % (html, pos_bar, prev_str, target)
        
        pos_bar = get_position_info(ndom_list)
        prev_str = '\n'.join(prev_ops) if len(prev_ops) > 0 else 'None'
        prompt = self.action_parser.get_prompt() % (html, prev_str, pos_bar, target)
        
        # TODO: For debug
        
        # for dom in ndom_list:
        #     bid = str(dom.get('ref', ''))
        #     label = hp.id_label_converter(bid)
        #     dom['label'] = label
        # print(rhtml)
        # print('\n'.join(get_dom_list(ndom_list)))
        print(prompt)
        
        act, res = self.get_operation(prompt)
        
        cmsg = {
            'dom': process_dom_list(dom_list),
            'prompt': prompt,
            'response': res,
            'action': json.dumps(act, ensure_ascii=False),
        }
        
        print('[Action]', act)
        
        if act is None:
            return action, cmsg
        
        intent, op, param = act
        segment = 'None'
        
        if op in ['Click', 'Hover', 'Type']:
            if param is None or len(param) == 0:
                return action, cmsg
            label = param[0]
            bid = hp.id_label_converter(label)
            if len(bid) == 0:
                return action, cmsg
            
            segment = hp.get_segment(bid)
            position = get_position_by_bid(dom_list, int(bid))
        
        # command_prompt = {
        #     'Click': '#Click# %s',
        #     'Hover': '#Hover# %s',
        #     'Scroll_up': '#Scroll_up#',
        #     'Scroll_down': '#Scroll_down#',
        #     'Type': '#Type# %s %s',
        # }
        
        command_prompt = {
            'Click': "click('%s')",
            'Hover': "hover('%s')",
            'Scroll_up': "scroll_page('up')",
            'Scroll_down': "scroll_page('down')",
            'Type': "type_string('%s', '%s', %s)"
        }
        
        if op == 'Click':
            action = env.unwrapped.create_action(ActionTypes.CLICK_COORDS, coords=position)
            command = command_prompt[op] % label
        if op == 'Hover':
            action = env.unwrapped.create_action(ActionTypes.MOVE_COORDS, coords=position)
            command = command_prompt[op] % label
        if op == 'Scroll_up':
            action = env.unwrapped.create_action(ActionTypes.SCROLL_UP_COORDS, coords=(80, 80))
            command = command_prompt[op]
        if op == 'Scroll_down':
            action = env.unwrapped.create_action(ActionTypes.SCROLL_DOWN_COORDS, coords=(80, 80))
            command = command_prompt[op]
        if op == 'Type':
            clear_text = '\uE003' * 500
            enter_text = '\uE006' if param[2] else ''
            action = env.unwrapped.create_action(ActionTypes.FOCUS_ELEMENT_AND_TYPE_TEXT, ref=bid, text=clear_text+param[1]+enter_text)
            command = command_prompt[op] % (label, param[1], param[2])
        
        print(action)
        ix = len(prev_ops) + 1
        # cur_op = f'{ix}. Html segment: {segment}; Operation: {command};'
        cur_op = f'{command} #HTML Segment: {segment}'
        # print(cur_op)
        prev_ops.append(cur_op)
        return action, cmsg
                
    def test(self, testname: str='', test_cnt: int=10) -> dict:
        asc = ActionSpaceConfig.get_preset()
        asc.scroll_amount = 145
        asc.scroll_time = 100
        env = gymnasium.make(f'miniwob/{testname}-v1', reward_processor=get_binary_reward, action_space_config=asc)#, render_mode='human')
           
        rewards = []
        mission_history = []
        
        test_path = os.path.join(self.result_path, f'{testname}.json')
        if os.path.exists(test_path):
            with open(test_path, 'r') as f:
                data = json.load(f)
            completed = data.get('completed', 0)
            if completed >= test_cnt:             
                score = data.get('avg_score', 0)
                return { testname: score }
        
        # run test
        secrets_generator = secrets.SystemRandom()
        try:
            seed_id = secrets_generator.randint(0, 10**9)
            obs, info = env.reset(seed=seed_id)
            for ix in range(test_cnt):
                target = obs.get('utterance', '')
                meta = {
                    'seed': seed_id,
                    'task': testname,
                    'case_id': ix,
                }
                
                mission_path = os.path.join(self.result_path, f'{testname}_{ix}.json')
                if os.path.exists(mission_path):
                    with open(mission_path, 'r') as f:
                        data = json.load(f)
                    if 'result' in data:
                        result = data['result']
                        rewards.append(result)
                        continue
                
                terminated = False
                reward = 0
                prev_ops = []
                
                llm_histories = []
                while True:
                    action, cmsg = self.policy(obs, env, prev_ops)
                    print(action)
                    if len(cmsg) > 0:
                        llm_histories.append(cmsg)
                    
                    obs, reward, terminated, truncated, info = env.step(action)
                    print(reward, terminated, truncated, info)
                    
                    if terminated or reward != 0:
                        seed_id = secrets_generator.randint(0, 10**9)
                        obs, info = env.reset(seed=seed_id)
                        break
                    
                    time.sleep(0.3)
                    obs, _, _, _, _ = env.step(env.unwrapped.create_action(ActionTypes.NONE))
                
                reward = 0 if reward < 0 else reward
                rewards.append(reward)   

                meta.update({
                    'result': reward,
                })
                 
                logger.info(json.dumps(meta, ensure_ascii=False))
                
                meta.update({
                    'log_id': LOG_ID,
                    'target': target,
                    'llm_histories': llm_histories
                })
                mission_history.append(meta)
                
                with open(mission_path, 'w') as f:
                    json.dump(meta, f, ensure_ascii=False)
        
        except Exception as e:
            logger.error(e)
        finally:
            env.close()
        
        if len(rewards) == 0:
            rewards.append(0)
        
        score = np.mean(rewards)
        meta = {
            'task': testname,
            'avg_score': score,
            'completed': len(rewards),
        }
        
        logger.info(json.dumps(meta, ensure_ascii=False))
        
        meta.update({
            'log_id': LOG_ID,
        })
        
        with open(test_path, 'w') as f:
            json.dump(meta, f, ensure_ascii=False)
            
        return { testname: score }

    def test_all_parallel(self, tasks: list=testcases, test_cnt: int=10):
        result, rewards = {}, []
        
        for testcase in tasks:
            ret = self.test(testcase, test_cnt)
            result.update(ret)
            rewards.extend(ret.values())
            
        self.log_all_result(result, rewards)
        return result
        
    @staticmethod
    def log_all_result(result: dict, rewards: list):
        logger.info('------')
        for k, v in result.items():
            logger.info('{:<30} {:6.2f}'.format(k, v))
        
        logger.info('{:<30} {:6.3f}'.format('all', np.mean(rewards)))

def create_job(q, model_path: str, result_path: str, cuda: str, tasks: list[str], test_cnt: int=10):
    test = TestMiniwob(model_path, result_path, cuda)
    result = test.test_all_parallel(tasks, test_cnt)
    q.put(result)

if __name__ == '__main__':
    cudas = sys.argv[1]
    test_cnt = int(sys.argv[2])
    model_path = sys.argv[3] 
    result_path = sys.argv[4] 
    # model_path = '/workspace/hanyu/hanyu/ckpt/autoglm/sft/step2/chatglm-9300'
    # result_path = 'result-0/'
    
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    
    if model_path == 'manual':
        test = TestMiniwob('manual', result_path)
        test.test_all_parallel(['enter-text'])
    
    else:
        cuda_ids = cudas.split(',')
        cudas_count = len(cuda_ids)
        
        result, rewards = {}, []
        
        tests = []
        for testname in testcases:
            test_path = os.path.join(result_path, f'{testname}.json')
            if os.path.exists(test_path):
                with open(test_path, 'r') as f:
                    data = json.load(f)
                completed = data.get('completed', 0)
                if completed >= test_cnt:  
                    score = data.get('avg_score', 0)
                    result.update({ testname: score })
                    rewards.append(score)
                    continue
            tests.append(testname)
        
        task_cnt = len(tests)
        batch = (task_cnt + cudas_count - 1) // cudas_count
        
        q = mp.Queue()
        processes = []
            
        for ix, cuda in enumerate(cuda_ids):
            p = mp.Process(target=create_job, args=(q, model_path, result_path, cuda, tests[ix * batch: (ix + 1) * batch], test_cnt, ))
            p.start()
            processes.append(p)

        for p in processes:
            ret = q.get()
            result.update(ret)
            rewards.extend(ret.values())
            
        for p in processes:
            p.join()
        
        TestMiniwob.log_all_result(result, rewards)
