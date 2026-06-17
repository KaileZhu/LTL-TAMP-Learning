from geopy.distance import geodesic
import geopy
import numpy as np
import random
import time
import copy
import matplotlib.pyplot as plt
import math
import os

red_agent_num = 81
blue_agent_num = 40

red_unit_type = ['redCommander', 'redCommanderMiddle', 'redAirArtillery', 'redRocketGun', 'redSAUGV', 'redRSUAVehicle',
                 'redRSUAV',
                 'redFSUAVehicle', 'redFSUAV', 'redArCMUGV', 'redInCOUGH', 'redAJUGV', 'redArCMissle', 'redInCMissle',
                 'redsuicideUAV']

blue_unit_type = ['blueCommander', 'blueUAVehicle', 'blueCommandMiddle', 'blueInfantry', 'blueArtillery',
                  'blueArchibald',
                  'blueADLanucher', 'blueCommNode', 'blueRadar', 'blueUAV']

red = [
    'Red.RedForce_RedCommander#0',
    'Red.RedForce_RedCommander#0_RedCommanderMiddle#0',
    'Red.RedForce_RedCommander#0_RedAirArtillery#0',
    'Red.RedForce_RedCommander#0_RedAirArtillery#1',
    'Red.RedForce_RedCommander#0_RedAirArtillery#2',
    'Red.RedForce_RedCommander#0_RedAirArtillery#3',
    'Red.RedForce_RedCommander#0_RedRocketGun#0',
    'Red.RedForce_RedCommander#0_RedRocketGun#1',
    'Red.RedForce_RedCommander#0_RedRocketGun#2',
    'Red.RedForce_RedCommander#0_RedRocketGun#3',
    'Red.RedForce_RedCommander#0_RedRocketGun#4',
    'Red.RedForce_RedCommander#0_RedSAUGV#0',
    'Red.RedForce_RedCommander#0_RedSAUGV#1',
    'Red.RedForce_RedCommander#0_RedSAUGV#2',
    'Red.RedForce_RedCommander#0_RedSAUGV#3',
    'Red.RedForce_RedCommander#0_RedSAUGV#4',
    'Red.RedForce_RedCommander#0_RedSAUGV#5',
    'Red.RedForce_RedCommander#0_RedSAUGV#6',
    'Red.RedForce_RedCommander#0_RedSAUGV#7',
    'Red.RedForce_RedCommander#0_RedRSUAVehicle#0',
    'Red.RedForce_RedCommander#0_RedRSUAVehicle#1',
    'Red.RedForce_RedCommander#0_RedRSUAVehicle#2',
    'Red.RedForce_RedCommander#0_RedRSUAVehicle#0.RedRSUAV#0',
    'Red.RedForce_RedCommander#0_RedRSUAVehicle#1.RedRSUAV#0',
    'Red.RedForce_RedCommander#0_RedRSUAVehicle#2.RedRSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#1',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#2',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#3',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#4',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#5',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#6',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#7',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#8',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#9',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#0.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#1.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#2.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#3.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#4.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#5.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#6.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#7.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#8.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedFSUAVehicle#9.RedFSUAV#0',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0',
    'Red.RedForce_RedCommander#0_RedAJUGV#0',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#0',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#1',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#2',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#3',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#4',
    'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#5',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#0',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#1',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#2',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#3',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#4',
    'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#5',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#0',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#1',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#2',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#3',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#4',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#5',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#6',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#7',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#8',
    'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#9',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#0',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#1',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#2',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#3',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#4',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#5',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#6',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#7',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#8',
    'Red.RedForce_RedCommander#0_RedsuicideUAV#9',
]

blue = [
    'Blue.BlueForce_BlueCommander#0',
    'Blue.BlueForce_BlueCommander#0_BlueUAVehicle#0',
    'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#0',
    'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#1',
    'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#2',
    'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#3',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#0',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#1',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#2',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#3',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#4',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#5',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#6',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#7',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#8',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#9',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#10',
    'Blue.BlueForce_BlueCommander#0_BlueInfantry#11',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#0',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#1',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#2',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#3',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#4',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#5',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#6',
    'Blue.BlueForce_BlueCommander#0_BlueArtillery#7',
    'Blue.BlueForce_BlueCommander#0_BlueArchibald#0',
    'Blue.BlueForce_BlueCommander#0_BlueArchibald#1',
    'Blue.BlueForce_BlueCommander#0_BlueADLanucher#0',
    'Blue.BlueForce_BlueCommander#0_BlueADLanucher#1',
    'Blue.BlueForce_BlueCommander#0_BlueADLanucher#2',
    'Blue.BlueForce_BlueCommander#0_BlueCommNode#0',
    'Blue.BlueForce_BlueCommander#0_BlueRadar#0',
    'Blue.BlueForce_BlueCommander#0_BlueRadar#1',
    'Blue.BlueForce_BlueCommander#0_BlueUAV#0',
    'Blue.BlueForce_BlueCommander#0_BlueUAV#1',
    'Blue.BlueForce_BlueCommander#0_BlueUAV#2',
    'Blue.BlueForce_BlueCommander#0_BlueUAV#3',
    'Blue.BlueForce_BlueCommander#0_BlueUAV#4',
    'Blue.BlueForce_BlueCommander#0_BlueUAV#5'
]

redCommander = red[0:2]  # 红方指挥所
redAirArtillery = red[2:6]  # 红方自动化防空高炮
redRocketGun = red[6:11]  # 红方无人值守火箭炮
redSAUGV = red[11:19]  # 红方察打一体无人车
redRSUAVehicle = red[19:22]  # 红方旋翼侦察无人机运载车
redRSUAV = red[22:25]  # 红方旋翼侦察无人机
redFSUAVehicle = red[25:35]  # 红方固定翼侦察无人机运载车
redFSUAV = red[35:45]  # 红方固定翼侦察无人机
redArCMUGV = red[45:47]  # 红方反辐射巡飞弹发射车
redInCMUGV = red[47]  # 红方红外巡飞弹发射车
redAJUGV = red[48]  # 红方反干扰无人车
redArCMissle = red[49:61]  # 红方反辐射巡飞弹
redInCMissle = red[61:71]  # 红方红外巡飞弹
redsuicideUAV = red[71:]  # 红方自杀式无人机
redMissle = red[49:71]

blueCommander = blue[0]
blueUAVehicle = blue[1]
blueCommandMiddle = blue[2:6]
blueInfantry = blue[6:18]  # 蓝方步兵
blueArtillery = blue[18:26]  # 蓝方炮兵
blueArchibald = blue[26:28]
blueADLanucher = blue[28:31]
blueCommNode = blue[31]
blueRadar = blue[32:34]
blueUAV = blue[34:]

blueInf = blueInfantry
blueArt = blueArtillery

location_mapping = {'a': [[77, 29], [77, 30], [78, 30], [78, 29]], 'b': [[78, 29], [78, 30], [79, 30], [79, 29]],
                    'c': [[79, 29], [79, 30], [80, 30], [80, 29]], 'd': [[80, 29], [80, 30], [81, 30], [81, 29]],
                    'e': [[77, 30], [77, 31], [78, 31], [78, 30]], 'f': [[78, 30], [78, 31], [79, 31], [79, 30]],
                    'g': [[79, 30], [79, 31], [80, 31], [80, 30]], 'h': [[80, 30], [80, 31], [81, 31], [81, 30]],
                    'i': [[77, 31], [77, 32], [78, 32], [78, 31]], 'j': [[78, 31], [78, 32], [79, 32], [79, 31]],
                    'k': [[79, 31], [79, 32], [80, 32], [80, 31]], 'l': [[80, 31], [80, 32], [81, 32], [81, 31]],
                    'm': [[77, 32], [77, 33], [78, 33], [78, 32]], 'n': [[78, 32], [78, 33], [79, 33], [79, 32]],
                    'o': [[79, 32], [79, 33], [80, 33], [80, 32]], 'p': [[80, 32], [80, 33], [81, 33], [81, 32]]}
red_unit_life = [
    100, 10,
    10, 10, 10, 10,
    10, 10, 10, 10, 10,
    35, 35, 35, 35, 35, 35, 35, 35,
    10, 10, 10,
    10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10,
    10,
    10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10
]

blue_unit_life = [
    100,
    10,
    20, 20, 20, 20,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10,
    10, 10,
    10, 10, 10,
    10,
    10, 10,
    10, 10, 10, 10, 10, 10
]

# todo: consider how to adjsut
redRSUAV_location = [[79.54, 30.54], [79.35, 30.32], [79.01, 30.52]]
redFSUAV_location = [[79.90, 30.38], [79.59, 30.08], [79.90, 30.02]]

blue_entity_area_mapping = ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'h', 'd', 'f', 'f', 'g', 'g', 'g', 'g',
                            'g', 'g', 'g', 'd', 'd', 'f', 'f', 'g', 'g', 'f', 'c', 'f', 'f', 'g', 'g', 'g', 'g', 'g',
                            'g', 'g', 'g', 'g']


def compute_acc_reward(obs):
    index = 0
    blue_life = [-1 for _ in range(40)]
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['life'] <= 0:
                blue_life[index] = 0
            else:
                blue_life[index] = entity['life']
            index += 1

    index = 0
    red_life = [1 for _ in range(81)]
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
        10, 4,
        1, 1, 1, 1,
        1, 1, 1, 1, 1,
        8, 8, 8, 8, 8, 8, 8, 8,
        2, 2, 2,
        3, 3, 3,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        2, 2,
        2,
        2,
        0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ]

    blue_weight = [
        10,
        1,
        4, 4, 4, 4,
        5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
        9, 9, 9, 9, 9, 9, 9, 9,
        2, 2,
        2, 2, 2,
        4,
        2, 2,
        3, 3, 3, 3, 3, 3
    ]

    blue_survive_reward = 0
    red_survive_reward = 0
    for i in range(40):
        if blue_life[i] > 0:
            blue_survive_reward = blue_survive_reward + blue_weight[i]

    for i in range(81):
        if red_life[i] > 0:
            red_survive_reward = red_survive_reward + red_weight[i]

    return red_survive_reward - blue_survive_reward + red_life_reward - blue_life_reward + 20


def state_situation(obs):
    status = {}

    red_state = []
    red_damage = []
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            entity_state_dict = {}
            entity_damage_dict = {}
            if entity['life'] <= 0:
                entity_damage_dict['agent_ID'] = entity['name']
                entity_damage_dict['unit_type'] = red_unit_type.index(id)
                entity_damage_dict['location_x'] = entity['longitude']
                entity_damage_dict['location_y'] = entity['latitude']
            else:
                entity_state_dict['agnet_ID'] = entity['name']
                entity_state_dict['unit_type'] = red_unit_type.index(id)
                entity_state_dict['location_x'] = entity['longitude']
                entity_state_dict['location_y'] = entity['latitude']
                entity_state_dict['life'] = entity['life']
                entity_state_dict['speed'] = entity['speed']

            if entity_state_dict:
                red_state.append(entity_state_dict)

            if entity_damage_dict:
                red_damage.append(entity_damage_dict)

    blue_state = []
    blue_damage = []
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            entity_state_dict = {}
            entity_damage_dict = {}
            if entity['life'] <= 0:
                entity_damage_dict['agent_ID'] = entity['name']
                entity_damage_dict['unit_type'] = blue_unit_type.index(id) + 15
                entity_damage_dict['location_x'] = entity['longitude']
                entity_damage_dict['location_y'] = entity['latitude']
            else:
                entity_state_dict['agnet_ID'] = entity['name']
                entity_state_dict['unit_type'] = blue_unit_type.index(id) + 15
                entity_state_dict['location_x'] = entity['longitude']
                entity_state_dict['location_y'] = entity['latitude']
                entity_state_dict['life'] = entity['life']
                entity_state_dict['speed'] = entity['speed']

            if entity_state_dict:
                blue_state.append(entity_state_dict)

            if entity_damage_dict:
                blue_damage.append(entity_damage_dict)

    status['redStatus'] = red_state
    status['redDamage'] = red_damage
    status['blueStatus'] = blue_state
    status['blueDamage'] = blue_damage

    return status


def blue_action(obs, command):
    location_x = []
    location_y = []
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if id == 'redSAUGV':

                if entity['life'] > 0 and entity['longitude'] < 80.2 and entity['latitude'] < 30.7:
                    # print('发现红方SAUGV')
                    location_x.append(entity['longitude'])
                    location_y.append(entity['latitude'])

    if len(location_x) != 0:
        for id, entities in obs['blueSituation'].items():
            for entity in entities:
                if id == 'blueInfantry' or id == 'blueArtillery':
                    if entity['life'] > 0:
                        action = {}
                        action['agentname'] = entity['name']

                        range_list = []
                        for i in range(len(location_x)):
                            range_list.append(
                                geodesic((entity['latitude'], entity['longitude']), (location_y[i], location_x[i])).km)
                        index = range_list.index(min(range_list))
                        action['longitude'] = location_x[index]
                        action['latitude'] = location_y[index]
                        action['altitude'] = 0
                        # print('蓝方开始移动')
                        command['moveactions'].append(action)

    # if len(location_x) != 0:
        # print(command)



    # 控制UAV
    index = 0
    angle_list = [30, 36, 42, 60, 66, 72]
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['name'] in blueUAV and entity['life'] > 0:
                action = {}
                action['agentname'] = entity['name']
                local_id = index - 34
                angle = angle_list[local_id]
                entity_location_x = entity['longitude']
                entity_location_y = entity['latitude']

                longitude, latitude = getDistancePoint(entity_location_x, entity_location_y, 10,
                                                       angle)
                action['longitude'] = longitude
                action['latitude'] = latitude
                action['altitude'] = 0
                if entity_location_x < 81.0 and entity_location_y < 31.0:
                    command['scoutactions'].append(action)

            index += 1

    return command


def red_action(obs, command):
    location_x = []
    location_y = []
    name = []
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['life'] > 0:
                location_x.append(entity['longitude'])
                location_y.append(entity['latitude'])
                name.append(entity['name'])

    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if id == 'redSAUGV':
                if entity['life'] > 0:
                    action = {}
                    action_ = {}
                    action['agentname'] = entity['name']
                    action_['agentname'] = entity['name']

                    range_list = []
                    for i in range(len(location_x)):
                        range_list.append(
                            geodesic((entity['latitude'], entity['longitude']), (location_y[i], location_x[i])).km)
                    index = range_list.index(min(range_list))
                    action['longitude'] = location_x[index]
                    action['latitude'] = location_y[index]
                    action['altitude'] = 0

                    command['moveactions'].append(action)

                    action_['targetname'] = [name[index]]
                    command['fireactions'].append(action_)
            elif id == 'redRSUAV':
                if entity['life'] > 0:
                    action = {}
                    action['agentname'] = entity['name']
                    index = redRSUAV.index(entity['name'])

                    location_x_, location_y_ = get_point_location(redRSUAV_location[index][0],
                                                                  redRSUAV_location[index][1], 0.03)
                    action['longitude'] = location_x_
                    action['latitude'] = location_y_
                    action['altitude'] = 0

                    command['moveactions'].append(action)
            elif id == 'redFSUAV':
                if entity['life'] > 0:
                    action = {}
                    action['agentname'] = entity['name']
                    index = redFSUAV.index(entity['name'])

                    location_x_, location_y_ = get_point_location(redFSUAV_location[index][0],
                                                                  redFSUAV_location[index][1], 0.03)
                    action['longitude'] = location_x_
                    action['latitude'] = location_y_
                    action['altitude'] = 0

                    command['moveactions'].append(action)
            elif id == 'redArCMissle' or id == 'redInCMissle':
                if entity['life'] > 0 and obs['step'] > 10:
                    index = redMissle.index(entity['name'])

                    action = {}
                    action_ = {}
                    action['agentname'] = entity['name']
                    action_['agentname'] = entity['name']

                    for _, entities in obs['blueSituation'].items():
                        for entity in entities:
                            if entity['name'] == blue[index]:
                                action['longitude'] = entity['longitude']
                                action['latitude'] = entity['latitude']
                                action['altitude'] = 0

                    command['moveactions'].append(action)

                    action_['targetname'] = [blue[index]]
                    command['fireactions'].append(action_)
    return command


def get_point_location(location_x, location_y, dis):
    location_x_ = location_x + (random.random() - 0.5) * 2 * dis
    location_y_ = location_y + (random.random() - 0.5) * 2 * dis
    return location_x_, location_y_


def get_task(path):
    fi = open(path, 'r')
    txt = fi.readlines()
    i = 0
    for w in txt:
        txt[i] = w.replace(',\n', '').replace('\'', '').replace(' ', '').replace('[[', '[').replace(')', '').replace(
            '((', '').replace('[', '').split(',')
        i += 1

    unit_task = [[] for _ in range(53)]
    unit_task_context = [[] for _ in range(53)]
    unit_task_num = [0 for _ in range(53)]
    unit_index = 0
    for i in range(len(txt)):
        if len(txt[i]) == 1:
            unit_task[unit_index].append(100)

            unit_index += 1
        else:
            unit_task[unit_index].append(int(txt[i][0][0]))
            unit_task_context[unit_index].append(txt[i][2:5])
            unit_task_num[unit_index] += 1
            if txt[i][-1][-1] == ']':
                unit_index += 1

    unit_task_now = [unit_task[i][0] for i in range(53)]
    unit_task_num_now = [0 for _ in range(53)]

    task, task_context, task_now, task_num, task_num_now = unit_task, unit_task_context, unit_task_now, unit_task_num, unit_task_num_now
    task_num_list = []
    for task_single in task:
        for task_num in task_single:
            if task_num not in task_num_list and task_num != 100 and task_num != -1:
                task_num_list.append(task_num)

    return unit_task, unit_task_context, unit_task_now, unit_task_num, unit_task_num_now, task_num_list


def get_task_constrain(task_now_):
    task_now = copy.deepcopy(task_now_)
    if 1 in task_now or 2 in task_now or 0 in task_now:
        for i in range(len(task_now)):
            if task_now[i] == 3 or task_now[i] == 4 or task_now[i] == 5:
                task_now[i] = 100
    elif 3 in task_now or 4 in task_now:
        for i in range(len(task_now)):
            if task_now[i] == 5:
                task_now[i] = 100

    return task_now


def is_task_done(obs, context, unit_name):
    task_type = context[0]
    target_area = context[1]
    target_type = context[2]

    # reset life to 0 when agents died
    index = 0
    blue_life = [1 for _ in range(blue_agent_num)]
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['life'] <= 0:
                blue_life[index] = 0
            index += 1

    index = 0
    red_life = [1 for _ in range(red_agent_num)]
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if entity['life'] <= 0:
                red_life[index] = 0
            index += 1

    if task_type == 'observe':
        if target_type == 'all':
            # 1125 修改侦察任务完成条件
            for red_id, red_entities in obs['redSituation'].items():
                for red_entity in red_entities:
                    if red_entity['name'] == unit_name:
                        unit_lat = red_entity['latitude']
                        unit_lon = red_entity['longitude']
                        if location_mapping[target_area][1][1] > unit_lat > location_mapping[target_area][0][1] \
                                and location_mapping[target_area][2][0] > unit_lon > location_mapping[target_area][0][
                            0]:
                            return True
                        else:
                            return False

            # 如果这个区域内有蓝方实体（这任务目标 除了蓝方死完能完成么？？？）
            # if target_area in blue_entity_area_mapping:
            #     is_detect = [0 for _ in range(blue_agent_num)]
            #     is_detect[blue_entity_area_mapping != target_area] = 1  # 非当前区域内的自动置1，最后用sum判断
            #
            #     index = 0
            #     for blue_id, blue_entities in obs['blueSituation'].items():
            #         for blue_entity in blue_entities:
            #             # 死了也探测到
            #             if blue_entity['life'] <= 0:
            #                 is_detect[index] = 1
            #                 index += 1
            #                 continue
            #             # 蓝方UAV摆了
            #             elif blue_entity['name'] in blueUAV:
            #                 is_detect[index] = 1
            #                 index += 1
            #                 continue
            #             # 已经是1（不在考察范围内的）也摆了
            #             elif is_detect[index] == 1:
            #                 index += 1
            #                 continue
            #             else:
            #                 target_lat = blue_entity['latitude']
            #                 target_lon = blue_entity['longitude']
            #                 flag = 0
            #                 for red_id, red_entities in obs['redSituation'].items():
            #                     if red_id in ['redRSUAV', 'redFSUAV']:
            #                         for red_entity in red_entities:
            #                             if red_entity['range'] >= geodesic((target_lat, target_lon),
            #                                                                (red_entity['latitude'],
            #                                                                 red_entity['longitude'])).km:
            #                                 is_detect[index] = 1
            #                                 flag = 1
            #                                 break
            #
            #                     if flag == 1:
            #                         break
            #                 index += 1
            #     if sum(is_detect) == blue_agent_num:
            #         return True
            #     else:
            #         return False

            # 没有的话 到了就行
            else:
                for red_id, red_entities in obs['redSituation'].items():
                    for red_entity in red_entities:
                        if red_entity['name'] == unit_name:
                            unit_lat = red_entity['latitude']
                            unit_lon = red_entity['longitude']
                            if location_mapping[target_area][1][1] > unit_lat > location_mapping[target_area][0][1] \
                                    and location_mapping[target_area][2][0] > unit_lon > location_mapping[target_area][0][0]:
                                return True
                            else:
                                return False

    elif task_type == 'attack':
        if target_type == 'infantry':
            index = 0
            life = [1 for _ in range(blue_agent_num)]
            for blue_id, blue_entities in obs['blueSituation'].items():
                for blue_entity in blue_entities:
                    if blue_entity['life'] <= 0:
                        life[index] = 0
                    index += 1
            # more violent
            finish_flag = 1
            for index in range(6, 18):
                if life[index] != 0:
                    finish_flag = 0
                    break

            if finish_flag:
                return True
            else:
                return False

        elif target_type == 'artillery':
            index = 0
            life = [1 for _ in range(blue_agent_num)]
            for blue_id, blue_entities in obs['blueSituation'].items():
                for blue_entity in blue_entities:
                    if blue_entity['life'] <= 0:
                        life[index] = 0
                    index += 1

            finish_flag = 1
            for index in range(18, 26):
                if life[index] != 0:
                    finish_flag = 0
                    break

            if finish_flag:
                return True
            else:
                return False

        elif target_type == 'all':
            index = 0
            life = [1 for _ in range(blue_agent_num)]
            for blue_id, blue_entities in obs['blueSituation'].items():
                for blue_entity in blue_entities:
                    if blue_entity['life'] <= 0:
                        life[index] = 0
                    index += 1

            if sum(life) == 0:
                return True
            else:
                return False

    elif task_type == 'support':
        for red_id, red_entities in obs['redSituation'].items():
            for red_entity in red_entities:
                if red_entity['name'] == unit_name:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    if location_mapping[target_area][1][1] > unit_lat > location_mapping[target_area][0][1] \
                            and location_mapping[target_area][2][0] > unit_lon > location_mapping[target_area][0][0]:
                        return True
                    else:
                        return False


def get_red_staus(obs):
    unit_staus = [-1 for _ in range(red_agent_num)]
    index = 0
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if index >= 49 and index < 71:
                index += 1
                continue
            if red_entity['life'] <= 0:
                unit_staus[index] = 0
            elif red_entity['life'] == red_unit_life[index]:
                unit_staus[index] = 1
            else:
                unit_staus[index] = 2

            index += 1

    red_staus = {}
    # print(unit_staus)
    red_staus['step'] = obs['step']
    red_staus['red_damage_rate'] = unit_staus.count(2) / 59
    red_staus['red_live_rate'] = unit_staus.count(1) / 59
    red_staus['red_destroy_rate'] = unit_staus.count(0) / 59

    return red_staus


def get_blue_staus(obs):
    unit_staus = [-1 for _ in range(40)]
    index = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_entity['life'] <= 0:
                unit_staus[index] = 0
            elif blue_entity['life'] == blue_unit_life[index]:
                unit_staus[index] = 1
            else:
                unit_staus[index] = 2

            index += 1

    blue_staus = {}
    blue_staus['step'] = obs['step']
    blue_staus['blue_damage_rate'] = unit_staus.count(2) / 40
    blue_staus['blue_live_rate'] = unit_staus.count(1) / 40
    blue_staus['blue_destroy_rate'] = unit_staus.count(0) / 40

    return blue_staus


blue_threat = [5, 5, 4, 4, 4, 4, 8, 8, 8, 8, 10, 10, 10, 6, 6, 6, 3, 3, 6, 6, 6, 7]


def get_blue_threat(obs):
    index = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            threat = {}
            threat['agent_id'] = blue_entity['name']
            threat['threat'] = blue_threat[index]
            index += 1
            file = open('blue_threat.txt', mode='a')
            file.write(str(threat) + ',\n')
            file.close()


# blue_strength = [1, 0, 0, 0, 0, 0, 7, 7, 7, 7, 9, 9, 9, 0, 0, 0, 0, 0, 3, 4, 4, 4]
# red_strength = [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0]

red_strength = [
    1, 0,
    1, 1, 1, 1,
    1, 1, 1, 1, 1,
    16, 16, 16, 16, 16, 16, 16, 16,
    0, 0, 0,
    3, 3, 3,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    0, 0,
    0,
    0,
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2
]

blue_strength = [
    1,
    0,
    0, 0, 0, 0,
    7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
    9, 9, 9, 9, 9, 9, 9, 9,
    0, 0,
    4, 4, 4,
    0,
    2, 2,
    3, 3, 3, 3, 3, 3
]



def get_strength(obs):
    index = 0
    blue_mi_strength = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_entity['life'] > 0:
                blue_mi_strength += blue_strength[index] * blue_entity['life'] / blue_unit_life[index]
            index += 1

    index = 0
    red_mi_strength = 0
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if red_entity['life'] > 0:
                red_mi_strength += red_strength[index] * red_entity['life'] / red_unit_life[index]
            index += 1
    return red_mi_strength, blue_mi_strength


# blue_value = [10, 1, 4, 4, 4, 4, 5, 5, 5, 5, 7, 7, 7, 2, 2, 2, 2, 2, 3, 4, 4, 3]
# red_value = [10, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 8, 8, 8, 2, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 2, 2, 3, 3]
# red_value = red_value + [0.5 for _ in range(22)]

red_value = [
    10, 4,
    1, 1, 1, 1,
    1, 1, 1, 1, 1,
    8, 8, 8, 8, 8, 8, 8, 8,
    2, 2, 2,
    3, 3, 3,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    2, 2,
    2,
    2,
    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1
]

blue_value = [
    10,
    1,
    4, 4, 4, 4,
    5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
    9, 9, 9, 9, 9, 9, 9, 9,
    2, 2,
    2, 2, 2,
    4,
    2, 2,
    3, 3, 3, 3, 3, 3
]

def get_value(obs):
    index = 0
    blue_mi_value = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_entity['life'] > 0:
                if blue_id == 'blueInfantry' or blue_id == 'blueArtillery':
                    blue_mi_value += blue_value[index] * blue_entity['life'] / blue_unit_life[index]
                else:
                    blue_mi_value += blue_value[index]
            index += 1

    index = 0
    red_mi_value = 0
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if red_entity['life'] > 0:
                if red_id == 'redSAUGV':
                    red_mi_value += red_value[index] * red_entity['life'] / red_unit_life[index]
                else:
                    red_mi_value += red_value[index]
            index += 1
    return red_mi_value, blue_mi_value


def get_detect(obs, detect_list):
    index = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if detect_list[index] == 1:
                index += 1
                continue
            if blue_entity['life'] <= 0:
                detect_list[index] = 1
                index += 1
            else:
                done = False
                blue_location_x = blue_entity['latitude']
                blue_location_y = blue_entity['longitude']
                for red_id, red_entities in obs['redSituation'].items():
                    if red_id == 'redRSUAV' or red_id == 'redFSUAV':
                        for red_entity in red_entities:
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


def delete_path(dir_path):
    del_list = os.listdir(dir_path)
    for i in del_list:
        file_path = os.path.join(dir_path, i)
        if os.path.isfile(file_path):
            os.remove(file_path)

class Logger:
    def __init__(self):
        self.detect_list = [0 for i in range(blue_agent_num)]

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

        red_staus = get_red_staus(situationDataDict)
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

        blue_staus = get_blue_staus(situationDataDict)
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

        detect_ratio, self.detect_list = get_detect(situationDataDict, self.detect_list)
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

        red_mi_strength, blue_mi_strength = get_strength(situationDataDict)
        file = open('logger\common\strength.txt', mode='a')
        file.write('{\'step\':' + str(situationDataDict['step']) + ', \'red_ military_strength\':' + str(red_mi_strength) +
                   ', \'blue_ military_strength\':' + str(blue_mi_strength) + '},\n')
        file.close()

        red_mi_value, blue_mi_value = get_value(situationDataDict)
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
        plt.ylim(ymin=0, ymax=250)

        ax.legend(fontsize=front_size)
        ax.set_xticks(xticks + 0.125)
        ax.set_xticklabels(shops, fontsize=front_size)
        plt.yticks(fontsize=front_size)
        plt.savefig('planning/src/gui/assets/strength_value/' + str(situationDataDict['step']))
        plt.close()

        # 红/蓝方威胁程度
        shops = ['红方威胁度', '蓝方威胁度']
        strength = [red_mi_strength, blue_mi_strength]
        xticks = np.arange(len(shops))
        fig, ax = plt.subplots(figsize=(10, 9))
        ax.bar(xticks[0], strength[0], width=0.25, label='红方威胁度评估', color='red')
        ax.bar(xticks[1], strength[1], width=0.25, label='蓝方威胁度评估', color='blue')
        ax.set_ylabel('威胁度评估', fontdict=textprops)
        plt.ylim(ymin=0, ymax=250)

        ax.legend(fontsize=front_size)
        ax.set_xticks(xticks)
        ax.set_xticklabels(shops, fontsize=front_size)
        plt.yticks(fontsize=front_size)
        plt.savefig('planning/src/gui/assets/strength_value/strength_' + str(situationDataDict['step']))
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

        reward = compute_acc_reward(situationDataDict)
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
                if red_entity["name"] in redSAUGV:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    SAUGV_idx = red_entity["name"][-1]

                    lat_path = 'logger/SAUGV/'+SAUGV_idx+'_lat.txt'
                    lon_path = 'logger/SAUGV/'+SAUGV_idx+'_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()

                if red_entity["name"] in redRSUAV:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    RSUAV_idx = red_entity["name"][-12]

                    lat_path = 'logger/RSUAV/' + RSUAV_idx + '_lat.txt'
                    lon_path = 'logger/RSUAV/' + RSUAV_idx + '_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()

                if red_entity["name"] in redFSUAV:
                    unit_lat = red_entity['latitude']
                    unit_lon = red_entity['longitude']
                    FSUAV_idx = red_entity["name"][-12]

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
                if blue_entity["name"] in blueUAV:
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
                if blue_entity["name"] in blueInf:
                    unit_lat = blue_entity['latitude']
                    unit_lon = blue_entity['longitude']
                    Inf_idx = blue_entity["name"][-2:]

                    lat_path = 'logger/blueInf/'+Inf_idx+'_lat.txt'
                    lon_path = 'logger/blueInf/'+Inf_idx+'_lon.txt'
                    file = open(lat_path, mode='a')
                    file.write(str(unit_lat) + ',\n')
                    file.close()
                    file = open(lon_path, mode='a')
                    file.write(str(unit_lon) + ',\n')
                    file.close()
                if blue_entity["name"] in blueArt:
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
        for i in range(8):
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
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='red', linewidth=4, label="红方地面力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='red', linewidth=4)

        # 红方RSUAV
        for i in range(3):
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
                plt.scatter(lon_list[-1], lat_list[-1], marker='<', color='red', linewidth=4, label="红方空中力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='red', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='<', color='red', linewidth=4)

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
            plt.scatter(lon_list[-1], lat_list[-1], marker='<', color='red', linewidth=4)

        # 蓝方UAV
        for i in range(6):
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
                plt.scatter(lon_list[-1], lat_list[-1], marker='>', color='blue', linewidth=4, label="蓝方空中力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='>', color='blue', linewidth=4)


        # 蓝方Inf
        for i in range(12):
            if i < 10:
                lat_path = 'logger/blueInf/#' + str(i) + '_lat.txt'
            else:
                lat_path = 'logger/blueInf/'+str(i)+'_lat.txt'
            lat_list = []
            file = open(lat_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lat_list.append(float(line1[0]))
            file.close()

            if i < 10:
                lon_path = 'logger/blueInf/#'+str(i)+'_lon.txt'
            else:
                lon_path = 'logger/blueInf/'+str(i)+'_lon.txt'
            lon_list = []
            file = open(lon_path, mode='r')
            for line in file:
                line1 = line.split(',')
                lon_list.append(float(line1[0]))
            file.close()
            if i == 0:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='blue', linewidth=4, label="蓝方地面力量位置")
            else:
                plt.plot(lon_list[-min(20, len(lon_list)):], lat_list[-min(20, len(lat_list)):], color='blue', linewidth=2)
                plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='blue', linewidth=4)

        # 蓝方Art
        for i in range(8):
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
            plt.scatter(lon_list[-1], lat_list[-1], marker='s', color='blue', linewidth=4)

        plt.legend(loc='upper left', fontsize=18)
        plt.ylim(ymin=29.5, ymax=31.5)
        plt.xlim(xmin=78, xmax=81)
        plt.xlabel('经度', fontdict=textprops)
        plt.ylabel('纬度', fontdict=textprops)
        plt.yticks(fontsize=front_size)
        plt.xticks(fontsize=front_size)
        plt.savefig('planning/src/gui/assets/route/' + str(situationDataDict['step']))

# from CentralServer import red
# 禁止攻击
def rule_forbidden_attack(mask, forbidden_attack_list):
    for i in range(len(forbidden_attack_list)):
        index = blue.index(forbidden_attack_list[i])
        mask[:, index] = -100000

    return mask

# 协同攻击
def rule_collaborative_attack(obs, agentname):
    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if red_entity['name'] == agentname and red_entity['life'] > 0:
                location_x = red_entity["latitude"]
                location_y = red_entity['longitude']
                for red_id, red_entities_ in obs['redSituation'].items():
                    for red_entity_ in red_entities_:
                        if red_entity_["name"] == agentname:
                            continue
                        location_x_ = red_entity_["latitude"]
                        location_y_ = red_entity_['longitude']
                        if 2.0 > geodesic((location_x, location_y), (location_x_, location_y_)).km:
                            return True

    return False


# 紧急避险
def rule_forbidden_damage(obs, agentname):
    threat = 0
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_id in blue_unit_type[3:5] and blue_entity['life'] > 5:
                threat = 1
                break

    for red_id, red_entities in obs['redSituation'].items():
        for red_entity in red_entities:
            if red_entity['name'] == agentname and red_entity['life'] > 0:
                if red_entity['life'] < 5 and threat == 1:
                    return False
                else:
                    return True


# 无限火力
# 默认即为无限火力

# 无视威胁
def rule_ignore_threat(obs, mask, target_list, ran):
    for blue_id, blue_entities in obs['blueSituation'].items():
        for blue_entity in blue_entities:
            if blue_entity['name'] in target_list and blue_entity['life'] > 0:
                blue_index = blue.index(blue_entity['name'])
                blue_location_x = blue_entity['latitude']
                blue_location_y = blue_entity['longitude']

                for red_id, red_entities in obs['redSituation'].items():
                    for red_entity in red_entities:
                        if red_id == red_unit_type[4] and red_entity['life'] > 0:
                            red_index = red.index(red_entity['name'])
                            red_location_x = red_entity['latitude']
                            red_location_y = red_entity['longitude']
                            if ran > geodesic((blue_location_x, blue_location_y), (red_location_x, red_location_y)).km:
                                mask[red_index, blue_index] = 100

    return mask


# 安全距离
def rule_safe_range(ran, model):
    model.ran = ran


def get_txt_from_replan(new_task_list, is_first=False):
    task = []
    task_context = []
    task_num = []

    for i in range(red_agent_num):
        agent_task_info_list = new_task_list[i]
        agent_task = []
        agent_task_context = []
        agent_task_num = 0

        if len(agent_task_info_list) != 0:
            for agent_task_info in agent_task_info_list:
                agent_task.append(agent_task_info[0][0])
                agent_task_context.append([agent_task_info[0][2], agent_task_info[0][3], agent_task_info[0][4]])
                agent_task_num += 1
        else:
            agent_task.append(100)

        task.append(agent_task)
        task_context.append(agent_task_context)
        task_num.append(agent_task_num)

    task_now = [task[i][0] for i in range(red_agent_num)]
    task_num_now = [0 for _ in range(red_agent_num)]

    task_num_list = []
    if is_first:
        for task_single in task:
            for task_num1 in task_single:
                if task_num1 not in task_num_list and task_num1 != 100 and task_num1 != -1:
                    task_num_list.append(task_num1)

    return task, task_context, task_now, task_num, task_num_now, task_num_list


def getDistancePoint(lon: float, lat: float, distance: float, direction: float):
    """
    根据经纬度，距离，方向获得一个地点
    :param lon: 经度
    :param lat: 纬度
    :param distance: 距离（千米）
    :param direction: 方向（北：0，东：90，南：180，西：360）
    :return:
    """
    start = geopy.Point(lat, lon)
    d = geopy.distance.GeodesicDistance(kilometers=distance)
    des = d.destination(point=start, bearing=direction)

    return float(des.longitude), float(des.latitude)


def red_action_0(obs, task_now, task_context, task_num_now):
    # init at here, then add blue and red const in relative values

    # index = 0
    # for id, entities in obs['redSituation'].items():
    #     for entity in entities:
    #         if task_now[index] == 100 or task_now[index] == -1 or task_context[index][task_num_now[index]][
    #             0] != 'attack':
    #             continue
    #         if task_context[index][task_num_now[index]][1] == 'f':
    #             task_context[index][task_num_now[index]][1] = 'g'
    #         index += 1

    index = 0
    command = {
        'moveactions': [],
        'fireactions': [],
        'scoutactions': []
    }


    location_x = []
    location_y = []
    name = []
    blue_live_flag = []
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['life'] > 0:
                location_x.append(entity['longitude'])
                location_y.append(entity['latitude'])
                name.append(entity['name'])
                blue_live_flag.append(1)
            else:
                blue_live_flag.append(0)

    # -------------------------------------防空炮------------------------------------- #
    # todo: change for attacking 6 blue UAVs
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if entity['name'] in red[2:6]:
                action = {}
                action['agentname'] = entity['name']

                min_dis_id = 0
                min_dis = 1000000
                self_location_x = entity['longitude']
                self_location_y = entity['latitude']
                blue_index = 0
                for id_, entities_ in obs['blueSituation'].items():
                    for entity_ in entities_:
                        if blue[blue_index] in blueUAV:
                            # print('111')
                            entity_location_x = entity_['longitude']
                            entity_location_y = entity_['latitude']
                            dis = math.sqrt((entity_location_x-self_location_x) ** 2 + (entity_location_y-self_location_y) ** 2)  # 不规范 但能用
                            if dis < min_dis:
                                min_dis = dis
                                min_dis_id = blue_index
                        blue_index += 1
                        # print(blue_index)
                action['targetname'] = [blue[min_dis_id]]

                command['fireactions'].append(action)
                # print(action)

    #  分配红方导弹
    # attack_target_id = [100 for _ in range(red_agent_num)]
    # index = 0
    # for id, entities in obs['redSituation'].items():
    #     for entity in entities:
    #         # 获取红方每个智能体及其索引
    #         # 如果当前没有被分配任务 则跳过
    #         if task_now[index] == 100 or task_now[index] == -1:
    #             pass
    #         # 如果被分配了任务，先看是不是导弹类型
    #         elif entity['name'] in redInCMissle or entity['name'] in redArCMissle:
    #             # 如果分配的是打击火炮阵地
    #             if task_context[index][task_num_now[index]][2] == 'artillery':
    #                 # 第一遍筛选：从既定区域内筛选未被打击的蓝方
    #                 for i in range(blue_agent_num):
    #                     # 判定当前考虑的蓝方单位是否在任务预设的区域内
    #                     if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
    #                         # 如果已被锁定则跳过
    #                         if i in attack_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blueArtillery:
    #                             attack_target_id[index] = i
    #                             break
    #                 # 如果既定区域内所有目标已被锁定，则从全局开始锁定
    #                 if attack_target_id[index] == 100:
    #                     for i in range(blue_agent_num):
    #                         # 如果已被锁定则跳过
    #                         if i in attack_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blueArtillery:
    #                             attack_target_id[index] = i
    #                             break
    #
    #             elif task_context[index][task_num_now[index]][2] == 'infantry':
    #                 # 第一遍筛选：从既定区域内筛选未被打击的蓝方
    #                 for i in range(blue_agent_num):
    #                     # 判定当前考虑的蓝方单位是否在任务预设的区域内
    #                     if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
    #                         # 如果已被锁定则跳过
    #                         if i in attack_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blueInfantry:
    #                             attack_target_id[index] = i
    #                             break
    #                 # 如果既定区域内所有目标已被锁定，则从全局开始锁定
    #                 if attack_target_id[index] == 100:
    #                     for i in range(blue_agent_num):
    #                         # 如果已被锁定则跳过
    #                         if i in attack_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blueInfantry:
    #                             attack_target_id[index] = i
    #                             break
    #             elif task_context[index][task_num_now[index]][2] == 'all':
    #                 # 第一遍筛选：从既定区域内筛选未被打击的蓝方
    #                 for i in range(blue_agent_num):
    #                     # 判定当前考虑的蓝方单位是否在任务预设的区域内
    #                     if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
    #                         # 如果已被锁定则跳过
    #                         if i in attack_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blueInfantry or blue[i] in blueArtillery:
    #                             attack_target_id[index] = i
    #                             break
    #                 # 如果既定区域内所有目标已被锁定，则从全局开始锁定
    #                 if attack_target_id[index] == 100:
    #                     for i in range(blue_agent_num):
    #                         # 如果已被锁定则跳过
    #                         if i in attack_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blueInfantry or blue[i] in blueArtillery:
    #                             attack_target_id[index] = i
    #                             break
    #         index += 1

    # if obs['step'] == 20:
    #     print(attack_target_id)

    # 不如指定了算完
    attack_target_id = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 12, 100, 100, 23, 13,
                        24, 100, 18, 100, 19, 6, 100, 100, 7, 20, 8, 9, 100, 10, 21, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100]

    # 分配红方无人车 多一步判断是observe还是attack
    UAV_target_id = [100 for _ in range(red_agent_num)]
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            # 获取红方每个智能体及其索引
            # 如果当前没有被分配任务 则跳过？ 不如直接默认attack
            if task_now[index] == 100 or task_now[index] == -1 or task_context[index][task_num_now[index]][0] != 'attack':
                pass
            # 如果被分配了任务，先看是不是无人车类型
            elif entity['name'] in redSAUGV:
                # 如果分配的是打击火炮阵地
                if task_context[index][task_num_now[index]][2] == 'artillery':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == 'g':
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                UAV_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if UAV_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                UAV_target_id[index] = i
                                break

                elif task_context[index][task_num_now[index]][2] == 'infantry':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == 'g':
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                UAV_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if UAV_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                UAV_target_id[index] = i
                                break
                elif task_context[index][task_num_now[index]][2] == 'all':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == 'g':
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                UAV_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if UAV_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                UAV_target_id[index] = i
                                break
            index += 1


    # 分配红方无人机目标
    sui_target_id = [100 for _ in range(red_agent_num)]
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            # 获取红方每个智能体及其索引
            # 如果当前没有被分配任务 则跳过
            if task_now[index] == 100 or task_now[index] == -1:
                pass
            # 如果被分配了任务，先看是不是导弹类型
            elif entity['name'] in redsuicideUAV:
                # 如果分配的是打击火炮阵地
                if task_context[index][task_num_now[index]][2] == 'artillery':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break

                elif task_context[index][task_num_now[index]][2] == 'infantry':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                sui_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                sui_target_id[index] = i
                                break
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break
                elif task_context[index][task_num_now[index]][2] == 'all':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break
            index += 1

    # 准备阶段结束 开始赋指令
    for i in range(red_agent_num):
        if task_now[i] == 100 or task_now[i] == -1:
            continue
        action = {}
        action_ = {}
        action['agentname'] = red[i]
        action_['agentname'] = red[i]
        if task_context[i][task_num_now[i]][0] == 'attack':
            # -------------------------------------红方无人车------------------------------------- #
            if red[i] in redSAUGV and obs['step'] >= 20:

                target_idx = UAV_target_id[i]
                if target_idx == 100:
                    continue
                # print(target_idx)
                for id, entities in obs['blueSituation'].items():
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            entity_location_x = entity['longitude']
                            entity_location_y = entity['latitude']
                            for _, entities_ in obs['redSituation'].items():
                                for entity_ in entities_:
                                    if entity_['name'] == red[i]:
                                        self_location_x = entity_['longitude']
                                        self_location_y = entity_['latitude']

                            if self_location_x - entity_location_x > 0:
                                direction = math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180
                            else:
                                direction = 360 - math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180

                            direction = direction + (random.random() - 0.5) * 20

                            longitude, latitude = getDistancePoint(entity_location_x, entity_location_y, 9,
                                                                   direction)
                            action_['longitude'] = longitude
                            action_['latitude'] = latitude
                            action_['altitude'] = 0
                            break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)
            # -------------------------------------红方巡飞弹------------------------------------- #
            elif (red[i] in redInCMissle or red[i] in redArCMissle) and obs['step'] >= 20:
                # 解算target：在上面解算完了
                target_idx = attack_target_id[i]
                # 后期会没有那么多目标。。。
                if target_idx == 100:
                    continue

                for id, entities in obs['blueSituation'].items():
                    flag = 0
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            action_['longitude'] = entity['longitude']
                            action_['latitude'] = entity['latitude']
                            action_['altitude'] = 0
                            flag = 1
                            break
                    if flag:
                        break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)

            # -------------------------------------红方自杀无人机------------------------------------- #
            elif (red[i] in redsuicideUAV) and obs['step'] >= 30:
                target_idx = sui_target_id[i]
                if target_idx == 100:
                    continue

                for id, entities in obs['blueSituation'].items():
                    flag = 0
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            action_['longitude'] = entity['longitude']
                            action_['latitude'] = entity['latitude']
                            action_['altitude'] = 0
                            flag = 1
                            break
                    if flag:
                        break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)

        else:
            # -----------------------------anything, support or observe, random----------------------------- #

            if red[i] in redSAUGV:
                if obs['step'] >= 20:
                    target_area = task_context[i][task_num_now[i]][1]
                    action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3
                    action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3
                    action['altitude'] = 0
                    command['moveactions'].append(action)
            else:
                target_area = task_context[i][task_num_now[i]][1]
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3
                action['altitude'] = 0
                command['moveactions'].append(action)


    # 再分配自杀无人机的目标
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            # 获取红方每个智能体及其索引
            # 如果当前没有被分配任务 则再分配
            if not(task_now[index] == 100):
                pass
            # 如果被分配了任务，先看是不是导弹类型
            elif entity['name'] in redsuicideUAV:
                # 直接默认打击全部
                # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                for i in range(blue_agent_num):
                    # 判定当前考虑的蓝方单位是否在任务预设的区域内
                    # 如果已被锁定则跳过
                    if i in sui_target_id or blue_live_flag[i] == 0:
                        continue
                    if blue[i] in blueInfantry or blue[i] in blueArtillery:
                        sui_target_id[index] = i
                        break

                if sui_target_id[index] == 100:
                    for i in range(blue_agent_num):
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break
            index += 1

    # 再分配导弹的目标
    # attack_target_id = [100 for _ in range(red_agent_num)]
    # index = 0
    # for id, entities in obs['redSituation'].items():
    #     for entity in entities:
    #         # 获取红方每个智能体及其索引
    #         # 如果当前没有被分配任务 则跳过
    #         if not(task_now[index] == 100):
    #             pass
    #         # 如果被分配了任务，先看是不是导弹类型
    #         elif entity['name'] in redInCMissle or entity['name'] in redArCMissle:
    #             # 如果分配的是打击火炮阵地
    #             # 第一遍筛选：blueArtillery
    #             for i in range(blue_agent_num):
    #                 # 如果已被锁定则跳过
    #                 if i in attack_target_id or blue_live_flag[i] == 0:
    #                     continue
    #                 if blue[i] in blueArtillery:
    #                     attack_target_id[index] = i
    #                     break
    #             # 如果所有blueArtillery已被锁定，则从全局开始锁定
    #             if attack_target_id[index] == 100:
    #                 for i in range(blue_agent_num):
    #                     # 如果已被锁定则跳过
    #                     if i in attack_target_id or blue_live_flag[i] == 0:
    #                         continue
    #                     if blue[i] in blueArtillery or blue[i] in blueInfantry:
    #                         attack_target_id[index] = i
    #                         break
    #         index += 1
    # if obs['step'] == 50:
    #     print(attack_target_id)

    # attack_target_id = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 12,  100, 100, 23,  13,
    #                     24,  100, 18,  100, 19,  6,   100, 100, 7,   20,  8,   9,   100, 10,  21,  100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100]

    attack_target_id = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 18,  19,  100, 100,
                        100, 20,  100, 21,  100, 100, 22,  25,  100, 100, 100, 100, 19,   100, 100, 26,  11,  100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100]

    # 再分配无人车的目标 用最近的来算！
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if not(task_now[index] == 100):
                pass
            elif entity['name'] in redSAUGV:
                min_dis_id = 0
                min_dis = 1000000
                self_location_x = entity['longitude']
                self_location_y = entity['latitude']
                blue_index = 0
                for id_, entities_ in obs['blueSituation'].items():
                    for entity_ in entities_:
                        if blue_live_flag[blue_index] == 0 or blue_index in UAV_target_id:
                            blue_index += 1
                            continue
                        entity_location_x = entity_['longitude']
                        entity_location_y = entity_['latitude']
                        dis = math.sqrt((entity_location_x-self_location_x) ** 2 + (entity_location_y-self_location_y) ** 2)  # 不规范 但能用
                        if dis < min_dis:
                            min_dis = dis
                            min_dis_id = blue_index
                        blue_index += 1
                UAV_target_id[index] = min_dis_id

                # # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                # for i in range(blue_agent_num):
                #     # 判定当前考虑的蓝方单位是否在任务预设的区域内
                #     if blue_entity_area_mapping[i] == 'g':
                #         # 如果已被锁定则跳过
                #         if i in UAV_target_id or blue_live_flag[i] == 0:
                #             continue
                #         if blue[i] in blueInfantry or blue[i] in blueArtillery:
                #             UAV_target_id[index] = i
                #             break
                # # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                # if UAV_target_id[index] == 100:
                #     for i in range(blue_agent_num):
                #         # 如果已被锁定则跳过
                #         if i in UAV_target_id or blue_live_flag[i] == 0:
                #             continue
                #         if blue[i] in blue[0:34]:
                #             UAV_target_id[index] = i
                #             break
            index += 1

    for i in range(red_agent_num):
        if task_now[i] == 100:
            action = {}
            action_ = {}
            action['agentname'] = red[i]
            action_['agentname'] = red[i]

            # -----------------------------无人机统一去侦查----------------------------- #
            if red[i] in redRSUAV:
                target_area = 'g'
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3
                action['altitude'] = 0
                command['moveactions'].append(action)
            elif red[i] in redFSUAV[0:5]:
                target_area = 'f'
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3 + 0.65
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3 - 0.1
                action['altitude'] = 0
                command['moveactions'].append(action)
            elif red[i] in redFSUAV[5:]:
                target_area = 'd'
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3 - 0.2
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3 + 0.4
                action['altitude'] = 0
                command['moveactions'].append(action)

            # ----------------------------- 发自杀无人机打击目标 ----------------------------- #
            elif (red[i] in redsuicideUAV) and obs['step'] >= 30:
                target_idx = sui_target_id[i]
                if target_idx == 100:
                    continue

                for id, entities in obs['blueSituation'].items():
                    flag = 0
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            action_['longitude'] = entity['longitude']
                            action_['latitude'] = entity['latitude']
                            action_['altitude'] = 0
                            flag = 1
                            break
                    if flag:
                        break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)
            # ----------------------------- 发导弹打击炮兵 ----------------------------- #
            # 注意可以延时一波
            elif (red[i] in redInCMissle or red[i] in redArCMissle) and obs['step'] >= 50:
                # 解算target：在上面解算完了
                target_idx = attack_target_id[i]
                if target_idx == 100:
                    continue

                for id, entities in obs['blueSituation'].items():
                    flag = 0
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            action_['longitude'] = entity['longitude']
                            action_['latitude'] = entity['latitude']
                            action_['altitude'] = 0
                            flag = 1
                            break
                    if flag:
                        break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)
            # ----------------------------- 无人车全面进攻 ----------------------------- #
            # 先修改好前面 这里再一起复制
            if red[i] in redSAUGV and obs['step'] >= 20:
                target_idx = UAV_target_id[i]
                # print(target_idx)
                for id, entities in obs['blueSituation'].items():
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            entity_location_x = entity['longitude']
                            entity_location_y = entity['latitude']
                            for _, entities_ in obs['redSituation'].items():
                                for entity_ in entities_:
                                    if entity_['name'] == red[i]:
                                        self_location_x = entity_['longitude']
                                        self_location_y = entity_['latitude']

                            if self_location_x - entity_location_x > 0:
                                direction = math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180
                            else:
                                direction = 360 - math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180

                            direction = direction + (random.random() - 0.5) * 20

                            longitude, latitude = getDistancePoint(entity_location_x, entity_location_y, 9,
                                                                   direction)
                            action_['longitude'] = longitude
                            action_['latitude'] = latitude
                            action_['altitude'] = 0
                            break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)

    return command


# for different methods
def red_action_2(obs, task_now, task_context, task_num_now, stick='无限制'):
    if stick == '无视威胁':
        ran = 2
    elif stick == '安全距离':
        ran = 9
    else:
        ran = 7
    # init at here, then add blue and red const in relative values

    # index = 0
    # for id, entities in obs['redSituation'].items():
    #     for entity in entities:
    #         if task_now[index] == 100 or task_now[index] == -1 or task_context[index][task_num_now[index]][
    #             0] != 'attack':
    #             continue
    #         if task_context[index][task_num_now[index]][1] == 'f':
    #             task_context[index][task_num_now[index]][1] = 'g'
    #         index += 1

    index = 0
    command = {
        'moveactions': [],
        'fireactions': [],
        'scoutactions': []
    }


    location_x = []
    location_y = []
    name = []
    blue_live_flag = []
    for id, entities in obs['blueSituation'].items():
        for entity in entities:
            if entity['life'] > 0:
                location_x.append(entity['longitude'])
                location_y.append(entity['latitude'])
                name.append(entity['name'])
                blue_live_flag.append(1)
            else:
                blue_live_flag.append(0)

    # -------------------------------------防空炮------------------------------------- #
    # todo: change for attacking 6 blue UAVs
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if entity['name'] in red[2:6]:
                action = {}
                action['agentname'] = entity['name']

                min_dis_id = 0
                min_dis = 1000000
                self_location_x = entity['longitude']
                self_location_y = entity['latitude']
                blue_index = 0
                for id_, entities_ in obs['blueSituation'].items():
                    for entity_ in entities_:
                        if blue[blue_index] in blueUAV:
                            # print('111')
                            entity_location_x = entity_['longitude']
                            entity_location_y = entity_['latitude']
                            dis = math.sqrt((entity_location_x-self_location_x) ** 2 + (entity_location_y-self_location_y) ** 2)  # 不规范 但能用
                            if dis < min_dis:
                                min_dis = dis
                                min_dis_id = blue_index
                        blue_index += 1
                        # print(blue_index)
                action['targetname'] = [blue[min_dis_id]]

                command['fireactions'].append(action)
                # print(action)

    #  分配红方导弹
    attack_target_id = [100 for _ in range(red_agent_num)]
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            # 获取红方每个智能体及其索引
            # 如果当前没有被分配任务 则跳过
            if task_now[index] == 100 or task_now[index] == -1:
                pass
            # 如果被分配了任务，先看是不是导弹类型
            elif entity['name'] in redInCMissle or entity['name'] in redArCMissle:
                # 如果分配的是打击火炮阵地
                if task_context[index][task_num_now[index]][2] == 'artillery':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in attack_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                attack_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if attack_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in attack_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                attack_target_id[index] = i
                                break

                elif task_context[index][task_num_now[index]][2] == 'infantry':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in attack_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                attack_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if attack_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in attack_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                attack_target_id[index] = i
                                break
                elif task_context[index][task_num_now[index]][2] == 'all':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in attack_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                attack_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if attack_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in attack_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                attack_target_id[index] = i
                                break
            index += 1

    # if obs['step'] == 20:
    #     print(attack_target_id)

    # 不如指定了算完
    # attack_target_id = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 12, 100, 100, 23, 13,
    #                     24, 100, 18, 100, 19, 6, 100, 100, 7, 20, 8, 9, 100, 10, 21, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100]

    # 分配红方无人车 多一步判断是observe还是attack
    UAV_target_id = [100 for _ in range(red_agent_num)]
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            # 获取红方每个智能体及其索引
            # 如果当前没有被分配任务 则跳过？ 不如直接默认attack
            if task_now[index] == 100 or task_now[index] == -1 or task_context[index][task_num_now[index]][0] != 'attack':
                pass
            # 如果被分配了任务，先看是不是无人车类型
            elif entity['name'] in redSAUGV:
                # 如果分配的是打击火炮阵地
                if task_context[index][task_num_now[index]][2] == 'artillery':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                UAV_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if UAV_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                UAV_target_id[index] = i
                                break

                elif task_context[index][task_num_now[index]][2] == 'infantry':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                UAV_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if UAV_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                UAV_target_id[index] = i
                                break
                elif task_context[index][task_num_now[index]][2] == 'all':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                UAV_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if UAV_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in UAV_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                UAV_target_id[index] = i
                                break
            index += 1


    # 分配红方无人机目标
    sui_target_id = [100 for _ in range(red_agent_num)]
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            # 获取红方每个智能体及其索引
            # 如果当前没有被分配任务 则跳过
            if task_now[index] == 100 or task_now[index] == -1:
                pass
            # 如果被分配了任务，先看是不是导弹类型
            elif entity['name'] in redsuicideUAV:
                # 如果分配的是打击火炮阵地
                if task_context[index][task_num_now[index]][2] == 'artillery':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break

                elif task_context[index][task_num_now[index]][2] == 'infantry':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                sui_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry:
                                sui_target_id[index] = i
                                break
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break
                elif task_context[index][task_num_now[index]][2] == 'all':
                    # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                    for i in range(blue_agent_num):
                        # 判定当前考虑的蓝方单位是否在任务预设的区域内
                        if blue_entity_area_mapping[i] == task_context[index][task_num_now[index]][1]:
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blueInfantry or blue[i] in blueArtillery:
                                sui_target_id[index] = i
                                break
                    if sui_target_id[index] == 100:
                        for i in range(blue_agent_num):
                            # 如果已被锁定则跳过
                            if i in sui_target_id or blue_live_flag[i] == 0:
                                continue
                            if blue[i] in blue[0:34]:
                                sui_target_id[index] = i
                                break
            index += 1

    # 准备阶段结束 开始赋指令
    for i in range(red_agent_num):
        if task_now[i] == 100 or task_now[i] == -1:
            continue
        action = {}
        action_ = {}
        action['agentname'] = red[i]
        action_['agentname'] = red[i]
        if task_context[i][task_num_now[i]][0] == 'attack':
            # -------------------------------------红方无人车------------------------------------- #
            if red[i] in redSAUGV and obs['step'] >= 20:

                target_idx = UAV_target_id[i]
                if target_idx == 100:
                    continue
                # print(target_idx)
                for id, entities in obs['blueSituation'].items():
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            entity_location_x = entity['longitude']
                            entity_location_y = entity['latitude']
                            for _, entities_ in obs['redSituation'].items():
                                for entity_ in entities_:
                                    if entity_['name'] == red[i]:
                                        self_location_x = entity_['longitude']
                                        self_location_y = entity_['latitude']

                            if self_location_x - entity_location_x > 0:
                                direction = math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180
                            else:
                                direction = 360 - math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180

                            direction = direction + (random.random() - 0.5) * 20

                            longitude, latitude = getDistancePoint(entity_location_x, entity_location_y, 9,
                                                                   direction)
                            action_['longitude'] = longitude
                            action_['latitude'] = latitude
                            action_['altitude'] = 0
                            break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)
            # -------------------------------------红方巡飞弹------------------------------------- #
            elif (red[i] in redInCMissle or red[i] in redArCMissle) and obs['step'] >= 20:
                # 解算target：在上面解算完了
                target_idx = attack_target_id[i]
                # 后期会没有那么多目标。。。
                if target_idx == 100:
                    continue

                for id, entities in obs['blueSituation'].items():
                    flag = 0
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            action_['longitude'] = entity['longitude']
                            action_['latitude'] = entity['latitude']
                            action_['altitude'] = 0
                            flag = 1
                            break
                    if flag:
                        break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                if obs['step'] == 20:
                    command['moveactions'].append(action_)

            # -------------------------------------红方自杀无人机------------------------------------- #
            elif (red[i] in redsuicideUAV) and obs['step'] >= 30:
                target_idx = sui_target_id[i]
                if target_idx == 100:
                    continue

                for id, entities in obs['blueSituation'].items():
                    flag = 0
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            action_['longitude'] = entity['longitude']
                            action_['latitude'] = entity['latitude']
                            action_['altitude'] = 0
                            flag = 1
                            break
                    if flag:
                        break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)

        else:
            # -----------------------------anything, support or observe, random----------------------------- #

            if red[i] in redSAUGV:
                if obs['step'] >= 20:
                    target_area = task_context[i][task_num_now[i]][1]
                    action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3
                    action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3
                    action['altitude'] = 0
                    command['moveactions'].append(action)
            else:
                target_area = task_context[i][task_num_now[i]][1]
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3
                action['altitude'] = 0
                command['moveactions'].append(action)


    # 再分配自杀无人机的目标
    # index = 0
    # for id, entities in obs['redSituation'].items():
    #     for entity in entities:
    #         # 获取红方每个智能体及其索引
    #         # 如果当前没有被分配任务 则再分配
    #         if not(task_now[index] == 100):
    #             pass
    #         # 如果被分配了任务，先看是不是导弹类型
    #         elif entity['name'] in redsuicideUAV:
    #             # 直接默认打击全部
    #             # 第一遍筛选：从既定区域内筛选未被打击的蓝方
    #             for i in range(blue_agent_num):
    #                 # 判定当前考虑的蓝方单位是否在任务预设的区域内
    #                 # 如果已被锁定则跳过
    #                 if i in sui_target_id or blue_live_flag[i] == 0:
    #                     continue
    #                 if blue[i] in blueInfantry or blue[i] in blueArtillery:
    #                     sui_target_id[index] = i
    #                     break
    #
    #             if sui_target_id[index] == 100:
    #                 for i in range(blue_agent_num):
    #                     for i in range(blue_agent_num):
    #                         # 如果已被锁定则跳过
    #                         if i in sui_target_id or blue_live_flag[i] == 0:
    #                             continue
    #                         if blue[i] in blue[0:34]:
    #                             sui_target_id[index] = i
    #                             break
    #         index += 1

    # 再分配导弹的目标
    # attack_target_id = [100 for _ in range(red_agent_num)]
    # index = 0
    # for id, entities in obs['redSituation'].items():
    #     for entity in entities:
    #         # 获取红方每个智能体及其索引
    #         # 如果当前没有被分配任务 则跳过
    #         if not(task_now[index] == 100):
    #             pass
    #         # 如果被分配了任务，先看是不是导弹类型
    #         elif entity['name'] in redInCMissle or entity['name'] in redArCMissle:
    #             # 如果分配的是打击火炮阵地
    #             # 第一遍筛选：blueArtillery
    #             for i in range(blue_agent_num):
    #                 # 如果已被锁定则跳过
    #                 if i in attack_target_id or blue_live_flag[i] == 0:
    #                     continue
    #                 if blue[i] in blueArtillery:
    #                     attack_target_id[index] = i
    #                     break
    #             # 如果所有blueArtillery已被锁定，则从全局开始锁定
    #             if attack_target_id[index] == 100:
    #                 for i in range(blue_agent_num):
    #                     # 如果已被锁定则跳过
    #                     if i in attack_target_id or blue_live_flag[i] == 0:
    #                         continue
    #                     if blue[i] in blueArtillery or blue[i] in blueInfantry:
    #                         attack_target_id[index] = i
    #                         break
    #         index += 1
    # if obs['step'] == 50:
    #     print(attack_target_id)

    # attack_target_id = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 12,  100, 100, 23,  13,
    #                     24,  100, 18,  100, 19,  6,   100, 100, 7,   20,  8,   9,   100, 10,  21,  100, 100, 100,
    #                     100, 100, 100, 100, 100, 100, 100, 100, 100]

    attack_target_id = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 18,  19,  100, 100,
                        100, 20,  100, 21,  100, 100, 22,  25,  100, 100, 100, 100, 19,   100, 100, 26,  11,  100,
                        100, 100, 100, 100, 100, 100, 100, 100, 100]

    # 再分配无人车的目标 用最近的来算！
    index = 0
    for id, entities in obs['redSituation'].items():
        for entity in entities:
            if not(task_now[index] == 100):
                pass
            elif entity['name'] in redSAUGV:
                min_dis_id = 0
                min_dis = 1000000
                self_location_x = entity['longitude']
                self_location_y = entity['latitude']
                blue_index = 0
                for id_, entities_ in obs['blueSituation'].items():
                    for entity_ in entities_:
                        if blue_live_flag[blue_index] == 0 or blue_index in UAV_target_id:
                            blue_index += 1
                            continue
                        entity_location_x = entity_['longitude']
                        entity_location_y = entity_['latitude']
                        dis = math.sqrt((entity_location_x-self_location_x) ** 2 + (entity_location_y-self_location_y) ** 2)  # 不规范 但能用
                        if dis < min_dis:
                            min_dis = dis
                            min_dis_id = blue_index
                        blue_index += 1
                UAV_target_id[index] = min_dis_id

                # # 第一遍筛选：从既定区域内筛选未被打击的蓝方
                # for i in range(blue_agent_num):
                #     # 判定当前考虑的蓝方单位是否在任务预设的区域内
                #     if blue_entity_area_mapping[i] == 'g':
                #         # 如果已被锁定则跳过
                #         if i in UAV_target_id or blue_live_flag[i] == 0:
                #             continue
                #         if blue[i] in blueInfantry or blue[i] in blueArtillery:
                #             UAV_target_id[index] = i
                #             break
                # # 如果既定区域内所有目标已被锁定，则从全局开始锁定
                # if UAV_target_id[index] == 100:
                #     for i in range(blue_agent_num):
                #         # 如果已被锁定则跳过
                #         if i in UAV_target_id or blue_live_flag[i] == 0:
                #             continue
                #         if blue[i] in blue[0:34]:
                #             UAV_target_id[index] = i
                #             break
            index += 1

    for i in range(red_agent_num):
        if task_now[i] == 100:
            action = {}
            action_ = {}
            action['agentname'] = red[i]
            action_['agentname'] = red[i]

            # -----------------------------无人机统一去侦查----------------------------- #
            if red[i] in redRSUAV:
                target_area = 'g'
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3
                action['altitude'] = 0
                command['moveactions'].append(action)
            elif red[i] in redFSUAV[0:5]:
                target_area = 'f'
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3 + 0.65
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3 - 0.1
                action['altitude'] = 0
                command['moveactions'].append(action)
            elif red[i] in redFSUAV[5:]:
                target_area = 'd'
                action['longitude'] = location_mapping[target_area][0][0] + random.random() * 1.3 - 0.2
                action['latitude'] = location_mapping[target_area][0][1] + random.random() * 1.3 + 0.4
                action['altitude'] = 0
                command['moveactions'].append(action)

            # ----------------------------- 发自杀无人机打击目标 ----------------------------- #
            # elif (red[i] in redsuicideUAV) and obs['step'] >= 30:
            #     target_idx = sui_target_id[i]
            #     if target_idx == 100:
            #         continue
            #
            #     for id, entities in obs['blueSituation'].items():
            #         flag = 0
            #         for entity in entities:
            #             if entity['name'] == blue[target_idx]:
            #                 action_['longitude'] = entity['longitude']
            #                 action_['latitude'] = entity['latitude']
            #                 action_['altitude'] = 0
            #                 flag = 1
            #                 break
            #         if flag:
            #             break
            #     action['targetname'] = [blue[target_idx]]
            #     command['fireactions'].append(action)
            #     command['moveactions'].append(action_)
            # ----------------------------- 发导弹打击炮兵 ----------------------------- #
            # 注意可以延时一波
            # elif (red[i] in redInCMissle or red[i] in redArCMissle) and obs['step'] >= 50:
            #     # 解算target：在上面解算完了
            #     target_idx = attack_target_id[i]
            #     if target_idx == 100:
            #         continue
            #
            #     for id, entities in obs['blueSituation'].items():
            #         flag = 0
            #         for entity in entities:
            #             if entity['name'] == blue[target_idx]:
            #                 action_['longitude'] = entity['longitude']
            #                 action_['latitude'] = entity['latitude']
            #                 action_['altitude'] = 0
            #                 flag = 1
            #                 break
            #         if flag:
            #             break
            #     action['targetname'] = [blue[target_idx]]
            #     command['fireactions'].append(action)
            #     command['moveactions'].append(action_)
            # ----------------------------- 无人车全面进攻 ----------------------------- #
            # 先修改好前面 这里再一起复制
            if red[i] in redSAUGV and obs['step'] >= 20:
                target_idx = UAV_target_id[i]
                # print(target_idx)
                for id, entities in obs['blueSituation'].items():
                    for entity in entities:
                        if entity['name'] == blue[target_idx]:
                            entity_location_x = entity['longitude']
                            entity_location_y = entity['latitude']
                            for _, entities_ in obs['redSituation'].items():
                                for entity_ in entities_:
                                    if entity_['name'] == red[i]:
                                        self_location_x = entity_['longitude']
                                        self_location_y = entity_['latitude']

                            if self_location_x - entity_location_x > 0:
                                direction = math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180
                            else:
                                direction = 360 - math.acos((self_location_y - entity_location_y) / (
                                            (self_location_y - entity_location_y) ** 2 + (
                                                self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180

                            direction = direction + (random.random() - 0.5) * 20

                            longitude, latitude = getDistancePoint(entity_location_x, entity_location_y, ran,
                                                                   direction)
                            action_['longitude'] = longitude
                            action_['latitude'] = latitude
                            action_['altitude'] = 0
                            break
                action['targetname'] = [blue[target_idx]]
                command['fireactions'].append(action)
                command['moveactions'].append(action_)

    return command

