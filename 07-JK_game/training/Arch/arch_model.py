" ArchModel. "

import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import geopy
import geopy.distance

from training.Arch.entity_encoder import EntityEncoder
from training.Arch.core import Core
from training.Arch.location_head import LocationHead
from training.Arch.selected_units_head import SelectedUnitsHead
from training.Arch.action_type_head import ActionTypeHead
from training.Arch.target_unit_head import TargetUnitHead



redCommander = ['Red.RedForce_RedCommander#0', 'Red.RedForce_RedCommander#0_RedCommanderMiddle#0']
redAirArtillery = ['Red.RedForce_RedCommander#0_RedAirArtillery#0', 'Red.RedForce_RedCommander#0_RedAirArtillery#1',
                   'Red.RedForce_RedCommander#0_RedAirArtillery#2', 'Red.RedForce_RedCommander#0_RedAirArtillery#3']
redRocketGun = ['Red.RedForce_RedCommander#0_RedRocketGun#0', 'Red.RedForce_RedCommander#0_RedRocketGun#1',
                'Red.RedForce_RedCommander#0_RedRocketGun#2', 'Red.RedForce_RedCommander#0_RedRocketGun#3',
                'Red.RedForce_RedCommander#0_RedRocketGun#4']
redSAUGV = ['Red.RedForce_RedCommander#0_RedSAUGV#0', 'Red.RedForce_RedCommander#0_RedSAUGV#1',
            'Red.RedForce_RedCommander#0_RedSAUGV#2', 'Red.RedForce_RedCommander#0_RedSAUGV#3']
redRSUAVehicle = ['Red.RedForce_RedCommander#0_RedRSUAVehicle#0', 'Red.RedForce_RedCommander#0_RedRSUAVehicle#1',
                  'Red.RedForce_RedCommander#0_RedRSUAVehicle#2']
redRSUAV = ['Red.RedForce_RedCommander#0_RedRSUAVehicle#0.RedRSUAV#0', 'Red.RedForce_RedCommander#0_RedRSUAVehicle#1.RedRSUAV#0',
            'Red.RedForce_RedCommander#0_RedRSUAVehicle#2.RedRSUAV#0']
redFSUAVehicle = ['Red.RedForce_RedCommander#0_RedFSUAVehicle#0', 'Red.RedForce_RedCommander#0_RedFSUAVehicle#1',
                  'Red.RedForce_RedCommander#0_RedFSUAVehicle#2']
redFSUAV = ['Red.RedForce_RedCommander#0_RedFSUAVehicle#0.RedFSUAV#0', 'Red.RedForce_RedCommander#0_RedFSUAVehicle#1.RedFSUAV#0',
            'Red.RedForce_RedCommander#0_RedFSUAVehicle#2.RedFSUAV#0']
redArCMUGV = ['Red.RedForce_RedCommander#0_RedArCMUGV#0', 'Red.RedForce_RedCommander#0_RedArCMUGV#1']
redInCMUGV = ['Red.RedForce_RedCommander#0_RedInCMUGV#0']
redAJUGV = ['Red.RedForce_RedCommander#0_RedAJUGV#0']
redArCMissle = ['Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#0', 'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#1',
                'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#2', 'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#3',
                'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#4', 'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#5',
                'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#0', 'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#1',
                'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#2', 'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#3',
                'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#4', 'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#5']
redInCMissle = ['Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#0', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#1',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#2', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#3',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#4', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#5',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#6', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#7',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#8', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#9']


blueCommander = ['Blue.BlueForce_BlueCommander#0']
blueUAVehicle = ['Blue.BlueForce_BlueCommander#0_BlueUAVehicle#0']
blueCommandMiddle = ['Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#0', 'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#1',
                     'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#2', 'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#3']
blueInfantry = ['Blue.BlueForce_BlueCommander#0_BlueInfantry#0', 'Blue.BlueForce_BlueCommander#0_BlueInfantry#1',
                'Blue.BlueForce_BlueCommander#0_BlueInfantry#2', 'Blue.BlueForce_BlueCommander#0_BlueInfantry#3']
blueArtillery = ['Blue.BlueForce_BlueCommander#0_BlueArtillery#0', 'Blue.BlueForce_BlueCommander#0_BlueArtillery#1',
                 'Blue.BlueForce_BlueCommander#0_BlueArtillery#2']
blueArchibald = ['Blue.BlueForce_BlueCommander#0_BlueArchibald#0', 'Blue.BlueForce_BlueCommander#0_BlueArchibald#1', ]  # ????
blueADLanucher = ['Blue.BlueForce_BlueCommander#0_BlueADLanucher#0', 'Blue.BlueForce_BlueCommander#0_BlueADLanucher#1',
                  'Blue.BlueForce_BlueCommander#0_BlueADLanucher#2']
blueCommNode = ['Blue.BlueForce_BlueCommander#0_BlueCommNode#0']
blueRadar = ['Blue.BlueForce_BlueCommander#0_BlueRadar#0', 'Blue.BlueForce_BlueCommander#0_BlueRadar#1']
blueUAV = ['Blue.BlueForce_BlueCommander#0_BlueUAV#0']



class ArchModel(nn.Module):
    '''
    Inputs: state
    Outputs:
        action
    '''

    def __init__(self):
        super(ArchModel, self).__init__()
        self.entity_encoder = EntityEncoder()
        self.core = Core()
        self.action_type_head = ActionTypeHead()
        self.target_unit_head = TargetUnitHead()
        self.target_unit_head_ = TargetUnitHead()
        self.location_head = LocationHead()
        self.location_head_ = LocationHead()
        self.selected_units_head = SelectedUnitsHead()
        self.project = nn.Linear(117, 64)
        self.ran = 13

    def preprocess_entity(self, obs):
        return self.entity_encoder.preprocess(obs)

    def forward(self, obs, task_now, task_context, task_num_now, batch_size=None, sequence_length=None, hidden_state=None):

        platform_list, red_name_list, blue_name_list = self.preprocess_entity(obs)
        red_num = len(red_name_list)
        blue_num = len(blue_name_list)
        platform_list = platform_list.cuda()

        entity_embeddings, embedded_entity = self.entity_encoder(platform_list)

        lstm_output, hidden_state = self.core(embedded_entity, batch_size, sequence_length, hidden_state)
        lstm_output = lstm_output.repeat(53, 1)
        agents_index = torch.eye(53).cuda()
        lstm_output = torch.cat([lstm_output, agents_index], dim=1)
        lstm_output = self.project(lstm_output)

        location_x_logits_, location_x_probs_, location_x_id_, location_y_logits_, location_y_probs_, location_y_id_ = self.location_head_(lstm_output)
        target_unit_logits_, target_unit_probs_, target_unit_id_ = self.target_unit_head_(lstm_output, entity_embeddings, blue_num, obs, task_now, task_context, task_num_now)

        command = {
            'moveactions': [],
            'fireactions': [],
            'scoutactions': []
        }

        for i in range(red_num):
            if task_now[i] == 100 or task_now[i] == -1:
                pass
            else:
                action = {}
                action_ = {}
                action['agentname'] = red_name_list[i]
                action_['agentname'] = red_name_list[i]
                if task_context[i][task_num_now[i]][0] == 'attack':

                    if red_name_list[i] in redSAUGV:
                        for id, entities in obs['blueSituation'].items():
                            for entity in entities:
                                if entity['name'] == blue_name_list[target_unit_id_[i]]:
                                    entity_location_x = entity['longitude']
                                    entity_location_y = entity['latitude']
                                    for _, entities_ in obs['redSituation'].items():
                                        for entity_ in entities_:
                                            if entity_['name'] == red_name_list[i]:
                                                self_location_x = entity_['longitude']
                                                self_location_y = entity_['latitude']

                                    if self_location_x - entity_location_x > 0:
                                        direction = math.acos((self_location_y - entity_location_y) / ((self_location_y - entity_location_y) ** 2 + (self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180
                                    else:
                                        direction = 360 - math.acos((self_location_y - entity_location_y) / ((self_location_y - entity_location_y) ** 2 + (self_location_x - entity_location_x) ** 2) ** 0.5) / math.pi * 180

                                    direction = direction + (random.random() - 0.5) * 20

                                    longitude, latitude = getDistancePoint(entity_location_x, entity_location_y, self.ran, direction)
                                    action_['longitude'] = longitude
                                    action_['latitude'] = latitude
                                    action_['altitude'] = 0
                                    break

                                    # action_['longitude'] = entity['longitude']
                                    # action_['latitude'] = entity['latitude']
                                    # action_['altitude'] = 0
                                    # break

                        action['targetname'] = [blue_name_list[target_unit_id_[i]]]
                        command['fireactions'].append(action)
                        command['moveactions'].append(action_)
                    elif (red_name_list[i] in redInCMissle or red_name_list[i] in redArCMissle) and obs['step'] >= 13:
                        for id, entities in obs['blueSituation'].items():
                            for entity in entities:
                                if entity['name'] == blue_name_list[target_unit_id_[i]]:
                                    action_['longitude'] = entity['longitude']
                                    action_['latitude'] = entity['latitude']
                                    action_['altitude'] = 0
                                    break

                        action['targetname'] = [blue_name_list[target_unit_id_[i]]]
                        command['fireactions'].append(action)
                        command['moveactions'].append(action_)
                else:
                    if task_context[i][task_num_now[i]][1] == 'l':
                        action['longitude'] = 79 + location_x_id_[i].cpu().item() * 0.1
                        action['latitude'] = 30 + location_y_id_[i].cpu().item() * 0.08
                        action['altitude'] = 0

                        command['moveactions'].append(action)
                    elif task_context[i][task_num_now[i]][1] == 'g':
                        action['longitude'] = 79.0 + location_x_id_[i].cpu().item() * 0.08
                        action['latitude'] = 31.0 + location_y_id_[i].cpu().item() * 0.1
                        action['altitude'] = 0

                        command['moveactions'].append(action)
                    elif task_context[i][task_num_now[i]][1] == 'm':
                        action['longitude'] = 80.3 + location_x_id_[i].cpu().item() * 0.05
                        action['latitude'] = 30.0 + location_y_id_[i].cpu().item() * 0.05
                        action['altitude'] = 0

                        command['moveactions'].append(action)
        return command


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

