#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *
def test_cmdFullState_accvel(cf0,cf1,cf2,cf3):
    K=np.array([[-0.2236,-0.6762,0,0],[0,0,-0.4472,-0.9510]])
    P=np.array([[0.1512,0.2236,0,0],[0.2236,0.6762,0,0],[0,0,0.4253,0.4472],[0,0,0.4472,0.9510]]) 
    B=np.array([[0,0],[1,0],[0,0],[0,1]])
    gain=np.dot(np.transpose(B),P)

    pos0 = cf0.position()
    vel0 = np.zeros(3)
    acc0 = np.zeros(3)
    yaw0 = 0
    omega0 = np.zeros(3)

    
#   pos1 = np.array([0.8,-5.0,1.0])
    pos1 = cf1.position()
    vel1 = np.zeros(3)
    acc1 = np.zeros(3)
    yaw1 = 0
    omega1 = np.zeros(3)


#    pos2 = np.array([1.0,3.0,1.0])
    pos2 = cf2.position()
    vel2 = np.zeros(3)  
    acc2 = np.zeros(3)
    yaw2 = 0
    omega2 = np.zeros(3)
    vel0_pre = np.zeros(3)
    vel1_pre = np.zeros(3)
    vel2_pre = np.zeros(3)
    vel3_pre = np.zeros(3)

    cf0_pre=cf0.position()
    cf1_pre=cf1.position()
    cf2_pre=cf2.position()
    cf3_pre=cf3.position()

    for i in range(5000):  
        cf0_pos = cf0.position()
        cf0_vel = vel0_pre       
        cf1_pos = cf1.position()
        cf1_vel = vel1_pre
        cf2_pos = cf2.position()
        cf2_vel = vel2_pre
        cf3_pos = cf3.position()
        cf3_vel = vel3_pre

        if i%10 == 0.0:
            vel0_pre = (cf0_pos-cf0_pre)/0.1
            cf0_pre = cf0_pos

            vel1_pre = (cf1_pos-cf1_pre)/0.1
            cf1_pre = cf1_pos

            vel2_pre = (cf2_pos-cf2_pre)/0.1
            cf2_pre = cf2_pos

            vel3_pre = (cf3_pos-cf3_pre)/0.1
            cf3_pre = cf3_pos


        kesei_0x = (cf0_pos[0]-1-cf3_pos[0])
        kesei_0vx = (cf0_vel[0]-cf3_vel[0])
        kesei_0y = (cf0_pos[1]-cf3_pos[1])
        kesei_0vy = (cf0_vel[1]-cf3_vel[1])
        kesei0 = np.array([[kesei_0x],[kesei_0vx],[kesei_0y],[kesei_0vy]])

        kesei_1x = (cf1_pos[0]+2-cf0_pos[0])
        kesei_1vx = (cf1_vel[0]-cf0_vel[0])
        kesei_1y = (cf1_pos[1]-1-cf0_pos[1])
        kesei_1vy = (cf1_vel[1]-cf0_vel[1])
        kesei1 = np.array([[kesei_1x],[kesei_1vx],[kesei_1y],[kesei_1vy]]) 

        kesei_2x = (cf2_pos[0]+2-cf0_pos[0])
        kesei_2vx = (cf2_vel[0]-cf0_vel[0])
        kesei_2y = (cf2_pos[1]+1-cf0_pos[1])
        kesei_2vy = (cf2_vel[1]-cf0_vel[1])
        kesei2 = np.array([[kesei_2x],[kesei_2vx],[kesei_2y],[kesei_2vy]])
               
       

        p0 = np.dot(np.dot(np.transpose(kesei0),P),kesei0)
        p0 = p0[0][0]
        BPkesei = 0.3*np.dot(np.dot(np.transpose(B),P),kesei0)
        f0 = -0.3*BPkesei/np.linalg.norm(BPkesei)
        u0 = p0*np.dot(K,kesei0)+f0
        acc0[0]=u0[0][0]
        acc0[1]=u0[1][0]


        vel0[0] = vel0[0] + acc0[0]*(0.01)    
        pos0[0] = pos0[0] + vel0[0]*(0.01)        
        vel0[1] = vel0[1] + acc0[1]*(0.01)
        pos0[1] = pos0[1] + vel0[1]*(0.01)
        pos0[2] = 1.0
        
        p1 = np.dot(np.dot(np.transpose(kesei1),P),kesei1)
        p1 = p1[0][0]
        BPkesei = 0.3*np.dot(np.dot(np.transpose(B),P),kesei1)
        f1 = -0.3*BPkesei/np.linalg.norm(BPkesei)
        u1 = p1*np.dot(K,kesei1)+f1
        acc1[0]=u1[0][0]
        acc1[1]=u1[1][0]



        vel1[0] = vel1[0] + acc1[0]*(0.01)    
        pos1[0] = pos1[0] + vel1[0]*(0.01)        
        vel1[1] = vel1[1] + acc1[1]*(0.01)
        pos1[1] = pos1[1] + vel1[1]*(0.01)
        pos1[2] = 1.0




        p2 = np.dot(np.dot(np.transpose(kesei2),P),kesei2)
        p2 = p2[0][0]
        BPkesei = 0.3*np.dot(np.dot(np.transpose(B),P),kesei2)
        f2 = -0.3*BPkesei/np.linalg.norm(BPkesei)
        u2 = p2*np.dot(K,kesei2)+f2
        acc2[0]=u2[0][0]
        acc2[1]=u2[1][0]


        vel2[0] = vel2[0] + acc2[0]*(0.01)    
        pos2[0] = pos2[0] + vel2[0]*(0.01)        
        vel2[1] = vel2[1] + acc2[1]*(0.01)
        pos2[1] = pos2[1] + vel2[1]*(0.01)
        pos2[2] = 1.0



        
        cf0.cmdFullState(pos0, vel0, acc0, yaw0, omega0)
        cf1.cmdFullState(pos1, vel1, acc1, yaw1, omega1)
        cf2.cmdFullState(pos2, vel2, acc2, yaw2, omega2)
        timeHelper.sleep(0.01)

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf0 = swarm.allcfs.crazyflies[0]
    cf1 = swarm.allcfs.crazyflies[1]
    cf2 = swarm.allcfs.crazyflies[2]
    cf3 = swarm.allcfs.crazyflies[3]
  
    Z = 1.0

    cf0.takeoff(targetHeight=Z, duration=Z+1.0)

    cf1.takeoff(targetHeight=Z, duration=Z+1.0)

    cf2.takeoff(targetHeight=Z, duration=Z+1.0) 

    cf3.takeoff(targetHeight=Z, duration=Z+1.0)   
    timeHelper.sleep(Z+2.0)


    cf0.goTo(np.array([1.0,0,1.0]),0,10.0)
    cf1.goTo(np.array([0.5,0,1.0]),0,10.0)
    cf2.goTo(np.array([0,0,1.0]),0,5.0)
    cf3.goTo(np.array([-0.5,0,1.0]),0,5.0)
    timeHelper.sleep(10.0)

    test_cmdFullState_accvel(cf0,cf1,cf2,cf3)

    cf0.notifySetpointsStop()
    cf1.notifySetpointsStop()
    cf2.notifySetpointsStop()
    cf3.notifySetpointsStop()

    cf0.land(targetHeight=0.03, duration=Z+1.0)
    cf1.land(targetHeight=0.03, duration=Z+1.0)
    cf2.land(targetHeight=0.03, duration=Z+1.0)
    cf3.land(targetHeight=0.03, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)
