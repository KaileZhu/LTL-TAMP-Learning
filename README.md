# LTL-TAMP-Learning

基于**线性时序逻辑（Linear Temporal Logic, LTL）的多智能体任务与运动规划（Task and Motion Planning, TAMP）** 学习仓库。

本仓库汇总了 LTL-TAMP 方向从理论学习、上游代码研读、通用 Baseline 构建到多个应用项目的完整研发历程，旨在为后续进入该方向的研究者提供一站式的学习与开发基础。

---

## 目录

- [仓库结构](#仓库结构)
- [学习路径](#学习路径)
- [Baseline 说明](#baseline-说明)
- [各项目说明](#各项目说明)
- [上游依赖](#上游依赖)
- [环境配置](#环境配置)
- [快速开始](#快速开始)
- [论文与引用](#论文与引用)
- [作者](#作者)
- [许可证](#许可证)

---

## 仓库结构

```
ltl-tamp-learning/
│
├── 01-学习路径/                          # 入门路线图与讨论记录
│   ├── 学习路径说明.txt                  # 从零到一的学习路线
│   └── LTG_20230911.pdf                 # 讨论组交流记录
│
├── 02-视频教程/                          # 讲座视频
│   └── Motion and Task Planning.MP4     # LTL-TAMP 入门讲座
│
├── 03-论文与书籍/                        # 经典教材与论文
│   ├── Planning Algorithms (LaValle 2006).pdf
│   ├── Principles of Model Checking.pdf
│   ├── Hybrid Control of Multi-robot Systems (博士论文).pdf
│   ├── Task and Motion Planning.pdf
│   ├── Formal Methods for Discrete-Time Dynamical Systems.pdf
│   ├── Formal Methods for Dynamic Systems (殷翔).pdf
│   ├── Simultaneous Task Allocation and Planning for Temporal Logic Goals....pdf
│   ├── Multi-agent Coordination Under Temporal Logic Tasks....pdf
│   ├── A Comprehensive Taxonomy for Multi Task Allocation.pdf
│   └── TMOS-相关/                       # TMOS 子方向专题
│       ├── TMOS.pdf
│       ├── Time Minimization and Online Synchronization.pdf
│       ├── ral在投.pdf
│       └── 泽森师兄论文汇报.pptx
│
├── 04-上游代码库/                        # 依赖的外部开源代码
│   ├── P_MAS_TG_py3/                    # 郭萌老师 LTL Planner (Python 3)
│   └── P_MAS_TG-py2/                    # 历史版本 (Python 2，留档)
│
├── 05-Baseline/                          # ⭐ 通用 Baseline
│   ├── LTL_MAS_C-action/                # 基于 LTL 的多智能体动作规划核心库
│   │   ├── src/                         #   核心源码
│   │   │   ├── baseline/               #     分支定界等优化方法
│   │   │   ├── ltl_mas/                #     LTL → Büchi → Poset 主流程
│   │   │   └── pywheeltecswarm/        #     可视化/仿真接口
│   │   ├── test/                        #   多场景测试
│   │   ├── data/                        #   输入/输出数据
│   │   ├── visual_env/                  #   可视化仿真环境 (Crazyswarm)
│   │   └── write_up/                    #   论文草稿与投稿版本
│   │
│   └── MILP/                            # 混合整数线性规划求解器
│       ├── scripts/                     #   MILP 形式化与重规划脚本
│       ├── scenes/                      #   场景定义
│       └── figures/                     #   结果图
│
├── 06-Project_MAS_TL_STAP/              # 主项目：多智能体协同任务分配与规划
│   ├── scripts/
│   │   ├── MAS_TL_STAP/                 #   核心库
│   │   │   ├── LTL2BA/                 #     LTL → Büchi 自动机
│   │   │   ├── buchi.py               #     Büchi 自动机构建
│   │   │   ├── poset_builder.py       #     偏序集构建
│   │   │   ├── poset_product.py       #     偏序集乘积
│   │   │   ├── B_A_B2.py              #     分支定界算法
│   │   │   ├── planner.py             #     BnB / MILP 求解器
│   │   │   ├── agent.py               #     智能体模型
│   │   │   ├── motion.py              #     运动规划 (A*, Dijkstra)
│   │   │   ├── system.py              #     多智能体系统
│   │   │   ├── product.py             #     乘积自动机
│   │   │   └── ltl4planner.py         #     LTL → Planner 接口
│   │   ├── run_case_1.py               #   实验主入口
│   │   └── test_code/                  #   测试与演示
│   ├── scenes/                          #   6 个场景定义 (YAML)
│   ├── figures/                         #   输出图与可视化结果
│   └── README.md                        #   详细说明
│
├── 07-JK_game/                           # 博弈决策项目
│   ├── planning/                         #   规划模块
│   │   ├── src/                         #     核心逻辑
│   │   ├── data/                        #     场景数据
│   │   └── test/                        #     测试
│   ├── training/                         #   训练模块 (神经网络)
│   ├── logger/                           #   日志系统
│   ├── CentralServer__master.py          #   后端主控
│   └── README.md                         #   使用说明
│
├── 08-Project_03_online/                 # 在线自适应规划项目
│   ├── scripts/                          #   在线/离线运行脚本
│   │   ├── run_case_online.py           #     在线运行入口
│   │   ├── run_case_from_json_online.py #     JSON 驱动在线运行
│   │   ├── run_case_from_json_offline.py#     JSON 驱动离线运行
│   │   └── MAS_TL_STAP/                 #     复用核心库
│   ├── scenes/                           #   6+ 在线场景
│   ├── 面向多智能体的可解释性脑启发博弈决策架构.pptx  # 答辩PPT
│   ├── 项目实施方案.docx
│   └── Dockerfile                        #   容器化部署
│
├── LICENSE                               # 许可证
└── README.md                             # 本文件
```

---

## 学习路径

推荐按以下顺序入门 LTL-TAMP：

### 第一步：理解 LTL

阅读 **[Principles of Model Checking](03-论文与书籍/Principles%20of%20Model%20Checking.pdf)** 的第 2、3、5 章，掌握 LTL 的语法和语义，之后可作为工具书查阅。

辅助资源：B站网课 [动态系统的形式化分析与控制](https://www.bilibili.com/video/BV12r4y1w7DF/)（殷翔老师）。

### 第二步：理解 LTL + Control

核心读物：**[Hybrid Control of Multi-robot Systems under Complex Temporal Tasks](03-论文与书籍/PhD%20Thesis-Hybrid%20Control%20of%20Multi-robot%20Systems.pdf)**（国老师博士论文），深入浅出地讲解了 LTL 如何与控制系统结合。

论文覆盖了自下而上（bottom-up）和自上而下（top-down）两条技术路线。

### 第三步：上手代码 —— LTL Planner

研读上游代码库 **[P_MAS_TG](04-上游代码库/P_MAS_TG_py3/)**（郭萌老师开源）。

重点关注 `P_MAS_TG/` 目录下的 LTL planner 实现，理解 LTL 公式如何驱动实际的运动规划。

讲座视频 `02-视频教程/Motion and Task Planning.MP4` 也在此阶段观看。

### 第四步：LTL → 偏序集（Poset）

阅读 **[Simultaneous Task Allocation and Planning for Temporal Logic Goals](03-论文与书籍/Simultaneous%20Task%20Allocation%20and%20Planning%20for%20Temporal%20Logic%20Goals%20in%20Heterogeneous%20Multi-Robot%20System.pdf)**（泽森论文）。

复现代码：本仓库的 **[05-Baseline/LTL_MAS_C-action](05-Baseline/LTL_MAS_C-action/)**。

核心管线：

```
LTL 公式 → Büchi 自动机 → 偏序集 → 最优分配 → 运动规划
```

### 第五步：偏序 → 动态决策

研读 **[07-JK_game](07-JK_game/)** 项目，理解博弈算法如何与 LTL 规划结合，以及模糊 TOPSIS 决策在多智能体协同中的应用。

### 第六步：进阶 —— TMOS

阅读 `03-论文与书籍/TMOS-相关/` 下的论文，了解**时间最小化与在线同步（Time Minimization and Online Synchronization）** 的前沿方向。

---

## Baseline 说明

Baseline 是所有项目的公共基础，位于 `05-Baseline/`，包含两大部分：

### Part 1: LTL_MAS_C-action（偏序 + 分支定界）

**功能：** 将 LTL 任务公式自动分解为子任务偏序集，并通过分支定界（Branch & Bound）算法将子任务最优分配给异构多智能体系统。

**核心流程：**

```
LTL 公式 → Büchi 自动机 → 偏序集 (Poset) → B&B/MILP 分配 → 运动规划 → 可视化
```

**四大核心模块：**

| 模块 | 功能 |
|------|------|
| `field` | 生成基础数据（WTS、动作模型等） |
| `Buchi_poset_builder` | 从 Büchi 自动机构建偏序集 |
| `Optimize_method` | 基于 B&B 或 MILP 的最优任务分配 |
| `Agent_swarm` | 多智能体仿真执行与可视化 |

### Part 2: MILP（混合整数线性规划）

**功能：** 提供基于 MILP 形式化的全局最优求解器，支持重规划（replanning）。与 Part 1 的 B&B 方法互补——MILP 可求全局最优解，B&B 适合大规模场景的快速求解。

**使用方式：**

```bash
# 将 Baseline 加入 Python 路径
export PYTHONPATH="$PYTHONPATH:$(pwd)/05-Baseline/LTL_MAS_C-action/src"

# 运行 MILP 求解
cd 05-Baseline/MILP/scripts
python run_case_MILP.py
```

---

## 各项目说明

### 06-Project_MAS_TL_STAP（主项目）

**全称：** Multi-Agent System — Temporal Logic based Simultaneous Task Allocation and Planning

解决异构多智能体系统中的**任务分配与运动规划联合优化**问题。给定 LTL 任务公式，框架自动分解任务、为多智能体分配协作性子任务，保证规划结果的渐进最优性。

- **求解方法：** B&B（分支定界）/ MILP
- **运动规划：** 栅格地图 + A* / Dijkstra
- **可视化：** 甘特图、轨迹图、视频导出
- **场景数：** 6 个预定义场景

```bash
cd 06-Project_MAS_TL_STAP/scripts
python run_case_1.py
```

在 `__main__` 中修改 `scene_index` 和 `opt_method`（`'BnB'` 或 `'MILP'`）即可切换不同配置。

### 07-JK_game（博弈决策）

将博弈论与 LTL 规划结合，通过「战法」自动生成 LTL 公式，进而生成偏序集和任务分配。集成了模糊 TOPSIS 多属性决策方法。

**启动方式：**

```bash
# 1. 启动后端
cd 07-JK_game
python CentralServer__master.py

# 2. 启动前端
cd 07-JK_game/planning/src/gui
python main.py

# 3. 在浏览器中访问 CentralServer 输出的 URL
```

### 08-Project_03_online（在线自适应规划）

面向动态战场环境的**在线自适应重规划**系统。支持离线预计算 + 在线快速响应，可在任务执行过程中动态调整分配方案。

```bash
cd 08-Project_03_online/scripts
python run_case_online.py
```

---

## 上游依赖

| 仓库 | 说明 | 位置 |
|------|------|------|
| [P_MAS_TG](https://github.com/MengGuo/P_MAS_TG) | 郭萌老师的 LTL 运动规划库 | `04-上游代码库/` |
| [LTL_MAS_C-action](https://github.com/LiuZesensengsheng/LTL_MAS_C-action) | LTL 多智能体动作规划 | `05-Baseline/LTL_MAS_C-action/` |
| [JK_game](https://github.com/LiuZesensengsheng/JK_game) | 博弈决策算法 | `07-JK_game/` |

---

## 环境配置

### 基础依赖

- Python ≥ 3.7（推荐 3.8+）
- pip 包：`numpy` `networkx` `matplotlib` `cvxpy` `Pillow` `pyyaml` `ortools`

### 一键安装

```bash
pip install numpy networkx matplotlib cvxpy Pillow pyyaml ortools
```

### 可选依赖

- **LTL2BA**：将 LTL 公式转换为 Büchi 自动机的外部工具，位于 `04-上游代码库/P_MAS_TG_py3/Install_ltl2ba/`
- **Crazyswarm**：用于物理仿真可视化，位于 `05-Baseline/LTL_MAS_C-action/visual_env/crazyswarm/`

---

## 快速开始

推荐按以下顺序运行各项目，逐步建立对整个技术栈的理解：

```bash
# 1. 学习上游代码 —— 理解 LTL Planner 基础
cd 04-上游代码库/P_MAS_TG_py3
python test.py

# 2. 运行 Baseline 测试 —— 理解偏序集构建与分配
cd 05-Baseline/LTL_MAS_C-action/test/task1_sim
python <test_script>.py

# 3. 运行主项目实验 —— 端到端任务分配与规划
cd 06-Project_MAS_TL_STAP/scripts
python run_case_1.py

# 4. 运行 MILP 方案 —— 全局最优求解对比
cd 05-Baseline/MILP/scripts
python run_case_MILP.py

# 5. 运行在线自适应项目
cd 08-Project_03_online/scripts
python run_case_online.py
```

---

## 论文与引用

本仓库涉及的学术工作：

1. **Guo, M.** — *Hybrid Control of Multi-robot Systems under Complex Temporal Tasks* (博士论文)
2. **Liu, Z. et al.** — *Simultaneous Task Allocation and Planning for Temporal Logic Goals in Heterogeneous Multi-Robot Systems*
3. **LaValle, S. M.** — *Planning Algorithms* (Cambridge University Press, 2006)
4. **Baier, C. & Katoen, J. P.** — *Principles of Model Checking* (MIT Press, 2008)
5. **Belta, C. et al.** — *Formal Methods for Discrete-Time Dynamical Systems*

如使用本仓库代码进行研究，请引用对应的上述论文。

---

## 作者

- **Junjie Wang** — pkuwjj1998@163.com
- Zesen Liu
- Yunyi Zhang
- Qisheng Zhao
- Shuo Zhang

---

## 许可证

本项目遵循 [LICENSE](LICENSE) 文件中的许可条款。

---

*最后更新：2026 年 6 月*
