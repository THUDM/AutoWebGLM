import json
import re
from pathlib import Path
from typing import Any, TypedDict

from browser_env import Action, ActionParsingError, Trajectory
from browser_env.env_config import URL_MAPPINGS
from browser_env.utils import StateInfo
from llms import lm_config
from llms.tokenizers import Tokenizer
from llms.utils import APIInput


class Instruction(TypedDict):
    """Instruction for constructing prompt"""

    intro: str
    examples: list[tuple[str, str]]
    template: str
    meta_data: dict[str, Any]


class PromptConstructor(object):
    def __init__(
        self,
        instruction_path: str | Path,
        lm_config: lm_config.LMConfig,
        tokenizer: Tokenizer,
    ):
        self.instruction_path = Path(instruction_path)
        self.obs_modality = "text"
        self.lm_config = lm_config
        instruction = json.load(open(self.instruction_path))
        instruction["examples"] = [tuple(e) for e in instruction["examples"]]
        self.instruction: Instruction = instruction
        self.tokenizer = tokenizer

    def get_lm_api_input(
        self, intro: str, examples: list[tuple[str, str]], current: str
    ) -> APIInput:

        """Return the require format for an API"""
        message: list[dict[str, str]] | str
        if "openai" in self.lm_config.provider:
            if self.lm_config.mode == "chat":
                message = [{"role": "system", "content": intro}]
                for (x, y) in examples:
                    message.append(
                        {
                            "role": "system",
                            "name": "example_user",
                            "content": x,
                        }
                    )
                    message.append(
                        {
                            "role": "system",
                            "name": "example_assistant",
                            "content": y,
                        }
                    )
                message.append({"role": "user", "content": current})
                return message
            elif self.lm_config.mode == "completion":
                message = f"{intro}\n\n"
                message += "Here are a few examples:\n"
                for example in examples:
                    message += f"Observation\n:{example[0]}\n\n"
                    message += f"Action: {example[1]}\n\n"
                message += "Now make prediction given the observation\n\n"
                message += f"Observation\n:{current}\n\n"
                message += "Action:"
                return message
            else:
                raise ValueError(
                    f"OpenAI models do not support mode {self.lm_config.mode}"
                )
        elif "huggingface" in self.lm_config.provider:
            # https://huggingface.co/blog/llama2#how-to-prompt-llama-2
            # https://github.com/facebookresearch/llama/blob/main/llama/generation.py#L320
            if "Llama-2" in self.lm_config.model:
                if self.lm_config.mode == "chat":
                    B_INST, E_INST = "[INST]", "[/INST]"
                    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
                    BOS, EOS = "<s>", "</s>"
                    # adding the system message to be the starting of the first example
                    examples = [
                        (
                            B_SYS + intro + E_SYS + examples[0][0],
                            examples[0][1],
                        )
                    ] + examples[1:]
                    message = "".join(
                        [
                            f"{BOS}{B_INST} {x.strip()} {E_INST} {y.strip()} {EOS}"
                            for (x, y) in examples
                        ]
                    )
                    # add the current observation
                    message += f"{BOS}{B_INST} {current.strip()} {E_INST} {self.instruction['meta_data'].get('force_prefix', '')}"

                    return message
                else:
                    raise ValueError("Only chat mode is supported for Llama-2")
            else:
                raise ValueError(
                    f"Huggingface models do not support model_tag {self.lm_config.gen_config['model_tag']}"
                )
        elif "ours" in self.lm_config.provider:
            message = f"{intro}\n\n"
            message += "Now make prediction given the observation\n\n"
            message += f"Observation\n:{current}\n\n"
            message += "Action:"
            return message
        else:
            raise NotImplementedError(
                f"Provider {self.lm_config.provider} not implemented"
            )

    def construct(
        self,
        trajectory: Trajectory,
        intent: str,
        meta_data: dict[str, Any] = {},
    ) -> APIInput:
        raise NotImplementedError

    def map_url_to_real(self, url: str) -> str:
        """Map the urls to their real world counterparts"""
        for i, j in URL_MAPPINGS.items():
            if i in url:
                url = url.replace(i, j)
        return url

    def map_url_to_local(self, url: str) -> str:
        """Map the urls to their local counterparts"""
        for i, j in URL_MAPPINGS.items():
            if j in url:
                url = url.replace(j, i)
            # https
            if j.replace("http", "https") in url:
                url = url.replace(j.replace("http", "https"), i)
        return url

    def _extract_action(self, response: str) -> str:
        raise NotImplementedError

    def extract_action(self, response: str) -> str:
        response = self._extract_action(response)
        response = self.map_url_to_local(response)
        return response


class DirectPromptConstructor(PromptConstructor):
    """The agent will direct predict the action"""

    def __init__(
        self,
        instruction_path: str | Path,
        lm_config: lm_config.LMConfig,
        tokenizer: Tokenizer,
    ):
        super().__init__(instruction_path, lm_config, tokenizer)

    def construct(
        self,
        trajectory: Trajectory,
        intent: str,
        meta_data: dict[str, Any] = {},
    ) -> APIInput:
        """Construct prompt given the trajectory"""
        intro = self.instruction["intro"]
        examples = self.instruction["examples"]
        template = self.instruction["template"]
        keywords = self.instruction["meta_data"]["keywords"]
        state_info: StateInfo = trajectory[-1]  # type: ignore[assignment]

        obs = state_info["observation"][self.obs_modality]
        max_obs_length = self.lm_config.gen_config["max_obs_length"]
        if max_obs_length:
            obs = self.tokenizer.decode(self.tokenizer.encode(obs)[:max_obs_length])  # type: ignore[arg-type]

        page = state_info["info"]["page"]
        url = page.url
        previous_action_str = meta_data["action_history"][-1]

        # input x
        current = template.format(
            objective=intent,
            url=self.map_url_to_real(url),
            observation=obs,
            previous_action=previous_action_str,
        )

        # make sure all keywords are replaced
        assert all([f"{{k}}" not in current for k in keywords])
        prompt = self.get_lm_api_input(intro, examples, current)
        return prompt

    def _extract_action(self, response: str) -> str:
        action_splitter = self.instruction["meta_data"]["action_splitter"]
        pattern = rf"{action_splitter}((.|\n)*?){action_splitter}"
        match = re.search(pattern, response)
        if match:
            return match.group(1).strip()
        else:
            raise ActionParsingError(
                f"Cannot parse action from response {response}"
            )


class CoTPromptConstructor(PromptConstructor):
    """The agent will perform step-by-step reasoning before the answer"""

    def __init__(
        self,
        instruction_path: str | Path,
        lm_config: lm_config.LMConfig,
        tokenizer: Tokenizer,
    ):
        super().__init__(instruction_path, lm_config, tokenizer)
        self.answer_phrase = self.instruction["meta_data"]["answer_phrase"]

    def construct(
        self,
        trajectory: Trajectory,
        intent: str,
        meta_data: dict[str, Any] = {},
    ) -> APIInput:
        intro = self.instruction["intro"]
        examples = self.instruction["examples"]
        template = self.instruction["template"]
        keywords = self.instruction["meta_data"]["keywords"]
        state_info: StateInfo = trajectory[-1]  # type: ignore[assignment]

        obs = state_info["observation"][self.obs_modality]
        max_obs_length = self.lm_config.gen_config["max_obs_length"]
        if max_obs_length:
            obs = self.tokenizer.decode(self.tokenizer.encode(obs)[:max_obs_length])  # type: ignore[arg-type]

        page = state_info["info"]["page"]
        url = page.url
        previous_action_str = meta_data["action_history"][-1]
        current = template.format(
            objective=intent,
            url=self.map_url_to_real(url),
            observation=obs,
            previous_action=previous_action_str,
        )

        assert all([f"{{k}}" not in current for k in keywords])

        prompt = self.get_lm_api_input(intro, examples, current)
        return prompt

    def _extract_action(self, response: str) -> str:
        # find the first occurence of action
        action_splitter = self.instruction["meta_data"]["action_splitter"]
        pattern = rf"{action_splitter}((.|\n)*?){action_splitter}"
        match = re.search(pattern, response)
        if match:
            return match.group(1).strip()
        else:
            raise ActionParsingError(
                f'Cannot find the answer phrase "{self.answer_phrase}" in "{response}"'
            )

class MyPromptConstructor(PromptConstructor):
    """The agent will perform step-by-step reasoning before the answer"""
    operation = [
        r"#?(Click)#?\s*([0-9]+)",
        r"#?(Type)#?\s*([0-9]+)\s+[\'\"]{0,1}([\s\S]+)[\'\"]{0,1}",
        r"#?(Select)#?\s*([0-9]+)\s+[\'\"]{0,1}(.+)[\'\"]{0,1}",
        r"#?(Scroll_up)#?",
        r"#?(Scroll_down)#?",
        r"#?(Goto)#?\s*(https?:\/\/[-a-z0-9]+(?:\.[-a-z0-9]+)*\.(?:com|cn|edu|uk)(?:\/[-a-z0-9_:@&?=+,.!/~*'%$]*)?)",
        r"#?(Go_backward)#?",
        r"#?(Go_forward)#?",
        r"#?(Hover)#?\s*([0-9]+)",
        r"#?(Answer)#?\s+(.+)",
        r"#?(Login)#?",
        r"#?(Verify)#?",
        r"#?(Exit)#?",
        r"#?(Record)#?\s+[\'\"]{0,1}(.+)[\'\"]{0,1}",
    ]
    
    translate = [
        "click",
        "type",
        "select",
        "scroll [up]",
        "scroll [down]",
        "goto",
        "go_back",
        "go_forward",
        "hover",
        "stop",
        "stop",
        "stop",
        "stop",
        "record",
    ]

    def __init__(
        self,
        instruction_path: str | Path,
        lm_config: lm_config.LMConfig,
        tokenizer: Tokenizer,
    ):
        super().__init__(instruction_path, lm_config, tokenizer)
        self.answer_phrase = self.instruction["meta_data"]["answer_phrase"]
        self.state = {}

    def construct(
        self,
        trajectory: Trajectory,
        intent: str,
        meta_data: dict[str, Any] = {},
    ) -> APIInput:
        intro = self.instruction["intro"]
        examples = self.instruction["examples"]
        template = self.instruction["template"]
        keywords = self.instruction["meta_data"]["keywords"]
        finale = self.instruction["finale"]
        state_info: StateInfo = trajectory[-1]  # type: ignore[assignment]

        obs = state_info["observation"][self.obs_modality]
        max_obs_length = self.lm_config.gen_config["max_obs_length"]
        if max_obs_length:
            obs = self.tokenizer.decode(self.tokenizer.encode(obs)[:max_obs_length])  # type: ignore[arg-type]

        info = state_info["info"]
        obs_metadata = info["observation_metadata"]["text"]
        nodes = obs_metadata["obs_nodes_info"]
        position_info = obs_metadata["position_info"]
        html_parser = obs_metadata["html_parser"]
        self.nodes = nodes
        
        page = info["page"]
        url = self.map_url_to_real(page.url)
        position_bar = self._get_position_bar(position_info)
        
        history = [f"{ix}. {his}" for his in meta_data["action_history"]]
        if len(history) == 1:
            previous_action_str = "None"
        else:
            previous_action_str = '\n'.join(history[1:])
            
        self.state.update({
            "url": url,
            "html": obs,
            "html_parser": html_parser,
            "segment": "None",
            "operation": "None",
        })
        
        current = template.format(
            objective=intent,
            url=url,
            html=obs,
            position=position_bar,
            previous_action=previous_action_str,
        )

        assert all([f"{{k}}" not in current for k in keywords])

        # prompt = self.get_lm_api_input(intro, examples, current)
        prompt = current + finale
        
        return prompt

    def _extract_action(self, response: str) -> str:
        # find the first occurence of action
        self.state["intention"] = self._extract_intention(response)
        
        for regex, act in zip(self.operation, self.translate):
            match = re.search(regex, response)

            if match:
                m = match.groups()
                if isinstance(m, tuple):
                    exact_act = m[0]
                    param = m[1:]
                else:
                    exact_act = m
                    param = []
                
                param = list(param)
                if act in ['click', 'hover', 'type', 'select']:
                    if len(param) == 0:
                        continue
                    
                    for node_id, node in self.nodes.items():
                        if node['label'] == param[0]:
                            label = param[0]
                            hp = self.state["html_parser"]
                            bid = hp.id_label_converter(label)
                            segment = hp.get_segment(bid)
                            
                            print('[Label]', label, bid, segment)
                            self.state["segment"] = segment
                            #self._extract_segment(self.state["html"], label)
                            if act not in ['select']:
                                param[0] = node_id
                            break
                
                
                if act in ['stop', 'select', 'record']:
                    if len(param) > 0:
                        param[-1] = param[-1].strip("\'\"")
                        
                if act in ['type']:
                    print('In prompt constructer', param[-1])
                    if len(param) > 0:
                        param[-1] = param[-1].strip("\'\"")
                        print(param[-1])
                        if param[-1].endswith('\n'):
                            param[-1] = param[-1][:-1]
                            param.append('1')
                        else:
                            param.append('0')
                    
                command = act
                for p in param:
                    command += f" [{p}]"
                
                print(command)
                return command
            
        raise ActionParsingError(
            f'Cannot find the answer phrase in "{response}"'
        )
    
    @staticmethod
    def _get_position_bar(data):
        position = data.get("position", 0.0)
        page_height = data.get("page_height", 1.0)
        left_bar = '-' * int(position)
        right_bar = '-' * int(max(1, page_height - position))
        return f'[0{left_bar}|{round(position, 1)}{right_bar}{round(page_height, 1)}]'
    
    @staticmethod
    def _extract_intention(response, lang='en'):
        if lang == 'en':
            matches = re.findall(r"#Thinking Process:\s*(.+)\s*#Operation:", response)
            print('[Try to match]', matches)
        else:
            matches = re.findall(r"#思考过程: (.+)", response)

        if matches:
            return matches[-1]
        else:
            return None
    
    @staticmethod
    def _extract_segment(html: str, tag: str):
        tag = f'[{tag}]'
        has_content = False

        def _left(html, start):
            nonlocal has_content
            left_cnt, right_cnt = 0, 0
            for i in range(start, -1, -1):
                if html[i] == '<':
                    left_cnt += 1
                elif html[i] == '>':
                    if html[i - 2] != '|' and html[i - 2] != '>':
                        has_content = True
                    right_cnt += 1
                elif html[i] == '|':
                    if html[i + 2] != '<' and html[i + 2] != '>':
                        has_content = True
                if left_cnt == right_cnt + 1:
                    return i
            return -1
        
        def _right(html, start):
            nonlocal has_content
            left_cnt, right_cnt = 0, 0
            for i in range(start, len(html), 1):
                if html[i] == '<':
                    left_cnt += 1
                elif html[i] == '>':
                    if html[i - 2] != '|' and html[i - 2] != '>':
                        has_content = True
                    right_cnt += 1
                elif html[i] == '|':
                    if html[i + 2] != '<' and html[i + 2] != '>':
                        has_content = True
                if left_cnt + 1 == right_cnt:
                    return i + 1
            return -1
        
        tag_start = html.find(tag)

        if tag_start == -1:
            return None
        
        left_bound, right_bound = _left(html, tag_start), _right(html, tag_start)
        while True:
            if left_bound == -1 or right_bound == -1:
                return None

            if has_content:
                break

            else:
                lb, rb = _left(html, left_bound - 1), _right(html, right_bound + 1)
                if lb == -1 or rb == -1:
                    break
                if rb - lb > 150:
                    break
                else:
                    left_bound, right_bound = lb, rb

        segment = html[left_bound:right_bound]

        if len(segment) > 150:
            return segment[:150] + '...>'
        
        return segment
    
class NewASPromptConstructor(PromptConstructor):
    """The agent will perform step-by-step reasoning before the answer"""
    operation = [
        r"(click)\(\s*[\'\"]([A-Z]{1,3})[\'\"]\s*\)",
        r"(type_string)\(\s*[\'\"]([A-Z]{1,3})[\'\"]\s*,\s*[\'\"]([\s\S]+)[\'\"]\s*,\s*(True|False)\s*\)",
        r"(select)\(\s*[\'\"]([A-Z]{1,3})[\'\"]\s*,\s*[\'\"]([\s\S]+)[\'\"]\s*\)",
        r"(scroll_page)\(\s*[\'\"]up[\'\"]\s*\)",
        r"(scroll_page)\(\s*[\'\"]down[\'\"]\s*\)",
        r"(jump_to)\(\s*[\'\"](.+)[\'\"]\s*,\s*(True|False)\s*\)",
        r"(go)\(\s*[\'\"]backward[\'\"]\s*\)",
        r"(go)\(\s*[\'\"]forward[\'\"]\s*\)",
        r"(hover)\(\s*[\'\"]([A-Z]{1,3})[\'\"]\s*\)",
        r"(finish)\(\s*\)",
        r"(finish)\(\s*(.+)\s*\)",
        r"(record)\(\s*[\'\"](.+)[\'\"]\s*\)",
        r"(switch_tab)\([\d]+\)"
    ]
    
    translate = [
        "click",
        "type",
        "select",
        "scroll [up]",
        "scroll [down]",
        "goto",
        "go_back",
        "go_forward",
        "hover",
        "stop",
        "stop",
        "record",
        "page_focus",
    ]

    def __init__(
        self,
        instruction_path: str | Path,
        lm_config: lm_config.LMConfig,
        tokenizer: Tokenizer,
    ):
        super().__init__(instruction_path, lm_config, tokenizer)
        self.answer_phrase = self.instruction["meta_data"]["answer_phrase"]
        self.state = {}

    def construct(
        self,
        trajectory: Trajectory,
        intent: str,
        meta_data: dict[str, Any] = {},
    ) -> APIInput:
        intro = self.instruction["intro"]
        examples = self.instruction["examples"]
        template = self.instruction["template"]
        keywords = self.instruction["meta_data"]["keywords"]
        finale = self.instruction["finale"]
        state_info: StateInfo = trajectory[-1]  # type: ignore[assignment]

        obs = state_info["observation"][self.obs_modality]
        max_obs_length = self.lm_config.gen_config["max_obs_length"]
        if max_obs_length:
            obs = self.tokenizer.decode(self.tokenizer.encode(obs)[:max_obs_length])  # type: ignore[arg-type]

        info = state_info["info"]
        obs_metadata = info["observation_metadata"]["text"]
        nodes = obs_metadata["obs_nodes_info"]
        position_info = obs_metadata["position_info"]
        html_parser = obs_metadata["html_parser"]
        tabs_str = obs_metadata["tab_title"]
        self.nodes = nodes
        
        page = info["page"]
        url = self.map_url_to_real(page.url)
        position_bar = self._get_position_bar(position_info)
        
        history = meta_data["action_history"]
        if len(history) == 1:
            previous_action_str = "None"
        else:
            previous_action_str = '\n'.join(history[1:])
            
        self.state.update({
            "url": url,
            "html": obs,
            "html_parser": html_parser,
            "segment": "None",
            "operation": "None",
        })
        
        current = template.format(
            objective=intent,
            url=url,
            html=obs,
            position=position_bar,
            previous_action=previous_action_str,
            tabs=tabs_str,
        )

        assert all([f"{{k}}" not in current for k in keywords])

        # prompt = self.get_lm_api_input(intro, examples, current)
        prompt = current + finale
        
        return prompt

    def _extract_action(self, response: str) -> str:
        # find the first occurence of action
        # self.state["intention"] = self._extract_intention(response)
        
        for regex, act in zip(self.operation, self.translate):
            match = re.search(regex, response)
            if match:
                m = match.groups()
                if isinstance(m, tuple):
                    exact_act = m[0]
                    param = m[1:]
                else:
                    exact_act = m
                    param = []
                
                print(exact_act, param)
                param = list(param)
                if act in ['click', 'hover', 'type', 'select']:
                    if len(param) == 0:
                        continue
                    
                    for node_id, node in self.nodes.items():
                        if node['label'] == param[0]:
                            label = param[0]
                            hp = self.state["html_parser"]
                            bid = hp.id_label_converter(label)
                            segment = hp.get_segment(bid)
                            
                            print('[Label]', label, bid, segment)
                            self.state["segment"] = segment
                            #self._extract_segment(self.state["html"], label)
                            if act not in ['select']:
                                param[0] = node_id
                            break
                
                if len(param) > 0:
                    if act in ['stop', 'select', 'record']:
                        param[-1] = param[-1].strip("\'\"")
                    if act in ['type', 'goto']:
                        param[-1] = '1' if param[-1] == 'True' else '0'
                    
                command = act
                for p in param:
                    command += f" [{p}]"
                
                print(command)
                return command
            
        raise ActionParsingError(
            f'Cannot find the answer phrase in "{response}"'
        )
    
    @staticmethod
    def _get_position_bar(data):
        position = data.get("position", 0.0)
        page_height = data.get("page_height", 1.0)
        return f"{round(position, 1)} / {round(page_height, 1)}"