from .utils import step_once, show_screenshot

from browser_env import (
    StateInfo,
    Trajectory,
)

def solver_240(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 2",
        "#Click# 4",
        "#Click# 22",
        "#Type# 42 218",
        "#Click# 52",
        "#Click# 41"
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    # while True:
    #     obs_info = state_info["info"]["observation_metadata"]["text"]
    #     dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    #     target_action = input()
    #     if target_action == 'noop':
    #         break
    #     res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
    #     if res is None:
    #         return traces, trajectory
    #     state_info, dom_tree, nodes_info = res
    
    instr_list = [
        # "#Click# 25",
        "#Scroll_down#",
        "#Type# 16 556 Pick Street",
        "#Select# 21 Colorado",
        "#Type# 23 Denver",
        "#Type# 25 80203",
        "#Click# 13",
        "#Exit#"
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        

def solver_241(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 3",
        "#Click# 5",
        # "#Click# 22",
        # "#Type# 42 218",
        # "#Click# 52",
        # "#Click# 41"
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
    
    # instr_list = [
    #     # "#Click# 25",
    #     "#Scroll_down#",
    #     "#Type# 16 556 Pick Street",
    #     "#Select# 21 Colorado",
    #     "#Type# 23 Denver",
    #     "#Type# 25 80203",
    #     "#Click# 13",
    #     "#Exit#"
    # ]
    
    # for instr in instr_list:
    #     obs_info = state_info["info"]["observation_metadata"]["text"]
    #     dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    #     target_action = instr
    #     res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
    #     if res is None:
    #         return traces, trajectory
    #     state_info, dom_tree, nodes_info = res
    
def solver_368(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 3",
        "#Click# 5",
        "#Click# 22",
        "#Click# 20",
        "#Type# 30 99",
        "#Type# 32 99",
        "#Click# 55",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res

def solver_279(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 7",
        "#Click# 27",
        "#Select# 22 year",
        "#Click# 25",
        "#Select# 34 2022",
        # "#Select# 33 May",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    instr_list = [
        "#Click# 18",
        "#Scroll_down#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_288(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 5",
        "#Click# 17",
        f"#Type# 44 {field_dict['term']}",
        "#Click# 17",
        # "#Type# 30 99",
        # "#Type# 32 99",
        # "#Click# 55",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_285(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Scroll_down#",
        "#Scroll_down#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_275(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 6",
        "#Click# 8",
        "#Click# 23",
        f"#Type# 19 {field_dict['old-heading']}\n",
        "#Click# 39",
        "#Click# 40",
        f"#Type# 23 {field_dict['heading']}",
        "#Click# 18",
        "#Exit#"
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_270(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
    instr_list = [
        "#Click# 7",
        "#Click# 15",
        "#Select# 24 month",
        "#Click# 27",
        "#Select# 30 2022",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    instr_list = [
        "#Click# 30",
        "#Select# 28 2022",
        # "#Select# 25 Dec",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    instr_list = [
        "#Click# 18",
        "#Scroll_down#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_247(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    print(field_dict)
        
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
    
    instr_list = [
        "#Click# 18",
        "#Exit#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_253(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 2",
        "#Click# 4",
        "#Click# 24",
        "#Click# 22",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    # "#Select# 46"
    print(field_dict)
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    instr_list = [
        "#Click# 50",
        "#Exit#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_257(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 2",
        "#Click# 4",
        "#Click# 24",
        "#Click# 22",
        f"#Type# 40 {field_dict['id']}",
        "#Click# 50",
        "#Click# 41",
        "#Click# 19",
        "#Click# 2",
        "#Exit#"
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_258(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 5",
        "#Click# 8",
        "#Click# 16",
        f"#Type# 22 {field_dict['topic']}",
        "#Select# 28 0",
        "#Scroll_down#",
        "#Select# 16 General",
        "#Scroll_down#",
        "#Click# 23",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    """
    #Select# 25 cart_fixed
    #Type# 28 10
    """
    print(field_dict)
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    instr_list = [
        "#Click# 11",
        "#Exit#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_268(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 7",
        "#Click# 15",
        "#Click# 27",
        "#Select# 30 2022",
        "#Click# 29",
        "#Click# 30",
        "#Select# 28 2022",
        "#Select# 25 Dec",
        "#Click# 59",
        "#Click# 18",
        "#Exit#"
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    """
    #Select# 25 cart_fixed
    #Type# 28 10
    """
    print(field_dict)
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    instr_list = [
        "#Click# 11",
        "#Exit#",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
def solver_277(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 5",
        "#Click# 17",
        f"#Select# 41 {field_dict['status']}",
        "#Click# 17",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    """
    #Answer# 0
    """
    print(field_dict)
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res

def solver_274(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = []
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 2",
        "#Click# 5",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    """
    #Answer# $175.40
    """
    print(field_dict)
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res

def solver_364(env, config_file, render_helper, agent, args, intent, field_dict):
    agent.reset(config_file)
    trajectory: Trajectory = [] 
    obs, info = env.reset(options={"config_file": config_file})
    state_info: StateInfo = {"observation": obs, "info": info}
    trajectory.append(state_info)

    meta_data = {"action_history": ["None"]}
    traces = []
    
    obs_info = info["observation_metadata"]["text"]
    dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
    
    instr_list = [
        "#Click# 4",
        "#Click# 6",
        "#Click# 24",
        "#Click# 22",
        f"#Type# 46 {field_dict['PhoneNum']}",
        "#Click# 60",
    ]
    
    for instr in instr_list:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = instr
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        
    """
    #Answer# $175.40
    """
    print(field_dict)
    while True:
        obs_info = state_info["info"]["observation_metadata"]["text"]
        dom_tree, nodes_info = obs_info["dom_info"]["dom_tree"], obs_info["obs_nodes_info"]
        target_action = input()
        if target_action == 'noop':
            break
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
    