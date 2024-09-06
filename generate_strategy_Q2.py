import yaml
import itertools

def generate_all_strategies():
    # 生成所有可能的 0 和 1 的组合
    combinations = list(itertools.product([0, 1], repeat=4))

    # 将每个组合转换为需要的策略格式
    strategies = []
    for comb in combinations:
        strategy = [
            [comb[0], comb[1]],  # 对应 [strategy[0][0], strategy[0][1]]
            comb[2],             # 对应 strategy[1]
            comb[3]              # 对应 strategy[2]
        ]
        strategies.append(strategy)
    
    return strategies

# 生成所有可能的策略
all_strategies = generate_all_strategies()

# 保存策略到 YAML 文件
file_name = "Q2strategies.yaml"
with open(file_name, 'w') as file:
    yaml.dump(all_strategies, file)

print(f"All strategies saved to {file_name}")