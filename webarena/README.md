# Modified WebArena evaluation

We modified the configuration in WebArena to add our unique simplification method to improve the speed of the evaluation.

The following content is inherited from the WebArena repository, and we've only modified some of the test commands and prompt formats.

## Install

```bash
# Python 3.10+
conda create -n webarena python=3.10; conda activate webarena
pip install -r requirements.txt
playwright install
pip install -e .

# optional, dev only
pip install -e ".[dev]"
mypy --install-types --non-interactive browser_env agents evaluation_harness
pip install pre-commit
pre-commit install
```
## End-to-end Evaluation

1. Setup the standalone environment.
Please check out [this page](environment_docker/README.md) for details.

2. Configurate the urls for each website.
```bash
export SHOPPING="<your_shopping_site_domain>:7770"
export SHOPPING_ADMIN="<your_e_commerce_cms_domain>:7780/admin"
export REDDIT="<your_reddit_domain>:9999"
export GITLAB="<your_gitlab_domain>:8023"
export MAP="<your_map_domain>:3000"
export WIKIPEDIA="<your_wikipedia_domain>:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
export HOMEPAGE="<your_homepage_domain>:4399" # this is a placeholder
```

> You are encouraged to update the environment variables in [github workflow](.github/workflows/tests.yml#L7) to ensure the correctness of unit tests

3. Generate config file for each test example
```bash
python scripts/generate_test_data.py
```
You will see `*.json` files generated in [config_files](./config_files) folder. Each file contains the configuration for one test example.

4. Obtain the auto-login cookies for all websites
```
mkdir -p ./.auth
python browser_env/auto_login.py
```
5. export `OPENAI_API_KEY=your_key`, a valid OpenAI API key starts with `sk-`

6. Launch the evaluation
```bash
python run.py \
  --instruction_path agent/prompts/jsons/new_action_prompt.json \ # this is the reasoning agent prompt we used in the paper
  --model gpt-3.5-turbo \
  --mode completion \
  --observation_type html \
  --action_set_tag id_html_nasc_tree \
  --result_dir <your_result_dir> \
  --test_start_idx 0 \
  --test_end_idx 1 \
```
This script will run the first example with GPT-3.5 reasoning agent. The trajectory will be saved in `<your_result_dir>/0.html`

## Develop Your Prompt-based Agent
1. Define the prompts. We provide two baseline agents whose correrponding prompts are listed [here](./agent/prompts/raw). Each prompt is a dictionary with the following keys:
```python
prompt = {
  "intro": <The overall guideline which includes the task description, available action, hint and others>,
  "examples": [
    (
      example_1_observation,
      example_1_response
    ),
    (
      example_2_observation,
      example_2_response
    ),
    ...
  ],
  "template": <How to organize different information such as observation, previous action, instruction, url>,
  "meta_data": {
    "observation": <Which observation space the agent uses>,
    "action_type": <Which action space the agent uses>,
    "keywords": <The keywords used in the template, the program will later enumerate all keywords in the template to see if all of them are correctly replaced with the content>,
    "prompt_constructor": <Which prompt construtor is in used, the prompt constructor will construct the input feed to an LLM and extract the action from the generation, more details below>,
    "action_splitter": <Inside which splitter can we extract the action, used by the prompt constructor>
    }
  }
```

2. Implement the prompt constructor. An example prompt constructor using Chain-of-thought/ReAct style reasoning is [here](./agent/prompts/prompt_constructor.py#L184). The prompt constructor is a class with the following methods:
* `construct`: construct the input feed to an LLM
* `_extract_action`: given the generation from an LLM, how to extract the phrase that corresponds to the action