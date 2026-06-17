# MAS_TL_STAP：基于时序逻辑的多智能体协同任务分配与规划

本仓库为一项关于**线性时序逻辑（LTL）约束下多智能体协同任务规划**的研究项目。给定 LTL 任务公式，本框架能够自动分解任务、为多智能体系统分配协作性子任务，并保证规划结果的渐进最优性。

## 概述

本项目旨在解决异构多智能体系统中的**任务分配与运动规划联合优化**问题。整体技术路线如下：

```
LTL 任务公式  →  Büchi 自动机  →  偏序集（Poset） →  最优分配（B&B / MILP） →  运动规划
```

核心功能：
- **LTL 到 Büchi 自动机的转换**：将 LTL 任务规范翻译为 Büchi 自动机。
- **基于偏序集的任务分解**：构建偏序集以刻画子任务之间的时序约束关系。
- **分支定界（B&B）求解器**：高效的组合优化方法，用于求解任务到智能体的最优分配。
- **MILP 求解器**：混合整数线性规划形式化，可求全局最优解。
- **运动规划**：基于栅格地图的路径规划（A*、Dijkstra），为智能体生成执行任务的运动轨迹。
- **可视化**：支持甘特图、轨迹图和视频导出，便于定性分析。

## 项目结构

```
Project_001/
├── scripts/
│   ├── MAS_TL_STAP/           # 核心库
│   │   ├── LTL2BA/            # LTL 公式 → Büchi 自动机转换
│   │   │   ├── boolean_formulas/  # 布尔公式的词法/语法解析器
│   │   │   ├── gltl2ba.py     # LTL 转 Büchi 封装接口
│   │   │   └── __init__.py
│   │   ├── buchi.py           # Büchi 自动机构建
│   │   ├── poset_builder.py   # 从 Büchi 自动机生成偏序集
│   │   ├── poset_product.py   # 偏序集乘积运算
│   │   ├── B_A_B2.py          # 分支定界算法
│   │   ├── planner.py         # BnB 搜索 & MILP 求解器
│   │   ├── agent.py           # 智能体模型
│   │   ├── motion.py          # 运动规划（栅格地图、Dijkstra）
│   │   ├── system.py          # 多智能体系统定义
│   │   ├── ltl4planner.py     # LTL 到规划器的接口
│   │   ├── product.py         # 乘积自动机
│   │   └── utils.py           # 工具函数
│   ├── run_case_1.py           # 实验运行主入口
│   └── test_code/             # 测试与演示脚本
├── scenes/                    # 场景定义文件（YAML，共6个场景）
├── figures/                   # 输出图片与地图图像
└── LICENSE                    # 许可证文件
```

## 快速开始

### 环境依赖

- Python ≥ 3.8
- 所需包：`numpy`、`networkx`、`matplotlib`、`cvxpy`、`Pillow`、`pyyaml`

### 安装

```bash
git clone git@github.com:KaileZhu/Project_001.git
cd Project_001
pip install numpy networkx matplotlib cvxpy Pillow pyyaml
```

### 运行实验

```bash
cd scripts
python run_case_1.py
```

默认使用 B&B 求解器运行场景 `06`。可在 `__main__` 代码块中修改 `scene_index` 的范围和 `opt_method` 参数（`'BnB'` 或 `'MILP'`）来运行不同的配置。

## 输出结果

框架输出以下内容：
- **任务分析耗时**（偏序集构建时间）
- **求解耗时**（B&B 或 MILP）
- **总任务完成时间**（makespan）
- **甘特图**：展示各智能体的调度计划（`figures/demo_XX_gantt.png`）
- **轨迹图**：展示各智能体在地图上的运动路径（`figures/demo_XX.png`）

## 作者

- **Junjie Wang** — pkuwjj1998@163.com
- Zesen Liu
- Yunyi Zhang
- Qisheng Zhao
- Shuo Zhang

## 引用

如果您的研究使用了本工作，请引用对应的学术论文。

## 许可证

本项目遵循 [LICENSE](LICENSE) 文件中的许可条款。
