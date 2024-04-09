# MiniWoB++

## Usage

```shell
pip install -r requirement.txt
python main.py [cudas] [test-amount] [model-path] [result-path]
```

### Parameter Description

| Parameter   | Format       | Mandatory | Use                                                        |
| ----------- | ------------ | --------- | ---------------------------------------------------------- |
| cudas       | 0,1,2        | Yes       | The GPU number to be used, separated by commas, no spaces  |
| test-amount | 10           | Yes       | Number of test cases per task, the paper uses 100, but generally, 10 groups are more reasonable for efficiency |
| model-path  | model_path/  | Yes       | Path to the model to be tested, if set to 'manual' then manual execution can be performed |
| result-path | result/      | Yes       | Location for the model's output (Tasks that have been completed in the same path **will not** be executed again) |

## Results

After running the above command, you should see a `log_files` folder appear in the current directory. The `**.log` files inside are the run results. When a task is completed, you should see the following output, where the result represents the test case score, which can be 0 or 1:

```sh
2023-11-30 06:28:13,283 - INFO - {"task": "click-button", "case_id": 10, "result": 1.0}
```

When all test cases for a group of tasks have been run, the following record will be output in the log:

```sh
2023-11-30 07:10:13,593 - INFO - {"task": "grid-coordinate", "avg_score": 0.3}
```

When all tasks in a process are completed, the log will record the following information:

```sh
2023-11-30 07:10:13,836 - INFO - ------
2023-11-30 07:10:13,836 - INFO - click-button-sequence            1.00
2023-11-30 07:10:13,836 - INFO - click-checkboxes                 0.62
2023-11-30 07:10:13,837 - INFO - click-checkboxes-large           0.07
2023-11-30 07:10:13,837 - INFO - click-color                      0.24
... (50 lines omitted)
2023-11-30 07:10:13,839 - INFO - enter-date                       1.00
2023-11-30 07:10:13,839 - INFO - grid-coordinate                  0.30
2023-11-30 07:10:13,839 - INFO - all                             0.442
```
