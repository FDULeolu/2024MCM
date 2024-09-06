import os
import yaml
from datetime import datetime
import pandas as pd

# 保存 strategy 和 product_info 到 yml 文件
def save_strategy_and_product_info(strategy, product_info, folder_path):
    strategy_file_name = "strategy_product_info.yml"
    strategy_file_path = os.path.join(folder_path, strategy_file_name)
    
    # 创建要保存的数据
    data = {
        'strategy': strategy,
        'product_info': product_info
    }

    # 将数据保存为 .yml 文件
    with open(strategy_file_path, 'w') as file:
        yaml.dump(data, file)
    
    print(f"Strategy and product info saved to {strategy_file_path}")

# 保存 result 字典为 CSV 文件
def save_result_to_csv(result, folder_path):
    result_file_name = "result.csv"
    result_file_path = os.path.join(folder_path, result_file_name)

    # 将字典转换为 DataFrame
    df = pd.DataFrame(result)

    # 保存 DataFrame 为 CSV 文件
    df.to_csv(result_file_path, index=False)

    print(f"Results saved to {result_file_path}")

def load_strategies_from_yaml(file_name):
    # 读取 YAML 文件
    with open(file_name, 'r') as file:
        strategies = yaml.safe_load(file)
    return strategies

# 读取 YAML 文件
def load_situation(file_name):
    with open(file_name, 'r') as file:
        return yaml.safe_load(file)