#！/usr/bin/env python3

import math
import yaml
import numpy as np
import json

from PIL import Image
from matplotlib import pyplot as plt
from scipy.interpolate import splprep, splev

from datetime import datetime, timedelta

class InputData:
    def __init__(self):
        self.position = dict()
        self.task_type = dict()
        self.sub_task_type = list()
        self.agent_type = dict()
        self.agent_data = list()
        self.broken_agent_list = list()
        self.broken_time = None
        self.fluctuated_task_type = dict()

    # 将绝对时间转化为相对时间
    def convert_to_relative_time(self, absolute_time1, absolute_time2):
        time_format = "%Y-%m-%d %H:%M:%S"
        time1 = datetime.strptime(absolute_time1, time_format)
        time2 = datetime.strptime(absolute_time2, time_format)
        relative_time = time2 - time1
        return relative_time.total_seconds()

    # 将相对时间转化回绝对时间
    def convert_to_absolute_time(self, reference_time, relative_time):
        time_format = "%Y-%m-%d %H:%M:%S"
        reference_time = datetime.strptime(reference_time, time_format)
        absolute_time = reference_time + timedelta(seconds=relative_time)
        return absolute_time.strftime(time_format)
    
    def read_from_yaml(self, file_path):
        """
        Initialize the information of task and environment.
        ----------
        Parameters:
            file_path:(str), the path of the yaml file.
        """
        # read data from file.yaml
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            print('----------------------------------------')
            print('Read from %s' %file_path)
        
        # get offline time budget
        offline_time_budget = data['offline time budget']
        # get offline missile assign strategy
        offline_missile_assign_strategy = data['offline missile assign strategy']
        
        # get online time budget
        online_time_budget = data['online time budget']
        # get online missile assign strategy
        online_missile_assign_strategy = data['online missile assign strategy']
        
        return offline_time_budget, offline_missile_assign_strategy, online_time_budget, online_missile_assign_strategy
    
    def read_from_json_offline(self, ssl_info, dlgh_info, weapon_info):
        # with open(file_path_ssl, 'r', encoding='utf-8') as file:
        #     ssl_info = json.load(file)["result"]
        # with open(file_path_dlgh, 'r', encoding='utf-8') as file:
        #     dlgh_info = json.load(file)["result"]
        # with open(file_path_weapon, 'r', encoding='utf-8') as file:
        #     weapon_info = json.load(file)["result"]
        task, agent_data = str(), list()

        # 处理mbbs中存在'-'或'_'符号的情况
        map_origin_to_regular_mbbs = dict()    # 格式{'原本的mbbs'：'清理后的mbbs'}
        map_regular_to_origin_mbbs = dict()    # 格式{'清理后的mbbs'：'原本的mbbs'}
        regularized_mbbs_list = list()  # 存储已经处理过的mbbs
        for big_task in dlgh_info:
            for target_info in big_task["ssyamx"]:
                if target_info["mbbs"] not in regularized_mbbs_list:
                    regularized_mbbs_list.append(target_info["mbbs"])
                    regular_mbbs = target_info["mbbs"].replace('-', '')
                    regular_mbbs = regular_mbbs.replace('_', '')
                    map_origin_to_regular_mbbs[target_info["mbbs"]] = regular_mbbs
                    map_regular_to_origin_mbbs[regular_mbbs] = target_info["mbbs"]

        # get the information of agents
        i = 0
        agent_list = []     # 用于存储那些已经已经收集好信息的智能体名称
        ssl_info_sorted = sorted(ssl_info, key=lambda x:x["mzzzsj"])
        self.offline_reference_time = ssl_info_sorted[0]["mzzzsj"]   # 用于将绝对时间转化为相对时间，格式为年/月/日/时/分/秒
        for weapon in weapon_info:
            if weapon['zbbs'] not in agent_list:
                agent_list.append(weapon['zbbs'])
                agent_datai = (i, weapon["zzwqxhnm"]+'_'+weapon["zdblxnm"], dict(), weapon['zbbs'], 10, weapon['xdsl'])     # 准备时间先都设定成10
                for ssl in ssl_info:
                    if ssl["hlptbs"] == weapon['zbbs']:
                        time_zuizao = self.convert_to_relative_time(self.offline_reference_time, ssl["mzzzsj"])
                        time_zuiwan = self.convert_to_relative_time(self.offline_reference_time, ssl["mzzwsj"])
                        agent_datai[2]['attack'+'_'+map_origin_to_regular_mbbs[ssl["mbbs"]]] = [ssl["djbhsj"],[time_zuizao,time_zuiwan]]
                agent_data.append(agent_datai)
                i = i + 1
        
        # get the information of tasks
        subtasks = dict()
        yxj_dic = dict()    # 用于存储每个目标的优先级
        for big_task in dlgh_info:
            for target_info in big_task["ssyamx"]:
                yxj_dic['attack'+'_'+map_origin_to_regular_mbbs[target_info["mbbs"]]] = target_info["yxj"]
                subtasks['attack'+'_'+map_origin_to_regular_mbbs[target_info["mbbs"]]] = dict()
                for req in target_info["dxdl"]:
                    subtasks['attack'+'_'+map_origin_to_regular_mbbs[target_info["mbbs"]]][req["zzwqxhnm"]+'_'+req["zdblxnm"]] = req["dl"]

        # 根据目标优先级得到LTL任务公式
        task = []
        # 首先根据优先级进行分层
        layer_dic = dict()
        for layer in set(yxj_dic.values()):
            layer_dic[layer] = list()
            for key, value in yxj_dic.items():
                if layer == value:
                    layer_dic[layer].append(key)
        layers = sorted(list(layer_dic.keys()))     # 升序排列优先级
        # 若无优先级区别，直接构建公式
        if len(layers) == 1:
            for subtask in layer_dic[layers[0]]:\
                task.append('<>({})'.format(subtask))
        else:
            for i in range(len(layers)-1):
                for subtask1 in layer_dic[layers[i]]:
                    for subtask2 in layer_dic[layers[i+1]]:
                        task.append('<>({} && <>({}))'.format(subtask1, subtask2))
        
        
        self.task_type = subtasks
        self.agent_data = agent_data
        self.map_regular_to_origin_mbbs = map_regular_to_origin_mbbs
        self.map_origin_to_regular_mbbs = map_origin_to_regular_mbbs

        return task
        
    def read_from_json_online(self, file_path_ssl, file_path_dlgh, file_path_weapon, file_offline_solution, file_time_failed_ssl):
        with open(file_path_ssl, 'r', encoding='utf-8') as file:
            ssl_info = json.load(file)["result"]
        with open(file_path_dlgh, 'r', encoding='utf-8') as file:
            dlgh_info = json.load(file)["result"]
        with open(file_path_weapon, 'r', encoding='utf-8') as file:
            weapon_info = json.load(file)["result"]
        
        with open(file_offline_solution, 'r', encoding='utf-8') as file:
            offline_solution = json.load(file)
        with open(file_time_failed_ssl, 'r', encoding='utf-8') as file:
            time_failed_ssl = json.load(file)
            
        task, agent_data = str(), list()
        
        # 处理mbbs中存在'-'或'_'符号的情况
        map_origin_to_regular_mbbs = dict()    # 格式{'原本的mbbs'：'清理后的mbbs'}
        map_regular_to_origin_mbbs = dict()    # 格式{'清理后的mbbs'：'原本的mbbs'}
        regularized_mbbs_list = list()  # 存储已经处理过的mbbs
        for big_task in dlgh_info:
            for target_info in big_task["ssyamx"]:
                if target_info["mbbs"] not in regularized_mbbs_list:
                    regularized_mbbs_list.append(target_info["mbbs"])
                    regular_mbbs = target_info["mbbs"].replace('-', '')
                    regular_mbbs = regular_mbbs.replace('_', '')
                    map_origin_to_regular_mbbs[target_info["mbbs"]] = regular_mbbs
                    map_regular_to_origin_mbbs[regular_mbbs] = target_info["mbbs"]
        
        replan_time = time_failed_ssl["replan time"]
        failed_ssl_list = time_failed_ssl['failed sslbs']
        # get the information of ssl/except failed ssl
        i = 0
        agent_list = []     # 用于存储那些已经已经收集好信息的智能体名称
        # ssl_info_sorted = sorted(ssl_info, key=lambda x:x["mzzzsj"])
        self.online_reference_time = replan_time   # 直接把触发重规划的时刻作为参考时刻，格式为年/月/日/时/分/秒
        for weapon in weapon_info:
            if weapon['zbbs'] not in agent_list:
                agent_list.append(weapon['zbbs'])
                # 需要根据重规划时间判断该装备是否已经发射过导弹从而计算其剩余弹量
                remain_missile = weapon['xdsl']
                for offline_ssl in offline_solution:
                    if offline_ssl["hlptbs"] == weapon['zbbs'] and replan_time > offline_ssl["djkssj"]:
                        remain_missile = remain_missile - offline_ssl["ydsl"]
                if remain_missile > 0:
                    agent_datai = (i, weapon["zzwqxhnm"]+'_'+weapon["zdblxnm"], dict(), weapon['zbbs'], 10, remain_missile)     # 准备时间先都设定成10
                    for ssl in ssl_info:
                        if ssl["hlptbs"] == weapon['zbbs'] and ssl["sslbs"] not in failed_ssl_list:     # 把失效的ssl去除掉
                            time_zuizao = self.convert_to_relative_time(self.online_reference_time, ssl["mzzzsj"])
                            time_zuiwan = self.convert_to_relative_time(self.online_reference_time, ssl["mzzwsj"])
                            agent_datai[2]['attack'+'_'+map_origin_to_regular_mbbs[ssl["mbbs"]]] = [ssl["djbhsj"],[time_zuizao,time_zuiwan]]
                    agent_data.append(agent_datai)
                    i = i + 1
        
        # get the information of tasks/except finished tasks
        subtasks = dict()
        yxj_dic = dict()    # 用于存储每个目标的优先级
        for big_task in dlgh_info:
            for target_info in big_task["ssyamx"]:
                yxj_dic['attack'+'_'+map_origin_to_regular_mbbs[target_info["mbbs"]]] = target_info["yxj"]
                subtasks['attack'+'_'+map_origin_to_regular_mbbs[target_info["mbbs"]]] = dict()
                for req in target_info["dxdl"]:
                    subtasks['attack'+'_'+map_origin_to_regular_mbbs[target_info["mbbs"]]][req["zzwqxhnm"]+'_'+req["zdblxnm"]] = req["dl"] 
        
        # 根据重规划时刻判断哪ssl已经执行了，从而更新任务（1.移除已完成的任务；2.更新任务的弹量需求）
        for offline_ssl in offline_solution:
            # 判断ssl是否已经执行
            if  replan_time > offline_ssl["djkssj"]:
                # 从weapon_info中提取该ssl的弹型
                for weapon in weapon_info:
                    if weapon["zbbs"] == offline_ssl["hlptbs"]:
                        missile_type = weapon["zzwqxhnm"]+'_'+weapon["zdblxnm"]
                        break
                # 在subtasks中更新任务及其弹量需求
                for task, req in subtasks.items():
                    if map_origin_to_regular_mbbs[offline_ssl["mbbs"]] in task:
                        req[missile_type] = req[missile_type] - offline_ssl["ydsl"]
                        if req[missile_type] <= 0:
                            del subtasks[task][missile_type]
                        if not subtasks[task]:
                            del subtasks[task]
                        break

        
        # 根据目标优先级得到LTL任务公式
        task = []
        # 更新优先级字典/把已完成的任务删掉
        for key in list(yxj_dic.keys()):
            if key not in subtasks.keys():
                del yxj_dic[key]
        # 根据优先级进行分层
        layer_dic = dict()
        for layer in set(yxj_dic.values()):
            layer_dic[layer] = list()
            for key, value in yxj_dic.items():
                if layer == value:
                    layer_dic[layer].append(key)
        layers = sorted(list(layer_dic.keys()))     # 升序排列优先级
         # 若无优先级区别，直接构建公式
        if len(layers) == 1:
            for subtask in layer_dic[layers[0]]:\
                task.append('<>({})'.format(subtask))
        else:
            for i in range(len(layers)-1):
                for subtask1 in layer_dic[layers[i]]:
                    for subtask2 in layer_dic[layers[i+1]]:
                        task.append('<>({} && <>({}))'.format(subtask1, subtask2))
        
        self.task_type = subtasks
        self.agent_data = agent_data
        self.map_regular_to_origin_mbbs = map_regular_to_origin_mbbs
        self.map_origin_to_regular_mbbs = map_origin_to_regular_mbbs

        return task, ssl_info, dlgh_info

def norm_distance(pos_f, pos_t):
    dis = math.hypot(pos_f[0]-pos_t[0], pos_f[1]-pos_t[1])
    return round(dis, 4)

def gener_path(path, vel, k=3, c=1.0):
    # convert the input path to np.array format
    path = np.array(path)
    # perform cubic spline interpolation
    tck, u = splprep(path.T, k=k, s=0, per=False)
    # evaluate the spline at more points
    curve_points = splev(np.linspace(0, 1, 100), tck)
    # calculate the arc length of the curve
    length = np.sum(np.sqrt(np.sum(np.diff(curve_points, axis=1)**2, axis=0)))
    time_eval = math.ceil(length/vel*c)
    # calculate curve points according to the evaluate time seqsuence
    t_eval = np.linspace(0, 1, time_eval)
    curve_points = np.array(splev(t_eval, tck))
    return curve_points
