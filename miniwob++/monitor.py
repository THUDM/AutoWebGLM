import subprocess
from pathlib import Path
import time
import re
import shutil
import sys, os
import random
import xml.etree.ElementTree as ET
import time
import json
from datetime import datetime

def get_free_gpus():
    while True:
        try:
            # 运行 nvidia-smi 命令，获取GPU信息
            smi_output = subprocess.check_output(['nvidia-smi', '-q', '-x']).decode()
            
            # 解析XML格式的输出
            gpu_info = ET.fromstring(smi_output)
            
            free_gpus = []
            for gpu_id, gpu in enumerate(gpu_info.findall('.//gpu')):
                total_memory = int(gpu.find('fb_memory_usage/total').text.split()[0])
                used_memory = int(gpu.find('fb_memory_usage/used').text.split()[0])
                
                # 检查显存占用是否低于50%
                if used_memory / total_memory < 0.1:
                    free_gpus.append(str(gpu_id))

            # 拼接GPU ID
            if len(free_gpus) > 0:
                return ','.join(free_gpus)
            else:
                print('waiting for free gpu...')
                time.sleep(60)
        
        except Exception as e:
            print(f"Error: {e}")
            return ""

class CheckpointMonitor:
    def __init__(self, checkpoint_dir: str, test_amount: int, keep_num: int):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.test_amount = test_amount
        self.keep_num = keep_num
        self.scores = {}  # 存储checkpoint目录路径和它们的分数
        if os.path.exists(self.checkpoint_dir / 'scores.json'):
            self.scores = json.load(open(self.checkpoint_dir / 'scores.json'))

    def evaluate_checkpoint(self, checkpoint_dir: Path) -> float:
        # 遍历testset目录，并找出所有包含test.json的文件夹
        result = {}
        
        free_gpus = get_free_gpus()
        print('runing evaluation on checkpoint: ', checkpoint_dir)
        print('use gpus: ', free_gpus)
        # cmd = f'python main.py {free_gpus} {self.test_amount} {str(checkpoint_dir)} {str(checkpoint_dir / "miniwobxx-test")}'
        # 调用auto_eval.sh脚本并获取输出
        output = subprocess.run(["python", "main.py", free_gpus, str(self.test_amount), str(checkpoint_dir), str(checkpoint_dir / "miniwobxx-test")], capture_output=True, text=True)
        output = output.stderr.strip().split('\n')[-1]

        try:
            score = float(output.split(' ')[-1])
            result['average'] = score
        except:
            print(f"Error: {output}")
            return None
        
        return result

    def update_top_checkpoints(self):
        if self.keep_num == -1:
            return
        print('updating top checkpoints...')
        # 取出keep_num之外的checkpoint
        out_checkpoints = sorted(self.scores.items(), key=lambda x: x[1]['average'], reverse=True)[self.keep_num:]
        out_checkpoints = {item[0]: item[1]['average'] for item in out_checkpoints}
        print('delete checkpoint:', out_checkpoints)
        # 删除out_checkpoints
        for path, score in out_checkpoints.items():
            if os.path.exists(path) and os.path.isdir(path):
                shutil.rmtree(path)

    def evaluate_and_update(self, checkpoint_dir):
        # 评估并更新checkpoint目录
        if checkpoint_dir.is_dir() and checkpoint_dir not in self.scores:
            print(f"evaluating new directory: {checkpoint_dir}")
            result = self.evaluate_checkpoint(checkpoint_dir)
            self.scores[str(checkpoint_dir)] = result
            open(self.checkpoint_dir / 'scores.json', 'w').write(json.dumps(self.scores, indent=4))
            self.update_top_checkpoints()
            
    def del_training_state(self):
        sorted_dir = [x for x in self.checkpoint_dir.iterdir() if x.is_dir()]
        sorted_dir.sort(key=lambda x: int(''.join(c for c in x.name if c.isdigit())))
        for existing_dir in sorted_dir[:-1]:
            step = int(''.join(c for c in existing_dir.name if c.isdigit()))
            state_dir = existing_dir / f'global_step{step}'
            if existing_dir.is_dir() and state_dir.exists():
                print('deleting training state: ', state_dir)
                shutil.rmtree(state_dir)
        
    def monitor(self):
        # 删除多余训练状态
        self.del_training_state()
        # 评估已存在且没有被评测的checkpoint
        sorted_dir = [x for x in self.checkpoint_dir.iterdir() if x.is_dir()]
        sorted_dir.sort(key=lambda x: int(''.join(c for c in x.name if c.isdigit())))
        for existing_dir in sorted_dir:
            if existing_dir.is_dir() and str(existing_dir) not in self.scores:
                print(f"evaluating existing directory: {existing_dir}")
                result = self.evaluate_checkpoint(existing_dir)
                self.scores[str(existing_dir)] = result
                open(self.checkpoint_dir / 'scores.json', 'w').write(json.dumps(self.scores, indent=4))
        
        self.update_top_checkpoints()
        
        # 监听checkpoint目录的创建事件
        while True:
            # 删除多余训练状态
            self.del_training_state()
            for new_dir in self.checkpoint_dir.iterdir():
                if new_dir.is_dir() and str(new_dir) not in self.scores:
                    print('find new directory: ', new_dir, 'wait to evaluate...')
                    time.sleep(60) # 等待模型ckpt存储
                    self.evaluate_and_update(new_dir)
            
            print('watching...')
            time.sleep(60)  # 持续监听

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python monitor.py <checkpoint_directory> <test-amount> <remain_ckpt, -1 for keep all, default to 5>")
        sys.exit(1)
        
    checkpoint_directory = sys.argv[1]
    test_amount = int(sys.argv[2])
    keep_num = int(sys.argv[3]) if len(sys.argv) == 4 else 5
    monitor = CheckpointMonitor(checkpoint_directory, test_amount, keep_num)
    monitor.monitor()