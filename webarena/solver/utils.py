import copy
import json
from PIL import Image

from agent import PromptAgent
from browser_env.helper_functions import get_action_description
from browser_env import ActionTypes

def show_screenshot(state_info):
    image_data = state_info["observation"]["image"]
    im = Image.fromarray(image_data)
    im.save('output/show_screenshot.png')

def get_nodes(dom_tree, nodes_info, attr, attrval, mode: int=0, use_elem: int=0):
    tar_nodes, temp_nodes = [], []
    for nodes in dom_tree:
        if (mode == 1 and nodes[attr] == attrval) or (mode == 0 and nodes[attr].count(attrval) > 0):
            if use_elem == 0:
                tar_nodes.append(nodes['backendNodeId'])
            elif use_elem == 1:
                temp_nodes.extend(nodes['childIds'])
            elif use_elem == 2:
                temp_nodes.append(nodes['parentId'])
                
    if use_elem != 0:
        for node in dom_tree:
            if node['nodeId'] in temp_nodes:
                tar_nodes.append(node['backendNodeId'])
    
    act_nodes = []
    
    for node in list(nodes_info.values()):
        if node['backend_id'] in tar_nodes:
            act_nodes.append(node)
    return act_nodes
 
def step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action):    
    obs_info = state_info["info"]["observation_metadata"]["text"]
    images = state_info["info"]["images"]
    dom_info, nodes_info = obs_info["dom_info"], obs_info["obs_nodes_info"]
    dom_tree = dom_info["dom_tree"]
    raw_html = dom_info["raw_html"]

    if target_action.count('#Type#') > 0 and target_action.endswith('\\n'):
        target_action = target_action[:-2] + '\n'
    
    prompt, action = agent.check_action(
        trajectory, intent, meta_data, target_action
    )

    print('[prompt] ', prompt)
    print('[action] ', action)
    
    # our_dom_tree = copy.deepcopy(dom_tree)
    # for elem in our_dom_tree:
    #     elem["union_bound"] = elem["union_bound"].tolist()
    
    myaction = copy.deepcopy(action)
    myaction["coords"] = myaction["coords"].tolist()
    
    need_to_keep = action['action_type'] != ActionTypes.NONE or target_action.count("#Record#") > 0
    
    trajectory.append(action)

    action_str = get_action_description(
        action,
        state_info["info"]["observation_metadata"],
        action_set_tag=args.action_set_tag,
        prompt_constructor=agent.prompt_constructor
        if isinstance(agent, PromptAgent)
        else None,
    )
    
    if need_to_keep:
        user_action = action_str.split(' #HTML Segment')[0]
        traces.append({
            'source': prompt,
            'target': f'{real_action}',
            'extra_data': {
                'element_id': action.get('element_id', ''),
                'dom_tree': dom_tree,
                'raw_html': raw_html,
                'nodes_info': nodes_info,
                'raw_action': myaction,
                'images': images,
            },
        })
    
    render_helper.render(
        action, state_info, meta_data, args.render_screenshot
    )
    
    if need_to_keep:
        meta_data["action_history"].append(action_str)

    if action["action_type"] == ActionTypes.STOP:
        return None
    
    # if action['action_type'] == ActionTypes.TYPE:
    #     action['text'] = [110] * 500 + action['text']

    obs, _, terminated, _, info = env.step(action)
    state_info = {"observation": obs, "info": info}
    show_screenshot(state_info)
    
    trajectory.append(state_info)

    if terminated:
        # add a action place holder
        trajectory.append(create_stop_action(""))
        return None
    
    obs_info = state_info["info"]["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    return state_info, dom_tree, nodes_info