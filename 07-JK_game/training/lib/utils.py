" some useful lib functions "

import numpy as np
import torch
from torch.autograd import Variable
import math


def to_one_hot(y, n_dims=None):
    ''' Take integer y(tensor or variable) with n dims and convert it to 1-hot representation with n+1 dims'''
    cuda_check = y.is_cuda
    if cuda_check:
        get_cuda_device = y.get_device()

    y_tensor = y.data if isinstance(y, Variable) else y
    y_tensor = y_tensor.type(torch.LongTensor).view(-1, 1)
    n_dims = n_dims if n_dims is not None else int(torch.max(y_tensor)) + 1
    y_one_hot = torch.zeros(y_tensor.size()[0], n_dims).scatter_(1, y_tensor, 1)
    y_one_hot = y_one_hot.view(*y.shape, -1)

    if cuda_check:
        y_one_hot = y_one_hot.to(get_cuda_device)

    return Variable(y_one_hot) if isinstance(y, Variable) else y_one_hot


def action_can_apply_to_target_entity_mask(obs, id_index, id, cls):
    if cls == 0:
        if id == id_index[0][0] or id == id_index[0][2] or id == id_index[0][4]:
            for ent in obs['platforminfos']:
                if ent['ID'] == id:
                    if ent['LeftWeapon'] == 1:
                        mask_type = torch.tensor([[1, 0, 0, 0, 0]], dtype=torch.float).cuda()
                        mask_entity = torch.tensor([[0, -100, -100, -100, -100]], dtype=torch.float).cuda()
                        return mask_entity, mask_type
    else:
        if id == id_index[0][5] or id == id_index[0][7] or id == id_index[0][9]:
            for ent in obs['platforminfos']:
                if ent['ID'] == id:
                    if ent['LeftWeapon'] == 1:
                        mask_type = torch.tensor([[1, 0, 0, 0, 0]], dtype=torch.float).cuda()
                        mask_entity = torch.tensor([[0, -100, -100, -100, -100]], dtype=torch.float).cuda()
                        return mask_entity, mask_type
    mask_entity = torch.tensor([[0, 0, 0, 0, 0]], dtype=torch.float).cuda()
    for i in range(5):
        if id_index[0][i + (1 - cls) * 5] == -1:
            mask_entity[0][i] = -100
    mask_type = torch.tensor([[1, 1, 1, 1, 1]], dtype=torch.float).cuda()
    return mask_entity, mask_type


def compute_reward(pre_obs, obs):
    rewards = []
    pre_red_human_num, pre_red_uav_num, pre_red_missle_num, pre_blue_human_num, pre_blue_uav_num, pre_blue_missle_num = get_info(
        pre_obs)
    red_human_num, red_uav_num, red_missle_num, blue_human_num, blue_uav_num, blue_missle_num = get_info(obs)
    # 奖励前系数为超参数，待修改
    # reward_red = 1 * (pre_red_human_num - red_human_num) + 0.2 * (pre_red_uav_num - red_uav_num) + 0.01 * (
    #             pre_red_missle_num - red_missle_num)
    # reward_blue = 1 * (pre_blue_human_num - blue_human_num) + 0.2 * (pre_blue_uav_num - blue_uav_num) + 0.01 * (
    #             pre_blue_missle_num - blue_missle_num)
    reward_red = 30*(pre_red_human_num - red_human_num) + 6 * (pre_red_uav_num - red_uav_num)
    reward_blue = 30*(pre_blue_human_num - blue_human_num) + 6 * (pre_blue_uav_num - blue_uav_num)
    rewards.append(reward_blue - reward_red)
    rewards.append(reward_red - reward_blue)
    rewards = torch.tensor(rewards).cuda()
    return rewards


def compute_loss(rewards, values, entropys, action_probs, next_value, flag_exists):
    returns, gae = compute_returns(next_value, values, rewards)
    action_probs = torch.cat(action_probs).cuda()
    returns = torch.cat(returns).detach().cuda()
    values = torch.cat(values).cuda()
    flag = torch.cat(flag_exists).cuda()
    gae = torch.cat(gae).detach().cuda()

    advantage = (returns - values) * flag
    # print(advantage)
    critic_loss = advantage.pow(2).sum()
    actor_loss = - (action_probs * gae).sum()
    entropy_sum = torch.cat(entropys, dim=1).sum()
    # print('critic_loss:', critic_loss, '    actor_loss:', actor_loss, '    entropy_loss:', entropy_sum)
    if actor_loss > 0:
        loss = (actor_loss + critic_loss * 0.5 - entropy_sum * 0.01) / 64 * 15
    else:
        loss = (actor_loss + critic_loss * 0.5 - entropy_sum * 0.01) / 64 * 15

    # print('actor_loss:', actor_loss, '    critic_loss:', critic_loss, '    entropy:', entropy_sum)
    return loss


def compute_returns(next_value, values, rewards, gamma=0.99, lamda=0.95):
    gae = []
    returns = []
    R = next_value
    first = True
    G = torch.zeros(1, 1).cuda()
    for step in reversed(range(len(rewards))):
        R = rewards[step] + gamma * R
        returns.insert(0, R)
        if first:
            delta = rewards[step] + gamma * next_value - values[step]
            G = G * gamma * lamda + delta
            gae.insert(0, G)
            first = False
        else:
            delta = rewards[step] + gamma * values[step + 1] - values[step]
            G = G * gamma * lamda + delta
            gae.insert(0, G)
    return returns, gae

