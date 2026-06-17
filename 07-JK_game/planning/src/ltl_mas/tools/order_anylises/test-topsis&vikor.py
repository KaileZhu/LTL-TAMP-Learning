# Required Libraries
import numpy as np
import pandas as pd

# 将py_decisions设置为Sources Root
from src.ltl_mas.tools.order_anylises.py_decisions.topsis.topsis import topsis_method
from src.ltl_mas.tools.order_anylises.py_decisions.vikor.vikor import vikor_method

if __name__ == '__main__':
    data = pd.read_csv('data.csv')  # 数据集
    dataset = data.iloc[:, 1:4]  # 指标列1,2,3
    # 指标权重
    ws = np.array([[0.6370, 0.2583, 0.1047]])  # 主观权重
    wo = np.array([[0.5786, 0.3762, 0.0452]])  # 客观权重
    weights = np.array([[0.7834, 0.2065, 0.0101]])  # 综合权重
    criterion_type = ['max', 'max', 'max']  # 指标类型:极大极小型

    # W-TOPSIS（使用熵权法得到的客观权重）
    print('W-TOPSIS')
    relative_closeness = topsis_method(dataset, wo, criterion_type, graph=False)
    # VIKOR 使用综合权重
    print('CW-VIKOR')
    s, r, q, c_solution = vikor_method(dataset, weights, criterion_type, strategy_coefficient=0.5, graph=False)


    # 存储
    df = pd.DataFrame(data, columns=['TOPSIS', 'VIKOR'])
    df['TOPSIS'] = relative_closeness
    df['VIKOR'] = c_solution
    df.to_csv('TOPSIS_VIKOR.csv')
