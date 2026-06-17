from geopy.distance import geodesic
import numpy as np
import random
import time
import copy
import math
import matplotlib.pyplot as plt
from training.Arch.arch_model import getDistancePoint
import os

red_type_2 = ['RC', 'RUSV', 'RSUAV', 'RAUAV', 'RM', 'RAD']

red_RC_2 = ['Red.RedForce_RC#0']
red_RUSV_2 = ['Red.RedForce_RC#0_RUSV#0', 'Red.RedForce_RC#0_RUSV#1', 'Red.RedForce_RC#0_RUSV#2', 'Red.RedForce_RC#0_RUSV#3',
            'Red.RedForce_RC#0_RUSV#4', 'Red.RedForce_RC#0_RUSV#5', 'Red.RedForce_RC#0_RUSV#6', 'Red.RedForce_RC#0_RUSV#7',
            'Red.RedForce_RC#0_RUSV#8', 'Red.RedForce_RC#0_RUSV#9']
red_RSUAV_2 = ['Red.RedForce_RC#0_RSUAV#0', 'Red.RedForce_RC#0_RSUAV#1', 'Red.RedForce_RC#0_RSUAV#2', 'Red.RedForce_RC#0_RSUAV#3',
             'Red.RedForce_RC#0_RSUAV#4']
red_RAUAV_2 = ['Red.RedForce_RC#0_RAUAV#0', 'Red.RedForce_RC#0_RAUAV#1', 'Red.RedForce_RC#0_RAUAV#2', 'Red.RedForce_RC#0_RAUAV#3',
             'Red.RedForce_RC#0_RAUAV#4', 'Red.RedForce_RC#0_RAUAV#5', 'Red.RedForce_RC#0_RAUAV#6', 'Red.RedForce_RC#0_RAUAV#7',
             'Red.RedForce_RC#0_RAUAV#8', 'Red.RedForce_RC#0_RAUAV#9']
red_RM_2 = ['Red.RedForce_RC#0_RM#0', 'Red.RedForce_RC#0_RM#1', 'Red.RedForce_RC#0_RM#2', 'Red.RedForce_RC#0_RM#3',
          'Red.RedForce_RC#0_RM#4', 'Red.RedForce_RC#0_RM#5', 'Red.RedForce_RC#0_RM#6', 'Red.RedForce_RC#0_RM#7',
          'Red.RedForce_RC#0_RM#8', 'Red.RedForce_RC#0_RM#9', 'Red.RedForce_RC#0_RM#10', 'Red.RedForce_RC#0_RM#12',
          'Red.RedForce_RC#0_RM#13', 'Red.RedForce_RC#0_RM#14', 'Red.RedForce_RC#0_RM#15', 'Red.RedForce_RC#0_RM#16',
          'Red.RedForce_RC#0_RM#17', 'Red.RedForce_RC#0_RM#18', 'Red.RedForce_RC#0_RM#19']
red_RAD_2 = ['Red.RedForce_RC#0_RAD#0', 'Red.RedForce_RC#0_RAD#1', 'Red.RedForce_RC#0_RAD#2']

blue_type_2 = ['BC', 'BUSV', 'BSUAV', 'BAUAV', 'BM', 'BAD']

blue_BC_2 = ['Blue.BlueForce_BC#0']
blue_BUSV_2 = ['Blue.BlueForce_BC#0_BUSV#0', 'Blue.BlueForce_BC#0_BUSV#1', 'Blue.BlueForce_BC#0_BUSV#2', 'Blue.BlueForce_BC#0_BUSV#3',
             'Blue.BlueForce_BC#0_BUSV#4']
blue_BSUAV_2 = ['Blue.BlueForce_BC#0_BSUAV#0', 'Blue.BlueForce_BC#0_BSUAV#1', 'Blue.BlueForce_BC#0_BSUAV#2', 'Blue.BlueForce_BC#0_BSUAV#3',
              'Blue.BlueForce_BC#0_BSUAV#4']
blue_BAUAV_2 = ['Blue.BlueForce_BC#0_BAUAV#0']
blue_BM_2 = ['Blue.BlueForce_BC#0_BM#0', 'Blue.BlueForce_BC#0_BM#1', 'Blue.BlueForce_BC#0_BM#2', 'Blue.BlueForce_BC#0_BM#3',
           'Blue.BlueForce_BC#0_BM#4', 'Blue.BlueForce_BC#0_BM#5', 'Blue.BlueForce_BC#0_BM#6', 'Blue.BlueForce_BC#0_BM#7',
           'Blue.BlueForce_BC#0_BM#8', 'Blue.BlueForce_BC#0_BM#9', 'Blue.BlueForce_BC#0_BM#10', 'Blue.BlueForce_BC#0_BM#11',
           'Blue.BlueForce_BC#0_BM#12', 'Blue.BlueForce_BC#0_BM#13', 'Blue.BlueForce_BC#0_BM#14', 'Blue.BlueForce_BC#0_BM#15',
           'Blue.BlueForce_BC#0_BM#16', 'Blue.BlueForce_BC#0_BM#17', 'Blue.BlueForce_BC#0_BM#18', 'Blue.BlueForce_BC#0_BM#19']
blue_BAD_2 = ['Blue.BlueForce_BC#0_BAD#0', 'Blue.BlueForce_BC#0_BAD#1', 'Blue.BlueForce_BC#0_BAD#2']

blue_location_2 = [[118, 23.5], [119, 24], [119, 25], [117, 24], [118, 25]]
red_location_2 = [[120, 25], [119.5, 24], [121, 25.5], [119, 23]]
red_location_for_USV_2 = [[121, 24], [120, 23.5]]

red_agent_num_2 = 49
blue_agent_num_2 = 35

def compute_acc_reward_2(obs):
    index = 0
    blue_life = [-1 for _ in range(blue_agent_num_2)]
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['name'] in blue_BC_2:
                blue_life[index] = 100
                index += 1
                continue
            if entity['life'] <= 0:
                blue_life[index] = 0
            else:
                blue_life[index] = entity['life']
            index += 1

    index = 0
    red_life = [1 for _ in range(red_agent_num_2)]
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if entity['life'] <= 0:
                red_life[index] = 0
            else:
                red_life[index] = entity['life']
            index += 1

    blue_life_reward = sum(blue_life) * 0
    red_life_reward = sum(red_life) * 0

    red_weight = [
        10,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
        3, 3, 3
    ]

    blue_weight = [
        10,
        4, 4, 4, 4, 4,
        4, 4, 4, 4, 4,
        10,
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
        3, 3, 3
    ]

    blue_survive_reward = 0
    red_survive_reward = 0
    for i in range(blue_agent_num_2):
        if blue_life[i] > 0:
            blue_survive_reward = blue_survive_reward + blue_weight[i]

    for i in range(red_agent_num_2):
        if red_life[i] > 0:
            red_survive_reward = red_survive_reward + red_weight[i]

    return red_survive_reward - blue_survive_reward + red_life_reward - blue_life_reward + 20

red_unit_life_2 = [
    100,
    20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
    20, 20, 20, 20, 20,
    40, 40, 40, 40, 40, 40, 40, 40, 40, 40,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    100, 100, 100
]
blue_unit_life_2 = [
    100,
    20, 20, 20, 20, 20,
    20, 20, 20, 20, 20,
    20,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    50, 50, 50
]

def delete_path(dir_path):
    del_list = os.listdir(dir_path)
    for i in del_list:
        file_path = os.path.join(dir_path, i)
        if os.path.isfile(file_path):
            os.remove(file_path)

def get_red_staus_2(obs):
    unit_staus = [-1 for _ in range(red_agent_num_2)]
    index = 0
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if index >= 26 and index < 46:
                index += 1
                continue
            if red_entity['life'] <= 0:
                unit_staus[index] = 0
            elif red_entity['life'] == red_unit_life_2[index]:
                unit_staus[index] = 1
            else:
                unit_staus[index] = 2

            index += 1

    red_staus = {}
    # print(unit_staus)
    red_staus['step'] = obs['step']
    red_staus['red_damage_rate'] = unit_staus.count(2) / 29
    red_staus['red_live_rate'] = unit_staus.count(1) / 29
    red_staus['red_destroy_rate'] = unit_staus.count(0) / 29

    return red_staus


def get_blue_staus_2(obs):
    unit_staus = [-1 for _ in range(blue_agent_num_2)]
    index = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if index >= 12 and index < 32:
                index += 1
                continue
            if blue_entity['name'] in blue_BC_2:
                unit_staus[index] = 1
                index += 1
                continue
            if blue_entity['life'] <= 0:
                unit_staus[index] = 0
            elif blue_entity['life'] == blue_unit_life_2[index]:
                unit_staus[index] = 1
            else:
                # print(blue_entity['name'], blue_entity['life'], blue_unit_life_2[index])
                unit_staus[index] = 2

            index += 1
    # print(unit_staus)
    blue_staus = {}
    blue_staus['step'] = obs['step']
    blue_staus['blue_damage_rate'] = unit_staus.count(2) / 15
    blue_staus['blue_live_rate'] = unit_staus.count(1) / 15
    blue_staus['blue_destroy_rate'] = unit_staus.count(0) / 15

    return blue_staus

# blue_strength_2 = [1, 0, 0, 0, 0, 0, 7, 7, 7, 7, 9, 9, 9, 0, 0, 0, 0, 0, 3, 4, 4, 4]
# blue_unit_life_2 = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0]

red_strength_2 = [
    1,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    3, 3, 3
]

blue_strength_2 = [
    1,
    12, 12, 12, 12, 12,
    5, 5, 5, 5, 5,
    8,
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    3, 3, 3
]

def get_strength_2(obs):
    index = 0
    blue_mi_strength = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_entity['name'] in blue_BC_2:
                blue_mi_strength += blue_strength_2[index] * 100 / blue_unit_life_2[index]
                index += 1
                continue
            if blue_entity['life'] > 0:
                blue_mi_strength += blue_strength_2[index] * blue_entity['life'] / blue_unit_life_2[index]
            index += 1

    index = 0
    red_mi_strength = 0
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if red_entity['life'] > 0:
                red_mi_strength += red_strength_2[index] * red_entity['life'] / red_unit_life_2[index]
            index += 1
    return red_mi_strength, blue_mi_strength

red_value_2 = [
    10,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    3, 3, 3
]

blue_value_2 = [
    10,
    4, 4, 4, 4, 4,
    4, 4, 4, 4, 4,
    10,
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    3, 3, 3
]


def get_value_2(obs):
    index = 0
    blue_mi_value = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_entity['name'] in blue_BC_2:
                blue_mi_value += blue_value_2[index]
            elif blue_entity['life'] > 0:
                blue_mi_value += blue_value_2[index]
            index += 1

    index = 0
    red_mi_value = 0
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if red_entity['life'] > 0:
                red_mi_value += red_value_2[index]
            index += 1
    return red_mi_value, blue_mi_value


def get_detect_2(obs, detect_list):
    index = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if detect_list[index] == 1:
                index += 1
                continue
            if blue_entity['name'] in blue_BC_2:
                done = False
                blue_location_x = blue_entity['latitude']
                blue_location_y = blue_entity['longitude']
                for red_id, red_entities in obs['redSituation'].items():
                    for red_entity in red_entities:
                        if red_entity["name"] in red_RSUAV_2 or red_entity["name"] in red_RAUAV_2:
                            red_location_x = red_entity['latitude']
                            red_location_y = red_entity['longitude']
                            if min(red_entity['range'], 40) > geodesic((blue_location_x, blue_location_y),
                                                                       (red_location_x, red_location_y)).km:
                                detect_list[index] = 1
                                done = True
                                break
                    if done:
                        break
                index += 1
            elif blue_entity['life'] <= 0:
                detect_list[index] = 1
                index += 1
            else:
                done = False
                blue_location_x = blue_entity['latitude']
                blue_location_y = blue_entity['longitude']
                for red_id, red_entities in obs['redSituation'].items():
                    for red_entity in red_entities:
                        if red_entity["name"] in red_RSUAV_2 or red_entity["name"] in red_RAUAV_2:
                            red_location_x = red_entity['latitude']
                            red_location_y = red_entity['longitude']
                            if min(red_entity['range'], 40) > geodesic((blue_location_x, blue_location_y),
                                                              (red_location_x, red_location_y)).km:
                                detect_list[index] = 1
                                done = True
                                break
                    if done:
                        break
                index += 1

    detect_num = np.sum(np.array(detect_list))
    return detect_num / 40.0, detect_list


class Logger2:
    def __init__(self):
        self.detect_list = [0 for i in range(blue_agent_num_2)]

        dir_path = 'planning/src/gui/assets/live_damage_destory/'
        del_list = os.listdir(dir_path)
        for i in del_list:
            file_path = os.path.join(dir_path, i)
            if os.path.isfile(file_path):
                os.remove(file_path)

        dir_path = 'planning/src/gui/assets/detect_ratio'
        del_list = os.listdir(dir_path)
        for i in del_list:
            file_path = os.path.join(dir_path, i)
            if os.path.isfile(file_path):
                os.remove(file_path)

        dir_path = 'planning/src/gui/assets/strength_value'
        del_list = os.listdir(dir_path)
        for i in del_list:
            file_path = os.path.join(dir_path, i)
            if os.path.isfile(file_path):
                os.remove(file_path)

        dir_path = 'planning/src/gui/assets/reward'
        del_list = os.listdir(dir_path)
        for i in del_list:
            file_path = os.path.join(dir_path, i)
            if os.path.isfile(file_path):
                os.remove(file_path)

        dir_path = 'planning/src/gui/assets/route'
        del_list = os.listdir(dir_path)
        for i in del_list:
            file_path = os.path.join(dir_path, i)
            if os.path.isfile(file_path):
                os.remove(file_path)

        dir_path = 'logger/SAUGV'
        del_list = os.listdir(dir_path)
        for i in del_list:
            file_path = os.path.join(dir_path, i)
            if os.path.isfile(file_path):
                os.remove(file_path)

        delete_path('logger/RSUAV')
        delete_path('logger/FSUAV')
        delete_path('logger/blueUAV')
        delete_path('logger/blueInf')
        delete_path('logger/blueArt')
        delete_path('logger/common')

    def update(self, situationDataDict, reward_list):
        # 设置字号
        front_size = 25
        textprops = {"size": 25}

        red_staus = get_red_staus_2(situationDataDict)
        file = open('logger/common/red_damage.txt', mode='a')
        file.write(str(red_staus) + ',\n')
        file.close()

        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.figure(figsize=(10, 6))
        rate1 = '红方战毁率' + str(round(red_staus['red_destroy_rate'] * 100)) + '%'
        rate2 = '红方受损率' + str(round(red_staus['red_damage_rate'] * 100)) + '%'
        rate3 = '红方完好率' + str(round(red_staus['red_live_rate'] * 100)) + '%'
        # label = ['红方战毁率', '红方受损率', '红方完好率']
        label = [rate1, rate2, rate3]
        explode = [0.1, 0.1, 0.1]
        patches, texts = plt.pie([red_staus['red_destroy_rate'], red_staus['red_damage_rate'], red_staus['red_live_rate']],
                labels=label, explode=explode, textprops=textprops)
        texts[1].set_y(texts[1]._y + 0.2)
        # for i in range(len(texts)):
        #     print(i, texts[i])
        # plt.title('红方战场战损比', fontdict=textprops)
        plt.axis("equal")
        plt.savefig('planning/src/gui/assets/live_damage_destory/red_' + str(situationDataDict['step']))
        plt.close()

        blue_staus = get_blue_staus_2(situationDataDict)
        file = open('logger/common/blue_damage.txt', mode='a')
        file.write(str(blue_staus) + ',\n')
        file.close()

        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.figure(figsize=(10, 6))
        rate1 = '蓝方战毁率'+str(round(blue_staus['blue_destroy_rate']*100)) + '%'
        rate2 = '蓝方受损率'+str(round(blue_staus['blue_damage_rate']*100)) + '%'
        rate3 = '蓝方完好率'+str(round(blue_staus['blue_live_rate']*100)) + '%'
        # label = ['蓝方战毁率', '蓝方受损率', '蓝方完好率']
        label = [rate1, rate2, rate3]
        explode = [0.1, 0.1, 0.1]
        patches, texts = plt.pie([blue_staus['blue_destroy_rate'], blue_staus['blue_damage_rate'], blue_staus['blue_live_rate']],
                labels=label, explode=explode, textprops=textprops)
        # print(texts[1])
        texts[1].set_y(texts[1]._y + 0.2)
        # plt.title('蓝方战场战损比', fontdict=textprops)
        plt.axis("equal")
        plt.savefig('planning/src/gui/assets/live_damage_destory/blue_' + str(situationDataDict['step']))
        plt.close()

        detect_ratio, self.detect_list = get_detect_2(situationDataDict, self.detect_list)
        file = open('logger\common\detect.txt', mode='a')
        file.write('{\'step\':' + str(situationDataDict['step']) + ', \'red_detect_rate\':' + str(detect_ratio) + '},\n')
        file.close()

        plt.rcParams['font.sans-serif'] = 'SimHei'
        plt.figure(figsize=(10, 6))
        rate1 = '侦察率' + str(round(detect_ratio * 100)) + '%'
        rate2 = '未侦察率' + str(round((1-detect_ratio) * 100)) + '%'
        # label = ['侦察率', '未侦察率']
        label = [rate1, rate2]
        explode = [0.1, 0.1]
        plt.pie([detect_ratio, 1-detect_ratio], labels=label, explode=explode, textprops=textprops)
        # plt.title('战场侦察比', fontdict=textprops)
        plt.axis("equal")
        plt.savefig('planning/src/gui/assets/detect_ratio/' + str(situationDataDict['step']))
        plt.close()

        red_mi_strength, blue_mi_strength = get_strength_2(situationDataDict)
        file = open('logger\common\strength.txt', mode='a')
        file.write('{\'step\':' + str(situationDataDict['step']) + ', \'red_ military_strength\':' + str(red_mi_strength) +
                   ', \'blue_ military_strength\':' + str(blue_mi_strength) + '},\n')
        file.close()

        red_mi_value, blue_mi_value = get_value_2(situationDataDict)
        file = open('logger/common/value.txt', mode='a')
        file.write('{\'step\':' + str(situationDataDict['step']) + ', \'red_ military_value\':' + str(red_mi_value) +
                   ', \'blue_ military_value\':' + str(blue_mi_value) + '},\n')
        file.close()

        shops = ['红方战力/价值评估', '蓝方战力/价值评估']
        strength = [red_mi_strength, blue_mi_strength]
        value = [red_mi_value, blue_mi_value]

        xticks = np.arange(len(shops))
        fig, ax = plt.subplots(figsize=(10, 9))
        ax.bar(xticks, strength, width=0.25, label='实时战力评估', color='red')
        ax.bar(xticks + 0.25, value, width=0.25, label='实时价值评估', color='blue')
        ax.set_ylabel('评估得分', fontdict=textprops)
        plt.ylim(ymin=0, ymax=160)

        ax.legend(fontsize=front_size)
        ax.set_xticks(xticks + 0.125)
        ax.set_xticklabels(shops, fontsize=front_size)
        plt.yticks(fontsize=front_size)
        plt.savefig('planning/src/gui/assets/strength_value/' + str(situationDataDict['step']))
        plt.close()

        red_location = []
        blue_location = []
        for id, entities in situationDataDict['redSituation'].items():
            for entity in entities:
                red_location.append([entity['longitude'], entity['latitude']])

        for id, entities in situationDataDict['blueSituation'].items():
            for entity in entities:
                blue_location.append([entity['longitude'], entity['latitude']])
        file = open('logger\common\location.txt', mode='a')
        file.write('red_location: ' + str(red_location) + ', blue_location: ' + str(blue_location) + '\n')
        file.close()

        reward = compute_acc_reward_2(situationDataDict)
        file = open('logger/common/reward.txt', mode='a')
        file.write('{\'step\':' + str(situationDataDict['step']) + ', \'reward\':' + str(reward) + '},\n')
        file.close()

        reward_list.append(reward)
        plt.figure(figsize=(12, 8))
        plt.axis([0, 300, 0, 205])
        x = list(range(len(reward_list)))

        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.plot(x, reward_list, color='r')
        plt.xlabel('仿真步长', fontdict=textprops)
        plt.ylabel('奖励', fontdict=textprops)
        plt.yticks(fontsize=front_size)
        plt.xticks(fontsize=front_size)
        plt.savefig('planning/src/gui/assets/reward/' + str(situationDataDict['step']))
        plt.close()

        for red_id, red_entities in situationDataDict['redSituation'].items():
            for red_entity in red_entities:
                if red_entity["name"] in red_RUSV_2:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    RUSV_idx = red_entity["name"][-1]

                    lat_path = 'logger/SAUGV/'+RUSV_idx+'_lat.txt'
                    lon_path = 'logger/SAUGV/'+RUSV_idx+'_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()

                if red_entity["name"] in red_RSUAV_2:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    RSUAV_idx = red_entity["name"][-1]

                    lat_path = 'logger/RSUAV/' + RSUAV_idx + '_lat.txt'
                    lon_path = 'logger/RSUAV/' + RSUAV_idx + '_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()

                if red_entity["name"] in red_RAUAV_2:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    FSUAV_idx = red_entity["name"][-1]

                    lat_path = 'logger/FSUAV/' + FSUAV_idx + '_lat.txt'
                    lon_path = 'logger/FSUAV/' + FSUAV_idx + '_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()
        for blue_id, blue_entities in situationDataDict['blueSituation'].items():
            for blue_entity in blue_entities:
                if blue_entity["name"] in blue_BUSV_2:
                    unit_lat = blue_entity['latitude']
                    unit_lon = blue_entity['longitude']
                    UAV_idx = blue_entity["name"][-1]

                    lat_path = 'logger/blueUAV/'+UAV_idx+'_lat.txt'
                    lon_path = 'logger/blueUAV/'+UAV_idx+'_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()
                if blue_entity["name"] in blue_BSUAV_2:
                    unit_lat = blue_entity['latitude']
                    unit_lon = blue_entity['longitude']
                    Inf_idx = blue_entity["name"][-1]

                    lat_path = 'logger/blueInf/'+Inf_idx+'_lat.txt'
                    lon_path = 'logger/blueInf/'+Inf_idx+'_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()
                if blue_entity["name"] in blue_BAUAV_2:
                    unit_lat = blue_entity['latitude']
                    unit_lon = blue_entity['longitude']
                    Art_idx = blue_entity["name"][-1]

                    lat_path = 'logger/blueArt/'+Art_idx+'_lat.txt'
                    lon_path = 'logger/blueArt/'+Art_idx+'_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()

        fig, ax = plt.subplots(figsize=(14, 10))
        color_list = ['red', 'green', 'blue', 'yellow']
        # 红方无人车
        for i in range(10):
            lat_path = 'logger/SAUGV/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            lon_path = 'logger/SAUGV/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()
            if i == 0:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2, label="红方作战单位轨迹")
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='red', linewidth=4, label="红方水下力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='red', linewidth=4)

        # 红方RSUAV
        for i in range(5):
            lat_path = 'logger/RSUAV/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            lon_path = 'logger/RSUAV/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()
            if i == 0:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='>', color='red', linewidth=4, label="红方空中力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='>', color='red', linewidth=4)

        # 红方FSUAV
        for i in range(10):
            lat_path = 'logger/FSUAV/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            lon_path = 'logger/FSUAV/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()

            plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2)
            plt.scatter(lon_list[-1], lat_list[-1], marker='>', color='red', linewidth=4)

        # 蓝方UAV
        for i in range(5):
            lat_path = 'logger/blueUAV/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            lon_path = 'logger/blueUAV/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()
            if i == 0:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2, label="蓝方作战单位轨迹")
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='blue', linewidth=4, label="蓝方水下力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='blue', linewidth=4)


        # 蓝方Inf
        for i in range(5):
            lat_path = 'logger/blueInf/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            lon_path = 'logger/blueInf/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()
            if i == 0:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='<', color='blue', linewidth=4, label="蓝方空中力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='<', color='blue', linewidth=4)

        # 蓝方Art
        for i in range(1):
            lat_path = 'logger/blueArt/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            lon_path = 'logger/blueArt/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()

            plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
            plt.scatter(lon_list[-1], lat_list[-1], marker='<', color='blue', linewidth=4)

        plt.legend(loc='upper left', fontsize=20)
        plt.ylim(ymin=23, ymax=26)
        plt.xlim(xmin=116, xmax=122)
        plt.xlabel('经度', fontdict=textprops)
        plt.ylabel('纬度', fontdict=textprops)
        plt.yticks(fontsize=front_size)
        plt.xticks(fontsize=front_size)
        plt.savefig('planning/src/gui/assets/route/' + str(situationDataDict['step']))

def blue_actions_2(situation, command):
    redSituation = situation['redSituation']
    blueSituation = situation['blueSituation']
    for blue_id, blue_entities in blueSituation.items():
        if blue_id == blue_type_2[1]:
            for blue_entity in blue_entities:
                blue_name = blue_entity['name']
                blue_lon = blue_entity['longitude']
                blue_lat = blue_entity['latitude']
                if blue_entity['life'] > 0 and situation['step'] == 1:
                    new_blue_lon = blue_lon - 0.5 * math.cos((int(blue_name[-1]) - 2) * 22.5 / 180 * math.pi)
                    new_blue_lat = blue_lat - 0.5 * math.sin((int(blue_name[-1]) - 2) * 22.5 / 180 * math.pi)

                    blue_action = {}
                    blue_action['agentname'] = blue_name
                    blue_action['longitude'] = new_blue_lon
                    blue_action['latitude'] = new_blue_lat
                    blue_action['altitude'] = 0
                    # print(blue_action)
                    # print(command)
                    command['moveactions'].append(blue_action)
                elif blue_entity['life'] > 0 and situation['step'] > 10:
                    for red_id, red_entities in redSituation.items():
                        if red_id == red_type_2[1]:
                            red_targetname = None
                            red_targetlon = None
                            red_targetlat = None
                            target_range = 10000
                            for red_entity in red_entities:
                                if red_entity['life'] > 0:
                                    if target_range > geodesic((red_entity['latitude'], red_entity['longitude']), (blue_lat, blue_lon)).km:
                                        red_targetname = red_entity['name']
                                        red_targetlat = red_entity['latitude']
                                        red_targetlon = red_entity['longitude']
                                        target_range = geodesic((red_entity['latitude'], red_entity['longitude']), (blue_lat, blue_lon)).km

                            if red_targetname is not None:
                                blue_action = {}
                                blue_action['agentname'] = blue_name
                                blue_action['longitude'] = red_targetlon
                                blue_action['latitude'] = red_targetlat
                                blue_action['altitude'] = 0
                                command['moveactions'].append(blue_action)
                                blue_action1 = {}
                                blue_action1['agentname'] = blue_name
                                blue_action1['targetname'] = [red_targetname]
                                command['fireactions'].append(blue_action1)
        elif blue_id == blue_type_2[2]:
            for blue_entity in blue_entities:
                blue_name = blue_entity['name']

                blue_action = {}
                blue_action['agentname'] = blue_name
                blue_action['longitude'] = blue_location_2[int(blue_name[-1])][0] + random.random() * 0.25
                blue_action['latitude'] = blue_location_2[int(blue_name[-1])][1] + random.random() * 0.25
                blue_action['altitude'] = 0
                command['moveactions'].append(blue_action)
        elif blue_id == blue_type_2[3]:
            for blue_entity in blue_entities:
                blue_name = blue_entity['name']
                blue_lon = blue_entity['longitude']
                blue_lat = blue_entity['latitude']
                if blue_entity['life'] > 0 and situation['step'] > 0:
                    red_targetname = None
                    red_targetlon = None
                    red_targetlat = None
                    target_range = 10000
                    for red_id, red_entities in redSituation.items():
                        if red_id == red_type_2[3]:
                            for red_entity in red_entities:
                                if red_entity['life'] > 0:
                                    if target_range > geodesic((red_entity['latitude'], red_entity['longitude']), (blue_lat, blue_lon)).km:
                                        red_targetname = red_entity['name']
                                        red_targetlat = red_entity['latitude']
                                        red_targetlon = red_entity['longitude']
                                        target_range = geodesic((red_entity['latitude'], red_entity['longitude']), (blue_lat, blue_lon)).km

                    if red_targetname is not None:
                        blue_action = {}
                        blue_action['agentname'] = blue_name
                        blue_action['longitude'] = red_targetlon
                        blue_action['latitude'] = red_targetlat
                        blue_action['altitude'] = 0
                        command['moveactions'].append(blue_action)
                        blue_action1 = {}
                        blue_action1['agentname'] = blue_name
                        blue_action1['targetname'] = [red_targetname]
                        command['fireactions'].append(blue_action1)

        elif blue_id == blue_type_2[4]:
            red_RAD_location = []
            for red_id, red_entities in redSituation.items():
                if red_id == red_type_2[-1]:
                    for red_entity in red_entities:
                        red_RAD_location.append([red_entity['longitude'], red_entity['latitude']])

            for blue_entity in blue_entities:
                blue_name = blue_entity['name']
                m = int(blue_name[-1]) % 8
                if m < 3:
                    blue_action = {}
                    blue_action['agentname'] = blue_name
                    blue_action['longitude'] = red_RAD_location[m][0]
                    blue_action['latitude'] = red_RAD_location[m][1]
                    blue_action['altitude'] = 0
                    command['moveactions'].append(blue_action)
                    blue_action1 = {}
                    blue_action1['agentname'] = blue_name
                    blue_action1['targetname'] = [red_RAD_2[m]]
                    command['fireactions'].append(blue_action1)

    return command


def red_actions_2(situation, command):
    redSituation = situation['redSituation']
    blueSituation = situation['blueSituation']
    for red_id, red_entities in redSituation.items():
        if red_id == red_type_2[2]:
            for red_entity in red_entities:
                red_name = red_entity['name']
                red_lon = red_entity['longitude']
                red_lat = red_entity['latitude']
                if situation['step'] < 10:
                    red_action = {}
                    red_action['agentname'] = red_name
                    red_action['longitude'] = red_location_2[int(red_name[-1]) % 2][0] + random.random() * 0.25
                    red_action['latitude'] = red_location_2[int(red_name[-1]) % 2][1] + random.random() * 0.25
                    red_action['altitude'] = 0
                    command['moveactions'].append(red_action)
                else:
                    if int(red_name[-1]) == 0 or int(red_name[-1]) == 1:
                        red_action = {}
                        red_action['agentname'] = red_name
                        red_action['longitude'] = red_location_2[int(red_name[-1]) + 2][0] + random.random() * 0.25
                        red_action['latitude'] = red_location_2[int(red_name[-1]) + 2][1] + random.random() * 0.25
                        red_action['altitude'] = 0
                        command['moveactions'].append(red_action)
                    else:
                        red_action = {}
                        red_action['agentname'] = red_name
                        red_action['longitude'] = red_location_2[int(red_name[-1]) % 2][0] + random.random() * 0.25
                        red_action['latitude'] = red_location_2[int(red_name[-1]) % 2][1] + random.random() * 0.25
                        red_action['altitude'] = 0
                        command['moveactions'].append(red_action)

        elif red_id == red_type_2[1]:
            for red_entity in red_entities:
                if red_entity['life'] > 0:
                    red_name = red_entity['name']
                    red_lon = red_entity['longitude']
                    red_lat = red_entity['latitude']
                    if int(red_name[-1]) == 0 or int(red_name[-1]) == 1:
                        if situation['step'] < 10:
                            red_action = {}
                            red_action['agentname'] = red_name
                            red_action['longitude'] = red_location_2[int(red_name[-1])][0]
                            red_action['latitude'] = red_location_2[int(red_name[-1])][1]
                            red_action['altitude'] = 0
                            command['moveactions'].append(red_action)
                        else:
                            for blue_id, blue_entities in blueSituation.items():
                                if blue_id == blue_type_2[1]:
                                    blue_targetname = None
                                    blue_targetlon = None
                                    blue_targetlat = None
                                    target_range = 10000
                                    for blue_entity in blue_entities:
                                        if blue_entity['life'] > 0:
                                            if target_range > geodesic(
                                                    (blue_entity['latitude'], blue_entity['longitude']),
                                                    (red_lat, red_lon)).km:
                                                blue_targetname = blue_entity['name']
                                                blue_targetlat = blue_entity['latitude']
                                                blue_targetlon = blue_entity['longitude']
                                                target_range = geodesic(
                                                    (blue_entity['latitude'], blue_entity['longitude']),
                                                    (red_lat, red_lon)).km

                                    if blue_targetname is not None:
                                        if red_lon - blue_targetlon > 0:
                                            direction = math.acos((red_lat - blue_targetlat) / (
                                                        (red_lat - blue_targetlat) ** 2 + (
                                                            red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180
                                        else:
                                            direction = 360 - math.acos((red_lat - blue_targetlat) / (
                                                        (red_lat - blue_targetlat) ** 2 + (
                                                            red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180

                                        direction = direction + (random.random() - 0.5) * 20

                                        longitude, latitude = getDistancePoint(blue_targetlon, blue_targetlat,
                                                                               10, direction)
                                        red_action = {}
                                        red_action['agentname'] = red_name
                                        red_action['longitude'] = longitude
                                        red_action['latitude'] = latitude
                                        red_action['altitude'] = 0
                                        command['moveactions'].append(red_action)
                                        red_action1 = {}
                                        red_action1['agentname'] = red_name
                                        red_action1['targetname'] = [blue_targetname]
                                        command['fireactions'].append(red_action1)
        elif red_id == red_type_2[3]:
            for red_entity in red_entities:
                red_name = red_entity['name']
                red_lon = red_entity['longitude']
                red_lat = red_entity['latitude']
                if int(red_name[-1]) == 0 or int(red_name[-1]) == 1:
                    for blue_id, blue_entities in blueSituation.items():
                        if blue_id == blue_type_2[1]:
                            blue_targetname = None
                            blue_targetlon = None
                            blue_targetlat = None
                            target_range = 10000
                            for blue_entity in blue_entities:
                                if blue_entity['life'] > 0:
                                    if target_range > geodesic(
                                            (blue_entity['latitude'], blue_entity['longitude']),
                                            (red_lat, red_lon)).km:
                                        blue_targetname = blue_entity['name']
                                        blue_targetlat = blue_entity['latitude']
                                        blue_targetlon = blue_entity['longitude']
                                        target_range = geodesic(
                                            (blue_entity['latitude'], blue_entity['longitude']),
                                            (red_lat, red_lon)).km

                            if blue_targetname is not None:
                                if red_lon - blue_targetlon > 0:
                                    direction = math.acos((red_lat - blue_targetlat) / (
                                            (red_lat - blue_targetlat) ** 2 + (
                                            red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180
                                else:
                                    direction = 360 - math.acos((red_lat - blue_targetlat) / (
                                            (red_lat - blue_targetlat) ** 2 + (
                                            red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180

                                direction = direction + (random.random() - 0.5) * 20

                                longitude, latitude = getDistancePoint(blue_targetlon, blue_targetlat,
                                                                       10, direction)
                                red_action = {}
                                red_action['agentname'] = red_name
                                red_action['longitude'] = longitude
                                red_action['latitude'] = latitude
                                red_action['altitude'] = 0
                                command['moveactions'].append(red_action)
                                red_action1 = {}
                                red_action1['agentname'] = red_name
                                red_action1['targetname'] = [blue_targetname]
                                command['fireactions'].append(red_action1)
                            else:
                                blue_targetname = None
                                blue_targetlon = None
                                blue_targetlat = None
                                target_range = 10000
                                for blue_id, blue_entities in blueSituation.items():
                                    if blue_id != blue_type_2[0] and blue_id != blue_type_2[4]:
                                        for blue_entity in blue_entities:
                                            if blue_entity['life'] > 0:
                                                if target_range > geodesic(
                                                        (blue_entity['latitude'], blue_entity['longitude']),
                                                        (red_lat, red_lon)).km:
                                                    blue_targetname = blue_entity['name']
                                                    blue_targetlat = blue_entity['latitude']
                                                    blue_targetlon = blue_entity['longitude']
                                                    target_range = geodesic(
                                                        (blue_entity['latitude'], blue_entity['longitude']),
                                                        (red_lat, red_lon)).km

                                if blue_targetname is not None:
                                    if red_lon - blue_targetlon > 0:
                                        direction = math.acos((red_lat - blue_targetlat) / (
                                                (red_lat - blue_targetlat) ** 2 + (
                                                red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180
                                    else:
                                        direction = 360 - math.acos((red_lat - blue_targetlat) / (
                                                (red_lat - blue_targetlat) ** 2 + (
                                                red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180

                                    direction = direction + (random.random() - 0.5) * 20

                                    longitude, latitude = getDistancePoint(blue_targetlon, blue_targetlat,
                                                                           10, direction)
                                    red_action = {}
                                    red_action['agentname'] = red_name
                                    red_action['longitude'] = longitude
                                    red_action['latitude'] = latitude
                                    red_action['altitude'] = 0
                                    command['moveactions'].append(red_action)
                                    red_action1 = {}
                                    red_action1['agentname'] = red_name
                                    red_action1['targetname'] = [blue_targetname]
                                    command['fireactions'].append(red_action1)
                elif int(red_name[-1]) == 2 or int(red_name[-1]) == 3:
                    for blue_id, blue_entities in blueSituation.items():
                        if blue_id == blue_type_2[3]:
                            blue_targetname = None
                            blue_targetlon = None
                            blue_targetlat = None
                            target_range = 10000
                            for blue_entity in blue_entities:
                                if blue_entity['life'] > 0:
                                    if target_range > geodesic(
                                            (blue_entity['latitude'], blue_entity['longitude']),
                                            (red_lat, red_lon)).km:
                                        blue_targetname = blue_entity['name']
                                        blue_targetlat = blue_entity['latitude']
                                        blue_targetlon = blue_entity['longitude']
                                        target_range = geodesic(
                                            (blue_entity['latitude'], blue_entity['longitude']),
                                            (red_lat, red_lon)).km

                            if blue_targetname is not None:
                                if red_lon - blue_targetlon > 0:
                                    direction = math.acos((red_lat - blue_targetlat) / (
                                            (red_lat - blue_targetlat) ** 2 + (
                                            red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180
                                else:
                                    direction = 360 - math.acos((red_lat - blue_targetlat) / (
                                            (red_lat - blue_targetlat) ** 2 + (
                                            red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180

                                direction = direction + (random.random() - 0.5) * 20

                                longitude, latitude = getDistancePoint(blue_targetlon, blue_targetlat,
                                                                       10, direction)
                                red_action = {}
                                red_action['agentname'] = red_name
                                red_action['longitude'] = longitude
                                red_action['latitude'] = latitude
                                red_action['altitude'] = 0
                                command['moveactions'].append(red_action)
                                red_action1 = {}
                                red_action1['agentname'] = red_name
                                red_action1['targetname'] = [blue_targetname]
                                command['fireactions'].append(red_action1)
                            else:
                                blue_targetname = None
                                blue_targetlon = None
                                blue_targetlat = None
                                target_range = 10000
                                for blue_id, blue_entities in blueSituation.items():
                                    if blue_id != blue_type_2[0] and blue_id != blue_type_2[4]:
                                        for blue_entity in blue_entities:
                                            if blue_entity['life'] > 0:
                                                if target_range > geodesic(
                                                        (blue_entity['latitude'], blue_entity['longitude']),
                                                        (red_lat, red_lon)).km:
                                                    blue_targetname = blue_entity['name']
                                                    blue_targetlat = blue_entity['latitude']
                                                    blue_targetlon = blue_entity['longitude']
                                                    target_range = geodesic(
                                                        (blue_entity['latitude'], blue_entity['longitude']),
                                                        (red_lat, red_lon)).km

                                if blue_targetname is not None:
                                    if red_lon - blue_targetlon > 0:
                                        direction = math.acos((red_lat - blue_targetlat) / (
                                                (red_lat - blue_targetlat) ** 2 + (
                                                red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180
                                    else:
                                        direction = 360 - math.acos((red_lat - blue_targetlat) / (
                                                (red_lat - blue_targetlat) ** 2 + (
                                                red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180

                                    direction = direction + (random.random() - 0.5) * 20

                                    longitude, latitude = getDistancePoint(blue_targetlon, blue_targetlat,
                                                                           10, direction)
                                    red_action = {}
                                    red_action['agentname'] = red_name
                                    red_action['longitude'] = longitude
                                    red_action['latitude'] = latitude
                                    red_action['altitude'] = 0
                                    command['moveactions'].append(red_action)
                                    red_action1 = {}
                                    red_action1['agentname'] = red_name
                                    red_action1['targetname'] = [blue_targetname]
                                    command['fireactions'].append(red_action1)
                elif int(red_name[-1]) == 4 or int(red_name[-1]) == 5:
                    blue_targetname = None
                    blue_targetlon = None
                    blue_targetlat = None
                    target_range = 10000
                    for blue_id, blue_entities in blueSituation.items():
                        if blue_id != blue_type_2[0] and blue_id != blue_type_2[4]:
                            for blue_entity in blue_entities:
                                if blue_entity['life'] > 0:
                                    if target_range > geodesic(
                                            (blue_entity['latitude'], blue_entity['longitude']),
                                            (red_lat, red_lon)).km:
                                        blue_targetname = blue_entity['name']
                                        blue_targetlat = blue_entity['latitude']
                                        blue_targetlon = blue_entity['longitude']
                                        target_range = geodesic(
                                            (blue_entity['latitude'], blue_entity['longitude']),
                                            (red_lat, red_lon)).km

                    if blue_targetname is not None:
                        if red_lon - blue_targetlon > 0:
                            direction = math.acos((red_lat - blue_targetlat) / (
                                    (red_lat - blue_targetlat) ** 2 + (
                                    red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180
                        else:
                            direction = 360 - math.acos((red_lat - blue_targetlat) / (
                                    (red_lat - blue_targetlat) ** 2 + (
                                    red_lon - blue_targetlon) ** 2) ** 0.5) / math.pi * 180

                        direction = direction + (random.random() - 0.5) * 20

                        longitude, latitude = getDistancePoint(blue_targetlon, blue_targetlat,
                                                               10, direction)
                        red_action = {}
                        red_action['agentname'] = red_name
                        red_action['longitude'] = longitude
                        red_action['latitude'] = latitude
                        red_action['altitude'] = 0
                        command['moveactions'].append(red_action)
                        red_action1 = {}
                        red_action1['agentname'] = red_name
                        red_action1['targetname'] = [blue_targetname]
                        command['fireactions'].append(red_action1)
    return command





