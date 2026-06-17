import requests
host='http://127.0.0.1:9999/decision'
#决策
#功能1：获取ZF选择的内容
a = requests.post(host, json={'ZF_choose_function':0})
print(a.json())

#功能2：ZF对应的ZF组合
a = requests.post(host, json={'ZF_combination':'全面进攻'})
print(a.json())

#功能3：确认ZF，并发送给后端服务（本次合作的系统）计算，并输出任务分解结果。

a = requests.post(host, json={'ZF_detail':'#这里的输入应该是前端给输入的数据，但是就不使用了'})
print(a.json())

#功能4：任务分解结果展示序列图（以甘特图为基底，静态的，此次是首次分解规划的结果，与下面的可视化结果有区别）
a = requests.post(host, json={'Gantt_graph':'first'})
print(a.json())

#功能5：实验结束后，红方任务分解下（包括重规划部分）的任务序列甘特图（带时间长短，时间采集随实验同步进行）
a = requests.post(host, json={'Gantt_graph':'final'})
print(a.json())
host='http://127.0.0.1:9999/gaming'
#博弈部分
#功能1：红方智能体战场信息
a = requests.post(host, json='red_war_infor')
print(a.json())

#功能2：蓝方智能体战场信息
a = requests.post(host, json='blue_war_infor')
print(a.json())

#功能3：红方当前探测信息
a = requests.post(host, json='red_search_infor')
print(a.json())

#功能4：红蓝单元战力评估
a = requests.post(host, json='red_blue_ability')
print(a.json())

#功能5：红蓝单元价值评估
a = requests.post(host, json='red_blue_value')
print(a.json())

#功能6：红方智能体执行子任务信息
a = requests.post(host, json='red_executing_subtask')
print(a.json())

#功能7：红方累计奖励
a = requests.post(host, json='red_reward')
print(a.json())