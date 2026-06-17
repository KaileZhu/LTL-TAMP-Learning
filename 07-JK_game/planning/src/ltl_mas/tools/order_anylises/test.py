###############################################################################

# Required Libraries
import numpy as np
import matplotlib.pyplot as plt

# Fuzzy TOPSIS
from py_decisions.topsis.fuzzy_topsis import fuzzy_topsis_method

# Fuzzy VIKOR
from py_decisions.vikor.fuzzy_vikor import fuzzy_vikor_method

def change_list(dataset):
    All_list =[]
    for newlist in dataset:
        nochange =newlist[:2]
        new_tuple_list =[]
        for num in range(len(newlist[0])):
            if newlist[2][num]>=newlist[3][num]:
                new_tuple_list.append(newlist[2][num])
            else:
                new_tuple_list.append(newlist[3][num])

        new_tuple_list =tuple(new_tuple_list)
        nochange.append(new_tuple_list)
        All_list.append(nochange)
    return All_list
##############################################################################

# Fuzzy TOPSIS

# Weigths
weights = list([
    [(0.1, 0.2, 0.3), (0.7, 0.8, 0.9), (0.3, 0.5, 0.8)]
])

# Load Criterion Type: 'max' or 'min'
criterion_type = ['max', 'max', 'min']

# Dataset
dataset = list([
    [(3, 6, 9), (5, 8, 9), (5, 7, 9),(9,3,1)],  # a1
    [(5, 7, 9), (3, 7, 9), (3, 5, 7),(4,3,8)],  # a2
    [(5, 8, 9), (3, 5, 7), (1, 2, 3),(2,2,5)],  # a3
    [(1, 2, 4), (1, 4, 7), (1, 2, 5),(6,4,7)]  ,
    [(1, 2, 400), (1, 4, 7), (1, 2, 5),(6,4,7)]  # a4
])

All_list =change_list(dataset)

# Call Fuzzy TOPSIS
#relative_closeness = fuzzy_topsis_method(All_list, weights, criterion_type, graph=False)
relative_closeness = fuzzy_topsis_method(dataset, weights, criterion_type, graph=False)
print(relative_closeness)
##############################################################################

# Fuzzy VIKOR

# Weigths
weights = list([
    [(0.1, 0.2, 0.3), (0.7, 0.8, 0.9), (0.3, 0.5, 0.8)]
])

# Load Criterion Type: 'max' or 'min'
criterion_type = ['max', 'max', 'min']

# Dataset
dataset = list([
    [(3, 6, 9), (5, 8, 9), (5, 7, 9),(2,5,2)],  # a1
    [(5, 7, 9), (3, 7, 9), (3, 5, 7),(5,2,8)],  # a2
    [(5, 8, 9), (3, 5, 7), (1, 2, 3),(7,2,3)],  # a3
    [(1, 2, 4), (1, 4, 7), (1, 2, 5),(9,8,1)]  # a4
])
All_list =change_list(dataset)

# Call Fuzzy VIKOR
s, r, q, c_solution = fuzzy_vikor_method(All_list, weights, criterion_type, strategy_coefficient=0.5, graph=True)




##############################################################################