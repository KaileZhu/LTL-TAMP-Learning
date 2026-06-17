更新日期2021.10.13
选定ortools 优化包 （开源，c++，能整数优化，带分支定界法）
准备实现：基础的01优化
                   基于分支定界法的整数优化
                   基于localsearch的方法（可能这里主要只使用其作为某个可行解的求解器）
                   带并行的localsearch（看情况）
    从poset到分发的接口
    在执行时的等待关系。

更新日期 2021.8.31
添加处理路径偏序集的算法
处理思路如下：1 生成所有路径
             2  调换路径顺序，获得排序关系
              3  补全排序关系
              4 分配（assignment）
              5 查表寻求排序关系，并加以验证。
 偏序集补充：
 1 增加接口
 2 修改为anytime算法
 3 结合计时工具进行定时！ 


## 2021.7.10

To-do:
* check interfaces after re-structure.
* run basic tests, even better use unit tests. 
    * check product buchi of single agent with/without action model. done
    * check product ts with/without marco actions.  done 
    * check product buchi of all agents without marco actions, with/without action model.  done
    * check product ts with marco actions. done (here is not exactly correct, there are more things to be consider than just add_labels )
    * check product buchi of with marco actions  done
    * check final plan.
* load agent mode, system model from .yaml files!!
* Complete docstrings.
* check flake8 for checking linting.

更新日期 2021.6.13
集中式的LTL处理逻辑
1 圈乘：包括 带动作的 和不带动作的
               对PTS 进行添加Macro-action
               对Buchi进行圈乘
               
         
2 任务规划： 利用Dij方法搜索路径

3  可视化：根据路径画出图


1 期计划目标                                                           1期完成记过
    实现基于networkx的自动生成motion model的WTS（单个智能体）                完成
    实现actions model的WTS                                                  完成
    实现macro-action model的WTS                                             完成
    实现每个model之间的圈乘                                                  完成

2 期计划目标
   优化算法结构，将叉乘作为单独的算法
   修改动作问题，定义macro动作由子模块构成
   设置可视化，计划直接在crazyflies中的python中读取
   


本次更新目标 打通WTS到Dij方法的问题
![image](https://github.com/LiuZesensengsheng/LTL_MAS_C-action/blob/optimize/picture/%E7%BB%98%E5%9B%BE1.jpg)
