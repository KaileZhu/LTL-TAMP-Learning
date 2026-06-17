###############################################################################

# Required Libraries
import copy
import matplotlib.pyplot as plt
import numpy as np

###############################################################################

# Function: Rank 
def ranking(flow):    
    rank_xy = np.zeros((flow.shape[0], 2))
    for i in range(0, rank_xy.shape[0]):
        rank_xy[i, 0] = 0
        rank_xy[i, 1] = flow.shape[0]-i           
    for i in range(0, rank_xy.shape[0]):
        plt.text(rank_xy[i, 0],  rank_xy[i, 1], 'a' + str(int(flow[i,0])), size = 12, ha = 'center', va = 'center', bbox = dict(boxstyle = 'round', ec = (0.0, 0.0, 0.0), fc = (0.8, 1.0, 0.8),))
    for i in range(0, rank_xy.shape[0]-1):
        plt.arrow(rank_xy[i, 0], rank_xy[i, 1], rank_xy[i+1, 0] - rank_xy[i, 0], rank_xy[i+1, 1] - rank_xy[i, 1], head_width = 0.01, head_length = 0.2, overhang = 0.0, color = 'black', linewidth = 0.9, length_includes_head = True)
    axes = plt.gca()
    axes.set_xlim([-1, +1])
    ymin = np.amin(rank_xy[:,1])
    ymax = np.amax(rank_xy[:,1])
    if (ymin < ymax):
        axes.set_ylim([ymin, ymax])
    else:
        axes.set_ylim([ymin-1, ymax+1])
    plt.axis('off')
    plt.show() 
    return

def change_list(dataset):
    All_list =[]
    for newlist in dataset:
        nochange =newlist[:2]
        new_tuple_list =[]
        for num in range(len(newlist[0])):
            if newlist[2][num]>=newlist[3][num]:
                new_tuple_list.append(newlist[2][num])
            else:
                new_tuple_list.append(newlist[3][num])

        new_tuple_list =tuple(new_tuple_list)
        nochange.append(new_tuple_list)
        All_list.append(nochange)
    return All_list

def data_pre_treat_meat(dataset):
    #获取将数组变成向量
    out_put_dataset=[]
    for i in range(len(dataset['time_cost'])):
        current_data=[]
        v_1=dataset['time_cost'][i]
        current_data.append((v_1,v_1,v_1))
        v_2=dataset['agent_needed'][i]
        current_data.append((v_2,v_2,v_2))
        v_3=dataset['task_comtribution'][i]
        current_data.append((v_3,v_3,v_3))
        v_4=dataset['task_risk'][i]
        current_data.append((v_4,v_4,v_4))
        out_put_dataset.append(current_data)


    return out_put_dataset


# Function: Fuzzy TOPSIS
def fuzzy_topsis_method(dataset, weights, criterion_type, graph = True):
    dataset=data_pre_treat_meat(dataset)
    dataset=change_list(dataset)
    r_ij      = copy.deepcopy(dataset)
    v_ij      = copy.deepcopy(dataset)
    p_ideal_A = copy.deepcopy(weights)
    n_ideal_A = copy.deepcopy(weights)
    dist_p    = np.zeros( (len(dataset), len(dataset[0])) )
    dist_n    = np.zeros( (len(dataset), len(dataset[0])) )
    for j in range(0, len(dataset[0])):
        c_star  = -float('inf')
        a_minus =  float('inf')
        for i in range(0, len(dataset)):
            a, b, c = dataset[i][j]
            if (c >= c_star and criterion_type[j] == 'max'):
                c_star = c
            if (a <= a_minus and criterion_type[j] == 'min'):
                a_minus = a
        if (criterion_type[j] == 'max'):
            for i in range(0, len(r_ij)):
                a, b, c    = r_ij[i][j]
                r_ij[i][j] = (a/c_star, b/c_star, c/c_star)
        else:
            for i in range(0, len(r_ij)):
                a, b, c    = r_ij[i][j]
                r_ij[i][j] = (a_minus/c, a_minus/b, a_minus/a)
        for i in range(0, len(r_ij)):
             a, b, c    = r_ij[i][j]
             d, e, f    = weights[0][j]
             v_ij[i][j] = (a*d, b*e, c*f)
        d, e, f = v_ij[0][j]
        x, y, z = v_ij[0][j]
        for i in range(0, len(v_ij)):
            a, b, c = v_ij[i][j]
            if (a > d):
                d = a
            if (b > e):
                e = b 
            if (c > f):
                f = c  
            if (a < x):
                x = a
            if (b < y):
                y = b 
            if (c < z):
                z = c  
        p_ideal_A[0][j] = (d, e, f) 
        n_ideal_A[0][j] = (x, y, z)
    for i in range(0, dist_p.shape[0]): 
        for j in range(0, dist_p.shape[1]):             
            a, b, c = v_ij[i][j]
            x, y, z = p_ideal_A[0][j]
            d, e, f = n_ideal_A[0][j]
            dist_p[i][j] = ( (1/dist_p.shape[1])* ( (a-x)**2 + (b-y)**2 + (c-z)**2 ) )**(1/2)
            dist_n[i][j] = ( (1/dist_n.shape[1])* ( (a-d)**2 + (b-e)**2 + (c-f)**2 ) )**(1/2)        
    d_plus  = np.sum(dist_p, axis = 1)
    d_minus = np.sum(dist_n, axis = 1) 
    c_i     = d_minus / (d_minus + d_plus)
    flow = np.copy(c_i)
    flow = np.reshape(flow, (c_i.shape[0], 1))
    flow = np.insert(flow, 0, list(range(1, c_i.shape[0]+1)), axis = 1)
    flow = flow[np.argsort(flow[:, 1])]
    flow = flow[::-1]
    return flow

###############################################################################