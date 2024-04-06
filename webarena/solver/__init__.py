from .utils import step_once, show_screenshot

from browser_env import (
    StateInfo,
    Trajectory,
)

from .shopping_admin import *

def manual_solver(env, config_file, render_helper, agent, args, intent, field_dict):
    # return solver_364(env, config_file, render_helper, agent, args, intent, field_dict)
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
        res = step_once(env, trajectory, render_helper, traces, state_info, agent, args, intent, meta_data, target_action)
        if res is None:
            return traces, trajectory
        state_info, dom_tree, nodes_info = res
        