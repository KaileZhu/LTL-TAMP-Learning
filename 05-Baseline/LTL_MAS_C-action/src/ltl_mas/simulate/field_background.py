import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
from matplotlib.patches import Ellipse, Circle
from src.ltl_mas.simulate.astar import AStar
import matplotlib.animation as animation
from src.ltl_mas.tools.nx_plot.bezier_method import smoothing_base_bezier

class field:
    '''
    this class provide the graph of map
    the cost time of action relatied to the map
    the cost between the map point
    '''
    def __init__(self):
        self.init_background()



    def init_background(self):
        self.back_ground={}
        self.back_ground["d1"]=[[0.0,300.0],[200.0,300.0],[137.0,208.0]]
        self.back_ground["d2"]=[[0.0,290.0],[0.0,0.0],[134.0,201.0]]
        self.back_ground["d3"]=[[10.0,0.0],[150.0,0.0],[237.0,131.0],[140.0,196.0]]
        self.back_ground["d4"]=[[160.0,0.0],[300.0,0.0],[341.0,62.0],[244.0,127.0]]
        self.back_ground["d5"]=[[310.0,0.0],[435.0,0.0],[348.0,57.0]]
        self.back_ground["d6"]=[[450.0,0.0],[500.0,0.0],[500.0,285.0],[353.0,64.0]]
        self.back_ground["d7"]=[[360.0,300],[249.0,134.0],[346.0,69.0],[500.0,300.0]]
        self.back_ground["d8"]=[[210.0,300.0],[145.0,203.0],[242.0,138.0],[350.0,300.0]]
        place_list=['d1','d2','d3','d4','d5','d6','d7','d8']
        self.color_for_label={'road':'y'}
        for place in place_list:
            self.color_for_label[place]='aquamarine'
        self.photovoltaic_list={'p1':[133,270],'p2':[100,256],'p3':[76,214],'p4':[58,189],'p5':[46,161],
                                'p6': [39, 130],'p7':[31,99],'p8':[78,32],'p9':[110,47],'p10':[127,71],
                                'p11': [146, 96],'p12':[162,120],'p13':[180,145],'p14':[204,186],'p15':[220,211],
                                'p16': [239, 235],'p17':[256,260],'p18':[417,261],'p19':[395,239],'p20':[378,215],
                                'p21': [360, 191],'p22':[343,166],'p23':[326,142],'p24':[308,117],'p25':[283,75],
                                'p26': [266, 51],'p27':[239,33],'p28':[201,22],'p29':[412,48],'p30':[430,72],
                                'p31': [446, 97],'p32':[454,128],'p33':[467,156],'p34':[474,187]
                                }
        self.station_list={"t1":[17,65],"t2":[42,18],"t3":[225,13],
                           "t4":[477,218],"t5":[459,266],"t6":[306,260],
                           "t7":[172,284]   }
        self.base_list={"b1":[358,15]}
        self.panels_wides_lenth_list={
            'p1':5,'p2':8,'p3':8,'p4':8,'p5':7,'p6':5,'p7':3,'p8':5,'p9':8,'p10':8,'p11':8,'p12':8,
            'p13':8,'p14':8,'p15':8,'p16':8,'p17':8,'p18':7,'p19':8,'p20':8,'p21':8,'p22':8,'p23':8,
            'p24':8,'p25':8,'p26':8,'p27':6,'p28':2,'p29':8,'p30':8,'p31':8,'p32':6,'p33':5,'p34':3
        }
        self.generate_panel()
        self.get_node_in_area_of_station()
        self.set_the_input_msg_for_task_assignment()
        self.get_node_in_barrier()

    def generate_panel(self):
        '''
        get the node in the panels
        '''
        self.panels_area_list={}
        self.panels_block_list={}
        self.node_set_for_panel={}
        self.node_set_for_panel2={}
        self.boundry_node_list_for_panel={}
        for panel,width in self.panels_wides_lenth_list.items():
            center=self.photovoltaic_list[panel]
            sin=0.56
            cos=0.83
            edges_list_up=[]
            edges_list_down=[]
            for i in range(width+1):
                node1=[center[0]+i*12*cos+12*sin-width*6*cos,center[1]-i*12*sin+12*cos+width*6*sin]
                node2=[center[0]+i*12*cos-12*sin-width*6*cos,center[1]-i*12*sin-12*cos+width*6*sin]
                edges_list_up.append(node1)
                edges_list_down.append(node2)
            self.panels_block_list[panel]=(edges_list_up,edges_list_down)
            boundry_node_list=[edges_list_up[0],edges_list_up[-1],edges_list_down[-1],edges_list_down[0]]
            self.boundry_node_list_for_panel[panel]=boundry_node_list
            area=width*12*12*2
            self.panels_area_list[panel]=area
            area1=self.get_area(boundry_node_list)
            if np.abs(area-area1)>50:
                new=1
            radius=width*6*cos+6*sin
            radius2=width*6*sin+6*cos
            #consider the accurate
            self.node_set_for_panel[panel]=[]
            self.node_set_for_panel2[panel] = []
            for i in range(int((center[0]-radius)//5*5),int((center[0]+radius)//5*5+5),5):
                for j in range(int((center[1]-radius2)//5*5),int((center[1]+radius2)//5*5+5),5 ):
                    if self.if_node_in_area((i,j),boundry_node_list,area):
                        self.node_set_for_panel[panel].append((i,j))
            for i in range(int((center[0]-radius)//2*2),int((center[0]+radius)//2*2+2),2):
                for j in range(int((center[1]-radius2)//2*2),int((center[1]+radius2)//2*2+2),2 ):
                    if self.if_node_in_area((i,j),boundry_node_list,area):
                        self.node_set_for_panel2[panel].append((i,j))
            if self.node_set_for_panel[panel]==[]:
                a=1

    def get_node_in_area_of_station(self):
        self.node_set_for_station={}
        for station,center in self.station_list.items():
            r=8
            self.node_set_for_station[station]=[]
            for i in range(int((center[0]-r)//2*2+2),int((center[0]+r)//2*2-2),2):
                l=(r**2-(i-center[0])**2)**0.5//1+1
                #print(l)
                #print(int((center[1]-l)//2*2),int((center[1]+l)//2*2))
                for j in range(int((center[1]-l)//2*2),int((center[1]+l)//2*2),2):
                    self.node_set_for_station[station].append((i,j))
        self.node_set_for_area=self.node_set_for_station.copy()
        self.node_set_for_area.update(self.node_set_for_panel)
        self.node_set_for_panel2.update(self.node_set_for_station)

    def get_node_in_barrier(self):
        self.node_set_for_barrier=[]
        for station,center in self.station_list.items():
            r=10
            for i in range(int((center[0]-r)//5*5+5),int((center[0]+r)//5*5),5):
                l=(r**2-(i-center[0])**2)**0.5//5+5
                #print(l)
                #print(int((center[1]-l)//2*2),int((center[1]+l)//2*2))
                for j in range(int((center[1]-l)//5*5),int((center[1]+l)//5*5+5),5):
                    self.node_set_for_barrier.append((i,j))
        sin = 0.56
        cos = 0.83
        for panel,width in self.panels_wides_lenth_list.items():
            center = self.photovoltaic_list[panel]
            area = width * 12 * 12 * 2
            radius = width * 6 * cos + 6 * sin
            radius2 = width * 6 * sin + 6 * cos

            for i in range(int((center[0]-radius)//5*5-5),int((center[0]+radius)//5*5+10),5):
                for j in range(int((center[1]-radius2)//5*5-5),int((center[1]+radius2)//5*5+10),5 ):
                    if self.if_node_next_to_area((i,j),self.boundry_node_list_for_panel[panel],area):
                        self.node_set_for_barrier.append((i,j))


    def plot_one_area(self,name):
        for node in self.node_set_for_area[name]:
            plt.plot(node[0],node[1],'o')
        plt.show()

    def plot_back_ground(self,agent_type,pose_trajectory,stage_track,num,type='with_word'):
        self.agent_type=agent_type
        self.pose_trajectory=pose_trajectory
        self.stage_track=stage_track
        fig=plt.figure(tight_layout=True,figsize=(20,10))
        ax=fig.add_subplot(111,aspect='equal')
        plt.fill([0,500,500,0],[0,0,300,300],'palegoldenrod')
        for i,k in self.back_ground.items():
            cl=self.color_for_label[i]
            plt.fill([k[i][0] for i in range(len(k))],[k[i][1] for i in range(len(k))],cl)
        for name,area in self.panels_block_list.items():
            x_list=[area[0][0][0],area[0][-1][0],area[1][-1][0],area[1][0][0]]
            y_list = [area[0][0][1], area[0][-1][1], area[1][-1][1], area[1][0][1]]
            plt.fill(x_list,y_list,'#448ee4')
            center=self.photovoltaic_list[name]
            x_list.append(area[0][0][0])
            y_list.append(area[0][0][1])
            plt.plot(x_list,y_list,'black')
            plt.plot([0.5*area[0][0][0]+0.5*area[1][0][0],0.5*area[0][-1][0]+0.5*area[1][-1][0]],
                      [0.5*area[0][0][1]+0.5*area[1][0][1],0.5*area[0][-1][1]+0.5*area[1][-1][1]],
                      'dimgrey')
            for i in range(len(area[0])):
                plt.plot([area[0][i][0],area[1][i][0]],[area[0][i][1],area[1][i][1]],'dimgrey')
            if type=='with_word':
                plt.text(center[0]-6,center[1]-3,name)
        #plot the station and base
        for station,center in self.station_list.items():
            cir=plt.Circle((center[0],center[1]),6,color='black')
            plt.text(center[0]+7,center[1],station)
            ax.add_artist(cir)
        for name,center in self.base_list.items():
            rec=plt.Rectangle((center[0]-28,center[1]-15),56,30,color='y')
            rec1=plt.Rectangle((center[0]-28,center[1]-15),56,30,color='black',fill=None)
            plt.text(center[0]-5,center[1]-3,station)
            ax.add_artist(rec)
            ax.add_artist(rec1)

        #fig=plt.figure(tight_layout=True)
        plt.xlim(0,500)
        plt.ylim(0,300)
        self.state_label_list={}
        for i in range(len(pose_trajectory[0])):
            if self.agent_type[i]=="UAV":
                shape='g'
            elif self.agent_type[i]=="UGV":
                shape='g'
            self.state_label_list[i]=plt.text(self.pose_trajectory[0][i][0],self.pose_trajectory[0][i][1],self.agent_type[i],fontsize=16)
        self.trajectory_list={}
        for i in range(len(pose_trajectory[0])):
            if self.agent_type[i]=="UAV":
                shape='g'
                self.trajectory_list[i],=plt.plot(pose_trajectory[0][i][0],pose_trajectory[0][i][1],shape)
            elif "UGV" in self.agent_type[i]:
                shape='g'
                self.trajectory_list[i],=plt.plot(pose_trajectory[0][i][0],pose_trajectory[0][i][1],shape)

        self.point_list={}
        self.point_edge_list={}
        for i in range(len(pose_trajectory[0])):
            if self.agent_type[i]=="UAV":
                shape='go'
                l=2
                agent_shape_x=[pose_trajectory[0][i][0]+n for n in [-l,l,-l,l,0]]
                agent_shape_y=[pose_trajectory[0][i][1]+n for n in [-l,-l,l,l,0]]
                agent_edge_x=[pose_trajectory[0][i][0]+n for n in [-l,l,0,-l,l]]
                agent_edge_y=[pose_trajectory[0][i][1]+n for n in [-l,l,0,l,-l]]
                self.point_edge_list[i],=plt.plot(agent_edge_x,agent_edge_y,'black',linewidth=3)
                self.point_list[i],=plt.plot(agent_shape_x,agent_shape_y,shape)
            elif self.agent_type[i]=="UGV_s":
                #shape='bs'
                #agent_shape_x=[pose_trajectory[0][i][0]+n for n in [-4,4,-4,4,0]]
                #agent_shape_y=[pose_trajectory[0][i][1]+n for n in [-4,-4,4,4,0]]
                self.point_list[i]=plt.Polygon([[pose_trajectory[0][i][0]-2,pose_trajectory[0][i][1]-3],
                                                      [pose_trajectory[0][i][0]+2,pose_trajectory[0][i][1]-3],
                                                      [pose_trajectory[0][i][0]+2,pose_trajectory[0][i][1]+3],
                                                      [pose_trajectory[0][i][0]+0,pose_trajectory[0][i][1]+5],
                                                      [pose_trajectory[0][i][0]-2,pose_trajectory[0][i][1]+3]],
                                                     color='g',alpha=1)
                #ax.add_patch(patch)
                ax.add_patch(self.point_list[i])
                #agent_edge_x=[pose_trajectory[0][i][0]+n for n in [-4,4,0,-4,4]]
                #agent_edge_y=[pose_trajectory[0][i][1]+n for n in [-4,4,0,4,-4]]
            elif self.agent_type[i]=="UGV_l":
                #shape='bs'
                l=2
                #agent_shape_x=[pose_trajectory[0][i][0]+n for n in [-l,l,-l,l,0]]
                #agent_shape_y=[pose_trajectory[0][i][1]+n for n in [-l,-l,l,l,0]]
                self.point_list[i]=plt.Polygon([[pose_trajectory[0][i][0]-3,pose_trajectory[0][i][1]-4],
                                                      [pose_trajectory[0][i][0]+3,pose_trajectory[0][i][1]-4],
                                                      [pose_trajectory[0][i][0]+3,pose_trajectory[0][i][1]+4],
                                                      [pose_trajectory[0][i][0]+0,pose_trajectory[0][i][1]+6],
                                                      [pose_trajectory[0][i][0]-3,pose_trajectory[0][i][1]+4]],
                                                     color='g',alpha=1)
                ax.add_patch(self.point_list[i])
                #self.point_list[i],=plt.plot(agent_shape_x,agent_shape_y,shape)
                #agent_edge_x=[pose_trajectory[0][i][0]+n for n in [-l,l,0,-l,l]]
                #agent_edge_y=[pose_trajectory[0][i][1]+n for n in [-l,l,0,l,-l]]
            #self.point_list[i],=plt.plot(agent_shape_x,agent_shape_y,shape)
        #self.plot_task_label(ax)
        anim=animation.FuncAnimation(fig,self.update_points,frames=num,interval=200,blit=False)
        #anim.save("test.gif")
        plt.show()

    def plot_back_ground_with_time(self,agent_type,pose_trajectory,stage_track,time,color_table,pre_name,type='with_word'):
        self.agent_type=agent_type
        self.pose_trajectory=pose_trajectory
        self.stage_track=stage_track
        fig=plt.figure(tight_layout=True,figsize=(20,10))
        ax=fig.add_subplot(111,aspect='equal')
        plt.fill([0,500,500,0],[0,0,300,300],'palegoldenrod')
        for i,k in self.back_ground.items():
            cl=self.color_for_label[i]
            plt.fill([k[i][0] for i in range(len(k))],[k[i][1] for i in range(len(k))],cl)
        for name,area in self.panels_block_list.items():
            x_list=[area[0][0][0],area[0][-1][0],area[1][-1][0],area[1][0][0]]
            y_list = [area[0][0][1], area[0][-1][1], area[1][-1][1], area[1][0][1]]
            plt.fill(x_list,y_list,'#448ee4')
            center=self.photovoltaic_list[name]
            x_list.append(area[0][0][0])
            y_list.append(area[0][0][1])
            plt.plot(x_list,y_list,'black')
            plt.plot([0.5*area[0][0][0]+0.5*area[1][0][0],0.5*area[0][-1][0]+0.5*area[1][-1][0]],
                      [0.5*area[0][0][1]+0.5*area[1][0][1],0.5*area[0][-1][1]+0.5*area[1][-1][1]],
                      'dimgrey')
            for i in range(len(area[0])):
                plt.plot([area[0][i][0],area[1][i][0]],[area[0][i][1],area[1][i][1]],'dimgrey')
            if type=='with_word':
                plt.text(center[0]-12,center[1]-6,name,fontsize=35)
        #plt.text(6,6,'t='+str(time)+'s',fontsize=60)
        #plot the station and base
        for station,center in self.station_list.items():
            cir=plt.Circle((center[0],center[1]),7,color='black')
            plt.text(center[0]+7,center[1],station,fontsize=35)
            ax.add_artist(cir)
        for name,center in self.base_list.items():
            x_list=[center[0]-28,center[0]-28,center[0]+28,center[0]+28]
            y_list=[center[1]-15,center[1]+15,center[1]+15,center[1]-15]
            plt.fill(x_list,y_list,'y')
            plt.plot(x_list,y_list,'black')
            #rec=plt.Rectangle((center[0]-28,center[1]-15),56,30,color='y')
            #rec1=plt.Rectangle((center[0]-28,center[1]-15),56,30,color='black',fill=None)
            #plt.text(center[0]-5,center[1]-3,station)
            #ax.add_artist(rec)
            #ax.add_artist(rec1)
        plt.xlim(0,500)
        plt.ylim(0,300)
        self.state_label_list={}
        subtime=0
        self.trajectory_list={}
        color_varide=['Greys','Purples','Blues','Greens','Oranges','Reds','YlOrBr','YlOrRd','OrRd','PuRd','RdPu','GnBu']
        for i in range(len(pose_trajectory[0])):
            cl=color_table[i]
            trajectory_x=[]
            trajectory_y=[]
            for j in range(subtime,time):
                trajectory_x.append(self.pose_trajectory[j][i][0])
                trajectory_y.append(self.pose_trajectory[j][i][1])
            #shape='g'
            #self.trajectory_list[i],=plt.plot(trajectory_x,trajectory_y,shape)
            if self.agent_type[i]=='UAV':
                category_colors=plt.get_cmap(color_varide[0])(np.linspace(0.6,1,(time-subtime)))
            elif self.agent_type[i]=='UGV_s':
                category_colors=plt.get_cmap(color_varide[3])(np.linspace(0.6,1,(time-subtime)))
            elif self.agent_type[i]=='UGV_l':
                category_colors=plt.get_cmap(color_varide[5])(np.linspace(0.4,0.8,(time-subtime)))
            #category_colors=plt.get_cmap(color_varide[i])(np.linspace(0.5,1,(time-subtime)))
            if 'UAV' in agent_type[i]:
                path_x=trajectory_x[0:time-subtime:5]
                path_y=trajectory_y[0:time-subtime:5]
            else:
                path_x=trajectory_x[0:time-subtime:10]
                path_y=trajectory_y[0:time-subtime:10]
            #x_curve, y_curve=smoothing_base_bezier(path_x,path_y)
            if len(path_x)==0:
                path_x=[trajectory_x[-1] for i in range(10)]
                path_y=[trajectory_y[-1] for i in range(10)]
            path_x,path_y=smoothing_base_bezier(path_x,path_y)
            step=(len(path_x)-1)//len(category_colors)+1
            if i >5:
                step=step*2
            for j in range(0,len(path_x)-step,step):
                #if (path_x[j+step]-path_x[j],path_y[j+step]-path_y[j]) == (0.0,0.0):
                    plt.arrow(path_x[j], path_y[j], path_x[j + 1] - path_x[j], path_y[j + 1] - path_y[j],
                               head_width=3, lw=9, color=category_colors[j // step])
                #else:
                    #plt.arrow(path_x[j],path_y[j],path_x[j+1]-path_x[j],path_y[j+1]-path_y[j],
                    #      length_includes_head=True,head_width=3,lw=9,color=category_colors[j//step])

        legend_name=[]
        cout_dic={'UAV':0,'UGV_l':0,'UGV_s':0}
        arrow_list=[]
        i=0
        for agent in agent_type:
            cout_dic[agent]=cout_dic[agent]+1
            legend_name.append(agent+' '+str(cout_dic[agent]))
            #arrow_list.append(plt.arrow(0,0,-3,-3,length_includes_head=True,head_width=2,lw=4,color=color_table[i]))
            i=i+1
        #plt.legend(arrow_list,legend_name)
        self.point_list={}
        self.point_edge_list={}
        for i in range(len(pose_trajectory[0])):
            if self.stage_track[time][i]=="motion":
                cl='orange'
            if self.stage_track[time][i]=="stay":
                cl='y'
            if self.stage_track[time][i]=="error":
                cl='black'
            else:
                cl='r'
            if self.agent_type[i]=="UAV":

                l=4
                agent_shape_x=[pose_trajectory[time][i][0]+n for n in [-l,l,-l,l]]
                agent_shape_y=[pose_trajectory[time][i][1]+n for n in [-l,-l,l,l]]
                agent_edge_x=[pose_trajectory[time][i][0]+n for n in [-l,l,0,-l,l]]
                agent_edge_y=[pose_trajectory[time][i][1]+n for n in [-l,l,0,l,-l]]
                self.point_edge_list[i]=plt.plot(agent_edge_x,agent_edge_y,'black',linewidth=3)
                #print(agent_shape_x)
                #print(agent_shape_y)
                print(cl+'o')
                if cl=='black':
                    self.point_list[i]=plt.plot(agent_shape_x,agent_shape_y,'k'+'o',markersize=10,zorder=5)
                else:
                    self.point_list[i]=plt.plot(agent_shape_x,agent_shape_y,cl+'o',markersize=8,zorder=3)
            elif self.agent_type[i]=="UGV_s":
                if self.pose_trajectory[time][i]==self.pose_trajectory[time+1][i]:
                    cos=1
                    sin=0
                else:
                    dis_x=self.pose_trajectory[time+1][i][0]-self.pose_trajectory[time][i][0]
                    dis_y=self.pose_trajectory[time+1][i][1]-self.pose_trajectory[time][i][1]
                    cos=dis_x/(dis_x**2+dis_y**2)**0.5
                    sin=dis_y/(dis_x**2+dis_y**2)**0.5
                #print(cos,sin)
                shape_list=[[n*cos-m*sin,n*sin+m*cos] for n,m in [(-5,-4),(5,-4),(7,0),(5,4),(-5,4)]]
                agent_shape=[[self.pose_trajectory[time][i][0]+n,self.pose_trajectory[time][i][1]+m]
                             for n,m in shape_list]
                cl='g'
                self.point_list[i]=plt.Polygon(agent_shape,color=cl,alpha=1,zorder=2)
                po=plt.Polygon(agent_shape,color='black',alpha=1,fill=None,zorder=3)
                ax.add_patch(self.point_list[i])
                ax.add_patch(po)
            elif self.agent_type[i]=="UGV_l":
                if self.pose_trajectory[time][i]==self.pose_trajectory[time+1][i]:
                    cos=1
                    sin=0
                else:
                    dis_x=self.pose_trajectory[time+1][i][0]-self.pose_trajectory[time][i][0]
                    dis_y=self.pose_trajectory[time+1][i][1]-self.pose_trajectory[time][i][1]
                    cos=dis_x/(dis_x**2+dis_y**2)**0.5
                    sin=dis_y/(dis_x**2+dis_y**2)**0.5
                shape_list=[[n*cos-m*sin,n*sin+m*cos]   for n,m in [(-6,-5),(6,-5),(8,0),(6,5),(-6,5)]]
                if i == 8:

                    agent_shape=[[self.pose_trajectory[time][i][0]+n+5,self.pose_trajectory[time][i][1]+m+5]
                             for n,m in shape_list]
                else:
                    agent_shape = [[self.pose_trajectory[time][i][0] + n, self.pose_trajectory[time][i][1] + m]
                                   for n, m in shape_list]
                self.point_list[i]=plt.Polygon(agent_shape,color=cl,alpha=1,zorder=2)
                po=plt.Polygon(agent_shape,color='black',alpha=1,fill=None,zorder=3)
                ax.add_patch(self.point_list[i])
                ax.add_patch(po)
        plt.show()
        s=1
        #plt.savefig('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/'+pre_name+str(time)+'.eps')

    def update_points(self,num):
        #if num<10:
        #    return
        #else:
        #print(num)
        #num=num*3
        if num > 50:
            sub_num = num - 50
        else:
            sub_num = 0
        sub_num=0
        for i in range(len(self.pose_trajectory[0])):
            trajectory_x=[]
            trajectory_y=[]
            for j in range(sub_num,num):
                trajectory_x.append(self.pose_trajectory[j][i][0])
                trajectory_y.append(self.pose_trajectory[j][i][1])
            self.trajectory_list[i].set_data(trajectory_x,trajectory_y)
            self.trajectory_list[i].set_color('green')

        for i in range(len(self.pose_trajectory[0])):
            self.state_label_list[i].set_text(self.stage_track[num][i])
            self.state_label_list[i].set_position((self.pose_trajectory[num][i][0],self.pose_trajectory[num][i][1]))

        for i in range(len(self.pose_trajectory[0])):
            #print('i',i,'num',num)
            if self.agent_type[i]=='UAV':
                self.point_list[i].set_marker("o")
                l=2
                agent_shape_x=[self.pose_trajectory[num][i][0]+n for n in [-3,3,-3,3]]
                agent_shape_y=[self.pose_trajectory[num][i][1]+n for n in [-3,-3,3,3]]
                agent_edge_x=[self.pose_trajectory[num][i][0]+n for n in [-l,l,0,-l,l]]
                agent_edge_y=[self.pose_trajectory[num][i][1]+n for n in [-l,l,0,l,-l]]
                self.point_edge_list[i].set_data(agent_edge_x,agent_edge_y)
                self.point_edge_list[i].set_color('black')
                self.point_list[i].set_data(agent_shape_x,agent_shape_y)
            if self.agent_type[i] == 'UGV_l':
                #self.point_list[i].set_marker("s")

                if self.pose_trajectory[num][i]==self.pose_trajectory[num+1][i]:
                    cos=1
                    sin=0
                else:
                    dis_x=self.pose_trajectory[num+1][i][0]-self.pose_trajectory[num][i][0]
                    dis_y=self.pose_trajectory[num+1][i][1]-self.pose_trajectory[num][i][1]
                    cos=dis_x/(dis_x**2+dis_y**2)**0.5
                    sin=dis_y/(dis_x**2+dis_y**2)**0.5
                                                            #(-3,-2),(3,-2),(5,0),(3,2),(-3,2)]
                shape_list=[[n*cos-m*sin,n*sin+m*cos]   for n,m in [(-4,-3),(4,-3),(6,0),(4,3),(-4,3)]]
                agent_shape=[[self.pose_trajectory[num][i][0]+n,self.pose_trajectory[num][i][1]+m]
                             for n,m in shape_list]
                agent_shape_x=[self.pose_trajectory[num][i][0]+n for n in [-2,2,2,0,-2]]
                agent_shape_y=[self.pose_trajectory[num][i][1]+n for n in [-3,-3,3,5,3]]
                self.point_list[i].set_xy(agent_shape)
                #self.point_list[i].set_xy(agent_shape_x,agent_shape_y)
                #agent_edge_x=[self.pose_trajectory[num][i][0]]
                #agent_edge_y=[self.pose_trajectory[num][i][1]]
            if self.agent_type[i] == 'UGV_s':
                #self.point_list[i].set_marker("s")
                if self.pose_trajectory[num][i][0]==self.pose_trajectory[num+1][i][0] or self.pose_trajectory[num+1][i][1]==self.pose_trajectory[num][i][1]:
                    cos=1
                    sin=0
                else:
                    dis_x=self.pose_trajectory[num+1][i][0]-self.pose_trajectory[num][i][0]
                    dis_y=self.pose_trajectory[num+1][i][1]-self.pose_trajectory[num][i][1]
                    cos=dis_x/(dis_x**2+dis_y**2)**0.5
                    sin=dis_y/(dis_x**2+dis_y**2)**0.5
                #print(cos,sin)
                shape_list=[[n*cos-m*sin,n*sin+m*cos] for n,m in [(-3,-2),(3,-2),(5,0),(3,2),(-3,2)]]
                agent_shape=[[self.pose_trajectory[num][i][0]+n,self.pose_trajectory[num][i][1]+m]
                             for n,m in shape_list]

                #agent_shape_x=[self.pose_trajectory[num][i][0]]
                #agent_shape_y=[self.pose_trajectory[num][i][1]]
                self.point_list[i].set_xy(agent_shape)
                #agent_edge_x=[self.pose_trajectory[num][i][0]]
                #agent_edge_y=[self.pose_trajectory[num][i][1]]
            #self.point_list[i].set_data(self.pose_trajectory[num][i][0],self.pose_trajectory[num][i][1])
            #self.point_list[i].set_data(agent_shape_x,agent_shape_y)
            #self.point_edge_list[i].set_data(agent_edge_x,agent_edge_y)
            #self.point_edge_list[i].set_color('black')
            #self.agent_type
            if self.stage_track[num][i]=="motion":
                cl='orange'
                self.point_list[i].set_color(cl)
            if self.stage_track[num][i]=="stay":
                cl='y'
                self.point_list[i].set_color(cl)
            if self.stage_track[num][i]=="error":
                cl='black'
                self.point_list[i].set_color(cl)
            else:
                cl='r'
                self.point_list[i].set_color(cl)
        return  self.point_list[8]

    def co_task_planning(self,task,place):
        if "temp" in task:#temp the temperature
            if 't' in place:
                return self.plan_the_temp_with_t(place)
            return  self.plan_the_uav_path_for_search(1,place)
        if 'scan' in task:# photo the panels
            return self.plan_the_scan_action(place)
        if "wash" in task:# wash the panels
            return  self.plan_the_wash_action(place)
        if "sweep" in task:# sweep the ground
            return self.plan_the_uav_path_for_search(1,place)
            #return self.plan_the_uav_path_for_search(2,place)
        if "mow" in task:# weed the glass
            return self.plan_the_uav_path_for_search(1,place)
        if "fix" in task: # fix the station
            return  self.plan_the_fix_action(place)
        if 'repair' in task: #repair one point of the panels
            return  self.plan_the_repair_action(place)
        print('not recieve current task type')

    def plan_the_temp_with_t(self,place):
        path=[[self.station_list[place] for i in range(10)]]
        return path

    def plan_the_scan_action(self,place):
        if 't' in place:
            center = self.station_list[place]
            r = 20
            real_path = [[center[0] + r * np.sin(np.pi * i / 180), center[1] + r * np.cos(np.pi * i / 180)] for i in
                           range(0, 360, 10)]
            a1=[8.6,5]
            a2=[-8.6,5]
            a3=[0,-10]
            new_path_list=[[ (node[0]+a1[0],node[1]+a1[1]) for node in real_path],
                        [ (node[0]+a2[0],node[1]+a2[1]) for node in real_path],
            [ (node[0]+a3[0],node[1]+a3[1]) for node in real_path]]
            return new_path_list
        path_init=self.plan_the_uav_path_for_search(1,place)
        a1=[8.6,5]
        a2=[-8.6,5]
        a3=[0,-10]
        new_path_list=[[ (node[0]+a1[0],node[1]+a1[1]) for node in path_init[0]],
                        [ (node[0]+a2[0],node[1]+a2[1]) for node in path_init[0]],
        [ (node[0]+a3[0],node[1]+a3[1]) for node in path_init[0]]]
        new_path=[
             [path[i] for i in range(0,len(path),2)] for path in new_path_list
        ]
        return new_path

    def plan_the_wash_action(self,place):
        node_set=self.node_set_for_panel2[place]
        node_set.sort()
        i=node_set[0][0]
        j=node_set[-1][0]
        new_node_set=[[] for n in range(i,j+2,2)]
        for node in node_set:
            #if (node[0]-i)//2<1:
                new_node_set[(node[0]-i)//2].append(node)
        UAV_path=[]
        UGV_l_path=[]
        for node_list in new_node_set:
            UAV_path.extend([node_list[0] for i in range(len(node_list))])
            UGV_l_path.extend([node_list[-1] for i in range(len(node_list))])
        # path1=[]
        # path1.extend(UAV_path)
        # path1.extend(UAV_path)
        # path1.extend(UAV_path)
        # path1.extend(UAV_path)
        # path1.extend(UAV_path)
        # path1.extend(UAV_path)
        # path2=[]
        # path2.extend(UGV_l_path)
        # path2.extend(UGV_l_path)
        # path2.extend(UGV_l_path)
        # path2.extend(UGV_l_path)
        # path2.extend(UGV_l_path)
        # path2.extend(UGV_l_path)
        final_path_list={'wash':[UAV_path, UGV_l_path] }
        return final_path_list

    def plan_the_fix_action(self,place):
        center=self.station_list[place]
        #center=self.total_node_pose[place]
        r=15
        path_UGV_l=[[center[0]+r*np.sin(np.pi*i/180),center[1]+r*np.cos(np.pi*i/180)] for i in range(0,360,5)]
        path_UGV_s=[[center[0]+r*np.sin(np.pi*i/180),center[1]+r*np.cos(np.pi*i/180)] for i in range(120,480,5)]
        return {'fix':[path_UGV_s,path_UGV_l]}

    def plan_the_repair_action(self,place):

        upline,lowline=self.panels_block_list[place]
        begin_node=upline[0]
        end_node=upline[-1]
        len=((begin_node[0]-end_node[0])**2+(begin_node[1]-end_node[1])**2)**0.5
        time=(len*6)//1
        path=range(0,int(time))
        UGV_s_path=[]
        UGV_s_path.append([[upline[0][0]*i/time+upline[-1][0]*(1-i/time),upline[0][1]*i/time+upline[-1][1]*(1-i/time)] for i in path])
        UGV_s_path.append([[lowline[0][0]*i/time+lowline[-1][0]*(1-i/time),lowline[0][1]*i/time+lowline[-1][1]*(1-i/time)] for i in path])
        UGV_l_path=[]
        center0=[upline[0][0]/2+lowline[0][0]/2,upline[0][1]/2+lowline[0][1]/2]
        center1=[upline[-1][0]/2+lowline[-1][0]/2,upline[-1][1]/2+lowline[-1][1]/2]
        UGV_l_path.append([[center0[0]*i/time+center1[0]*(1-i/time),center0[1]*i/time+center1[1]*(1-i/time)] for i in path])
        final_path_list={'repair_UGV_l':UGV_l_path,'repair_UGV_s':UGV_s_path}
        return final_path_list

    def plan_the_uav_path_for_search(self,agent_number,name):

        node_set=self.node_set_for_panel2[name]
        node_set.sort()
        i=node_set[0][0]
        j=node_set[-1][0]
        new_node_set=[[] for n in range(i,j+2,2)]
        for node in node_set:
            new_node_set[(node[0]-i)//2].append(node)
        new_node_set1=[new_node_set[i] for i in range(0,len(new_node_set),3)]
        for l in range(len(new_node_set1)):
            if l%2==0:
                new_node_set1[l]=new_node_set1[l][::-1]
        final_list=[]
        for new_list in new_node_set1:
            final_list.extend(new_list)
        begin_num=len(final_list)//agent_number
        path_list=[]
        for i in range(0,len(final_list),begin_num):
            path_list.append([final_list[j+i] for j in range(begin_num)])
        return  path_list

    def plan_the_uav_path_for_chase(self,place,time=40):
        #remain to decision
        node_set=self.node_set_for_area[place]
        center_node=np.average(node_set,0)//1
        direction_set=[[0,1],[0,-1],[1,0],[-1,0]]
        lenth=[]
        for direction in direction_set:
            for i in range(30):
                if not self.if_node_in_area(node_set+direction*i,self.back_ground[place],self.area_list[place]):
                    lenth.append(i)
                    break
        if not len(lenth)==4:
            s=1
        node_list=[]
        for n in range(4):
            round_n=time//lenth[n]
            node_list.append([])
            for i in range(round_n):
                if i//2==0:
                    node_list.extend([center_node+direction_set[n]*l for l in range(lenth[n])])
                else:
                    node_list.extend([center_node+direction_set[n]*(lenth[n]-l) for l in range(lenth[n])])
            left_n=time%lenth[n]
            if round_n//2==0:
                node_list.extend([center_node+direction_set[n]*l for l in range(left_n)])
            else:
                node_list.extend([center_node+direction_set[n]*(left_n-l) for l in range(left_n)])
        return node_list


    def if_node_in_area(self,node,duobianx,area):
        duobianx2=[duobianx[-1],*duobianx[:-1]]
        s=0
        for i in range(len(duobianx)):
            node1=duobianx[i]
            node2=duobianx2[i]
            s=s+self.get_area([node,node1,node2])
        if s<=area+30:
            return 1
        else :
            return 0

    def if_node_next_to_area(self,node,duobianx,area):
        duobianx2=[duobianx[-1],*duobianx[:-1]]
        s=0
        for i in range(len(duobianx)):
            node1=duobianx[i]
            node2=duobianx2[i]
            s=s+self.get_area([node,node1,node2])
        if s<=area+30:
            return 1
        else :
            return 0

    def get_area(self,node_list):
        S=0
        for i in range(len(node_list)-2):
            x1=node_list[0]
            x2=node_list[i+1]
            x3=node_list[i+2]
            S=S+np.abs((x2[0]-x1[0])*(x3[1]-x1[1])-(x2[1]-x1[1])*(x3[0]-x1[0]))/2
        return S

    def labels_of_place(self,place):
        return self.labels_for_place[place]

    def set_the_input_msg_for_task_assignment(self):
        """
        put out the msg BNB and local search need
        cost time from place to another place
        time
        cost time for action(with place)
        actionname+id+_+subtask
        """
        interested_map_list=list(self.panels_area_list.keys())
        agent_execution_rate_with_area={'temp':10,'scan':20,'wash':10,'sweep':10,'mow':5,'repair':5}
        co_action_data={'temp': {'temp':1},
                        'scan': {'scan':3} ,
                        'wash': {'wash':2},
                        'sweep':{'sweep':1} ,
                        'mow':{'mow':1},
                        'fix':{'fix':2} ,
                        'repair':{'repair_UGV_l':1,'repair_UGV_s':2},
                        'monitor':{'monitor_UAV':2,'monitor_UGV_l':1}
                        }
        task_type={}
        #define the action about panels (related to the area size)
        #generate the time of task execution
        action_list_1=['temp','scan','wash','sweep','mow','repair']
        station_action=['mow','fix','scan','temp']
        execute_time_list={}
        for action in action_list_1:
            act=self.co_task_planning(action,'p2')
            #print(action)
            if isinstance(act,dict):
                for i,j in act.items():
                    1
                execute_time_list[action]=len(j[0])
            else:
                execute_time_list[action]=len(act[0])
        station_execute_time_list={}
        for action in station_action:
            act=self.co_task_planning(action,'t2')
            #print(action)
            if isinstance(act,dict):
                for i,j in act.items():
                    1
                station_execute_time_list[action]=len(j[0])
            else:
                print(action)
                print(len(act[0]))
                a=len(act[0])
                station_execute_time_list[action]=len(act[0])
        for interested_area in interested_map_list:
            for task, mage in agent_execution_rate_with_area.items():
                new_label=task+interested_area

                #self.panels_area_list[interested_area]/agent_execution_rate_with_area[task]//1
                task_type[new_label]=(execute_time_list[task],
                                          co_action_data[task])
        for interested_area in self.station_list.keys():
            for task in station_action:
                #task='fix'
                new_label=task+interested_area
                #self.panels_area_list[interested_area]/agent_execution_rate_with_area[task]//1
                task_type[new_label]=(station_execute_time_list[task],
                                          co_action_data[task])
        #task_type['back']=(1,{'back':1})
        #define the time not related the area size
        #task_not_relate_with_area={'fix':(60, {'fix':1}),'monitor':(30,{'monitor_UAV':2,'monitor_UGV_l':1})}
        #task_type['fix']=(60, {'fix':1})
        #task_type['monitor']=(30,{'monitor_UAV':2,'monitor_UGV_l':1})
        #position should be tree kind that the UAV UGVs UGVl here we just put the most simplified one
        self.total_node_pose=self.photovoltaic_list.copy()
        self.total_node_pose.update(self.station_list)
        self.total_node_pose.update(self.base_list)
        #position={}
        #for place1,pos1 in self.total_node_pose.items():
        #    for place2,pos2 in self.total_node_pose.items():
        #        if (place2,place1) not in position.keys():
        #            dis=self.get_map_relations((pos1[0]//2*2,pos1[1]//2*2),(pos2[0]//2*2,pos2[1]//2*2),set())
                    #print('dis=',dis)
        #            position[(place1,place2)]=dis//1
        #            position[(place2,place1)]=dis//1

        agent_type={'UAV':{'serve':['temp','scan','wash','back'],'velocity':10.0},
            'UGV_l':{'serve':['wash','repair_UGV_l','back','fix'],'velocity':2.0},
                   'UGV_s':{'serve':['sweep','mow','repair_UGV_s','back','fix'],'velocity':4.0} }
        agent_data_s1=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UGV_l'),
                    (5,'b1','UGV_l'),
                    (6,'b1','UGV_s'),
                    (7,'b1','UGV_s')
                    ]
        agent_data_s02=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4, 'b1', 'UAV'),
                    (5, 'b1', 'UAV'),
                    (6, 'b1', 'UAV'),
                    (7, 'b1', 'UAV'),
                    (8,'b1','UGV_l'),
                    (9,'b1','UGV_l'),
                    (10, 'b1', 'UGV_l'),
                    (11, 'b1', 'UGV_l'),
                    (12,'b1','UGV_s'),
                    (13,'b1','UGV_s'),
                    (14, 'b1', 'UGV_s'),
                    (15, 'b1', 'UGV_s')
                    ]

        agent_data_s03 = [(i,'b1','UAV') for i in range(12)]
        agent_data_s03.extend([(i,'b1','UGV_l') for i in range(12,18)])
        agent_data_s03.extend([(i, 'b1', 'UGV_s') for i in range(18, 24)])
        agent_data_s04 = [(i, 'b1', 'UAV') for i in range(16)]
        agent_data_s04.extend([(i, 'b1', 'UGV_l') for i in range(16, 24)])
        agent_data_s04.extend([(i, 'b1', 'UGV_s') for i in range(24, 32)])
        agent_data_s05 = [(i, 'b1', 'UAV') for i in range(20)]
        agent_data_s05.extend([(i, 'b1', 'UGV_l') for i in range(20, 30)])
        agent_data_s05.extend([(i, 'b1', 'UGV_s') for i in range(30, 40)])

        agent_data_s2=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UAV'),
                    (5, 'b1', 'UAV'),

                    (6,'b1','UGV_l'),
                    (7,'b1','UGV_l'),
                    (8,'b1','UGV_l'),

                    (9,'b1','UGV_s'),
                    (10,'b1','UGV_s'),
                    (11,'b1','UGV_s'),
                       ]
        agent_data_s3=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UAV'),
                    (5,'b1','UAV'),
                    (6,'b1','UAV'),
                    (7,'b1','UAV'),
                    (8,'b1','UAV'),
                    (9,'b1','UAV'),

                    (10,'b1','UGV_l'),
                    (11,'b1','UGV_l'),
                    (12,'b1','UGV_l'),
                    (13,'b1','UGV_l'),
                    (14,'b1','UGV_l'),

                    (15,'b1','UGV_s'),
                    (16,'b1','UGV_s'),
                    (17,'b1','UGV_s'),
                    (18,'b1','UGV_s'),
                    (19,'b1','UGV_s'),
                       ]
        sub_task_type=['temp','scan','wash_UAV','wash_UGV_l','repair_UGV_l','fix_UGV_l','sweep','mow','repair_UGV_s','fix_UGV_s']
        position_2={}
        position_2.update(self.photovoltaic_list)
        position_2.update(self.station_list)
        position_2.update(self.base_list)
        agent_data=agent_data_s2
        self.input_data=input_data(position_2,task_type,sub_task_type,agent_data,agent_type)

    def choose_agent_number(self,num):
        agent_swam_num=[]
        uav_num=4
        ugv_l_num=2
        ugv_s_num=2
        for i in range(1,6):
            agent_data=[]
            z=0
            for j in range(uav_num*i):
                agent_data.append((z,'b1','UAV'))
                z=z+1
            for j in range(ugv_l_num*i):
                agent_data.append((z,'b1','UGV_l'))
                z=z+1
            for j in range(ugv_s_num*i):
                agent_data.append((z,'b1','UGV_s'))
                z=z+1
            agent_swam_num.append(agent_data)
        self.input_data.agent_data=agent_swam_num[num]

    def get_center_node_of_place(self,place):
        poly=self.total_node_pose[place]
        return poly

    def get_map_relations(self,start,goal,barrier):
        '''
        due to the large size of map, we give a distance between center
        '''
        field_new_env=photovoltaic_Env(5)
        field_new_env.add_barrier(barrier)
        start1=(start[0]//5*5,start[1]//5*5)
        goal1=(goal[0]//5*5,goal[1]//5*5)
        path_finder=AStar(start1, goal1,'he',field_new_env)
        path,_=path_finder.searching()
        dis=0
        for node_i in range(len(path)-1):
            node1=path[node_i]
            node2=path[node_i+1]
            dis=dis+((node1[0]-node2[0])**2+(node1[1]-node2[1])**2)**0.5
        return dis

class photovoltaic_Env:
    def __init__(self,accuracy):
        self.x_range = 500  # size of background
        self.y_range = 300
        self.motions = [(-accuracy, 0), (-accuracy, accuracy), (0, accuracy), (accuracy,accuracy),
                        (accuracy, 0), (accuracy, -accuracy), (0, -accuracy), (-accuracy, -accuracy)]
        self.obs = self.obs_map()

    def update_obs(self, obs):
        self.obs = obs

    def obs_map(self):
        """
        Initialize obstacles' positions
        :return: map of obstacles
        assume that the UAV can go anywhere
        """
        obs = set()
        return obs

    def add_barrier(self,barrer):
        for node in barrer:
            self.obs.add(tuple(node))

class input_data:
    def __init__(self,position,task_type,sub_task_type,agent_data,agent_type):
        self.position=position
        self.task_type=task_type
        self.sub_task_type=sub_task_type
        self.agent_data=agent_data
        self.agent_type=agent_type
