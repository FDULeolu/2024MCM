from utils import *

strategy = load_strategies_from_yaml('Q2strategies.yml')
situation = load_situation('Q2situation.yml')
print(strategy, situation)
for i in strategy:
    print(i)
for key, value in situation.items():
    print(key, value)