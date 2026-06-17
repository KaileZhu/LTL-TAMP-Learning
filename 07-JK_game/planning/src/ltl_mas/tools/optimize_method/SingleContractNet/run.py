#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ContractNet_pkg.simulation import Simulation
import ContractNet_pkg.experiments as ep

def Run():
    print("sim starts\n")

    # 定义仿真案例，进行合同网算法仿真
    sim = Simulation(ep.case_1)
    sim.contractNet_algorithm()

    print("sim ends\n")

    # 获取任务分配结果 solution
    solution = sim.return_solution()

    return solution