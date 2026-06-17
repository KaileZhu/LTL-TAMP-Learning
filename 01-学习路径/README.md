# 学习路径

## 推荐入门顺序

1. **先了解 LTL 是如何和控制联系起来的**
   - a. 了解 LTL：看 *Principles of Model Checking* 第 2、3、5 章，大致了解语义即可，之后当工具书用
   - b. 了解 LTL + Control：有自下而上和自上而下两条路径，推荐看国老师的毕业论文，非常深入浅出

2. **了解 LTL 在控制中的代码操作**
   - 看 [P_MAS_TG](https://github.com/MengGuo/P_MAS_TG) 项目，了解最基础的 LTL + Control 代码实现
   - 理解 LTL Planner 的作用

3. **LTL → 偏序集（Poset）**
   - 看泽森的论文 *Simultaneous Task Allocation and Planning for Temporal Logic Goals*
   - 复现代码：本仓库 `05-Baseline/LTL_MAS_C-action/`

4. **偏序 → 动态决策**
   - 看 JK_game 项目：本仓库 `07-JK_game/`

5. **进阶：TMOS**
   - 阅读 `03-论文与书籍/TMOS-相关/` 下的论文
