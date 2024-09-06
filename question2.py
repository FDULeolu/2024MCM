from part import *
from factory import *
from tqdm import tqdm
from utils import *

N = 10000   # 采购零配件数量


def run(product_info, strategy):

    warehouse = WareHouse(product_info)
    factory = Factory(warehouse)

    # 购买零件
    factory.buy_parts('part1', N)
    factory.buy_parts('part2', N)

    while not factory.stop_manu(['part1', 'part2']):
        # 是否检测零件1和零件2
        if strategy[0][0]:
            factory.check_batch('part1')
        if strategy[0][0]:
            factory.check_batch('part2')

        # 装配
        factory.assemble(['part1', 'part2'], 'product1')

        # 是否检测产品，对于不合格产品是否拆解
        if strategy[1] and strategy[2]:
            factory.check_batch('product1', True)
        elif strategy[1] and not strategy[2]:
            factory.check_batch('product1')

        # 出售并记录不合格产品
        factory.sell('product1')

        # 是否拆解不合格产品，若不拆解，直接丢弃
        if strategy[2]:
            factory.disassemble_batch('product1')
        else:
            factory.drop_product('product1')


    # 若最终的合格产品数量小余客户数量，用平均成本补齐
    factory.after_sale_service('product1')

    # factory.print_result()
    return factory.result()


strategies = load_strategies_from_yaml('Q2strategies.yml')
situations = load_situation('Q2situation.yml')

base_folder = 'question2'
if not os.path.exists(base_folder):
    os.makedirs(base_folder)


for id, info in situations.items():

    situation_folder = os.path.join(base_folder, f"situation_{id}")
    os.makedirs(situation_folder, exist_ok=True)

    for i in range(len(strategies)):

        strategy_folder = os.path.join(situation_folder, f"strategy_{i}")
        strategy = strategies[i]
        result = []

        for _ in tqdm(range(200)):
            result.append(run(info, strategy))

        os.makedirs(strategy_folder, exist_ok=True)
        # 保存 strategy 和 product_info 到子文件夹中的 .yml 文件
        save_strategy_and_product_info(strategy, info, strategy_folder)

        # 保存 result 到子文件夹中的 CSV 文件
        save_result_to_csv(result, strategy_folder)

# product_info = {
#             'part1':{
#                 'fail_rate': 0.1,
#                 'unit_cost': 4,
#                 'check_cost': 2
#             },
#             'part2':{
#                 'fail_rate': 0.1,
#                 'unit_cost': 18,
#                 'check_cost': 3
#             },
#             'product1':{
#                 'fail_rate': 0.1,
#                 'assemble_cost': 6,
#                 'check_cost': 3,
#                 'market_value': 56,
#                 'exchange_cost': 6,
#                 'disassemble_cost': 5
#             }}

# strategy = [
#     [1, 1],
#     1,
#     1
# ]

# result = []
# for i in tqdm(range(1000)):
#     result.append(run(product_info, strategy))

# base_folder = 'question2'
# if not os.path.exists(base_folder):
#     os.makedirs(base_folder)

# 创建一个以时间戳为名称的子文件夹
# timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# timestamp_folder = os.path.join(base_folder, timestamp)
# os.makedirs(timestamp_folder)

