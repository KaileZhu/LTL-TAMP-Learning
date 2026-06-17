import os
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import data.input_data.map_data as mp_data
import matplotlib.patches as mpathes
import copy
import random
from src.ltl_mas.simulate.field_background import field
sys.path.append(os.path.dirname(os.path.abspath(__file__)) +
                "/../../Search_based_Planning/")

from src.ltl_mas.simulate import env


class Plotting:
    def __init__(self, agent_type,fig):
        #self.xI, self.xG = xI, xG
        self.agent_type=agent_type
        self.env = env.Env()
        self.obs = self.env.obs_map()
        self.fig=fig


    def update_obs(self, obs):
        self.obs = obs

    def animation(self, path, visited, name):
        self.plot_grid(name)
        self.plot_visited(visited)
        self.plot_path(path)
        plt.show()

    def animation_lrta(self, path, visited, name):
        self.plot_grid(name)
        cl = self.color_list_2()
        path_combine = []

        for k in range(len(path)):
            self.plot_visited(visited[k], cl[k])
            plt.pause(0.2)
            self.plot_path(path[k])
            path_combine += path[k]
            plt.pause(0.2)
        if self.xI in path_combine:
            path_combine.remove(self.xI)
        self.plot_path(path_combine)
        plt.show()

    def animation_ara_star(self, path, visited, name):
        self.plot_grid(name)
        cl_v, cl_p = self.color_list()
        for k in range(len(path)):
            self.plot_visited(visited[k], cl_v[k])
            self.plot_path(path[k], cl_p[k], True)
            plt.pause(0.5)

        plt.show()

    def plot_grid(self, name):
        obs_x = [x[0] for x in self.obs]
        obs_y = [x[1] for x in self.obs]
        plt.plot(obs_x, obs_y, "sk")
        plt.title(name)
        plt.axis("equal")

    def plot_fied_env(self):
        a=field()
        a.init_background()
        for i,k in a.back_ground.items():
            cl=a.color_for_label[i]
            [k[i][0] for i in range(len(k))]
            plt.fill([k[i][0] for i in range(len(k))],[k[i][1] for i in range(len(k))],cl)


    def plot_trajectory(self, pose_trajectory,stage_track, cl='r', flag=False):
        self.pose_trajectory=pose_trajectory
        self.stage_track=stage_track

        fig=plt.figure(tight_layout=True)
        plt.xlim(0,500)
        plt.ylim(0,300)
        #ax1 = fig.add_subplot(111, aspect='equal')
        #self.plot_grid('task executing')
        self.trajectory_list={}
        for i in range(len(pose_trajectory[0])):
            if self.agent_type[i]=="UAV":
                shape='g'
            elif self.agent_type[i]=="UGV":
                shape='b'
            self.trajectory_list[i],=plt.plot(pose_trajectory[0][i][0],pose_trajectory[0][i][1],shape)
        self.point_list={}
        for i in range(len(pose_trajectory[0])):
            if self.agent_type[i]=="UAV":
                shape='go'
            elif self.agent_type[i]=="UGV":
                shape='bs'
            self.point_list[i],=plt.plot(pose_trajectory[0][i][0],pose_trajectory[0][i][1],shape)
        #self.plot_task_label(ax)
        anim=animation.FuncAnimation(fig,self.update_points,frames=4000,interval=200,blit=False)
        plt.show()


    def plot_task_label(self,fig):
        #'<> (search_a && <> ( formation_f)) && <> (goto_c && <>search_d)'
        task=[(0,'goto','c'), (1,'search','a'), (2,'search','d'), (3,'formation','f')]
        for i in task:
            pose1=copy.deepcopy(mp_data.position[i[2]])
            name=str(i[0])+' '+i[1]
            plt.text(pose1[0]-3,pose1[1],name)
            pose1[0]=pose1[0]-3
            pose1[1]=pose1[1]-3
            rect=mpathes.Rectangle(tuple(pose1),5,5,color='y')
            #plt.Rectangle(tuple(pose),40,40,color='y')
            fig.add_patch(rect)



    def update_points(self,num):
        if num<10:
            return
        else:
            num=num-10
        for i in range(len(self.pose_trajectory[0])):
            trajectory_x=[]
            trajectory_y=[]
            for j in range(num):
                trajectory_x.append(self.pose_trajectory[j][i][0])
                trajectory_y.append(self.pose_trajectory[j][i][1])
            self.trajectory_list[i].set_data(trajectory_x,trajectory_y)
        for i in range(len(self.pose_trajectory[0])):
            if self.stage_track[num][i]=="motion":
                cl='r'
                self.point_list[i].set_data(self.pose_trajectory[num][i][0],self.pose_trajectory[num][i][1])
                self.point_list[i].set_color(cl)
            if self.stage_track[num][i]=="action":
                cl='b'
                if num%3==0 :
                    self.point_list[i].set_data(self.pose_trajectory[num][i][0]+random.randint(-3,3)/1.3,self.pose_trajectory[num][i][1]+random.randint(-3,3)/1.3)
                    self.point_list[i].set_color(cl)
            if self.stage_track[num][i]=="stay":
                cl='g'
                self.point_list[i].set_data(self.pose_trajectory[num][i][0],self.pose_trajectory[num][i][1])
                self.point_list[i].set_color(cl)


    def plot_path(self, path, cl='r', flag=False):
        path_x = [path[i][0] for i in range(len(path))]
        path_y = [path[i][1] for i in range(len(path))]

        if not flag:
            plt.plot(path_x, path_y, linewidth='3', color='r')
        else:
            plt.plot(path_x, path_y, linewidth='3', color=cl)

        plt.plot(self.xI[0], self.xI[1], "bs")
        plt.plot(self.xG[0], self.xG[1], "gs")

        plt.pause(0.01)

    def plot_visited_bi(self, v_fore, v_back):
        if self.xI in v_fore:
            v_fore.remove(self.xI)

        if self.xG in v_back:
            v_back.remove(self.xG)

        len_fore, len_back = len(v_fore), len(v_back)

        for k in range(max(len_fore, len_back)):
            if k < len_fore:
                plt.plot(v_fore[k][0], v_fore[k][1], linewidth='3', color='gray', marker='o')
            if k < len_back:
                plt.plot(v_back[k][0], v_back[k][1], linewidth='3', color='cornflowerblue', marker='o')

            plt.gcf().canvas.mpl_connect('key_release_event',
                                         lambda event: [exit(0) if event.key == 'escape' else None])

            if k % 10 == 0:
                plt.pause(0.001)
        plt.pause(0.01)

    @staticmethod
    def color_list():
        cl_v = ['silver',
                'wheat',
                'lightskyblue',
                'royalblue',
                'slategray']
        cl_p = ['gray',
                'orange',
                'deepskyblue',
                'red',
                'm']
        return cl_v, cl_p

    @staticmethod
    def color_list_2():
        cl = ['silver',
              'steelblue',
              'dimgray',
              'cornflowerblue',
              'dodgerblue',
              'royalblue',
              'plum',
              'mediumslateblue',
              'mediumpurple',
              'blueviolet',
              ]
        return cl