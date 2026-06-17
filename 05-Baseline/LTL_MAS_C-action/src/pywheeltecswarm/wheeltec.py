#!/usr/bin/env python

from asyncio.proactor_events import _ProactorReadPipeTransport
import sys
import yaml
#import rospy
import numpy as np
from tf import TransformListener
from geometry_msgs.msg import TwistStamped,PoseStamped,Twist

class TimeHelper:
    """Object containing all time-related functionality.
    
    """
    def __init__(self) :
        self.rosRate = None
        self.rateHz = None

    def time(self):
        """Returns the current time in seconds."""
        return rospy.Time.now( ).to_sec( )

    def sleep(self, duration):
        """Sleeps for the provided duration in seconds."""
        rospy.sleep(duration)

    def sleepForRate(self, rateHz):
        """Sleeps so that, if called in a loop, executes at specified rate."""
        if self.rosRate is None or self.rateHz != rateHz :
            self.rosRate = rospy.Rate( rateHz )
            self.rateHz = rateHz
        self.rosRate.sleep( )

    def isShutdown(self):
        """Returns true if the script should abort, e.g. from Ctrl-C."""
        return rospy.is_shutdown()



class Wheeltec:
    """Object representing a single UGV robot.

    The bulk of the module's functionality is contained in this class.
    """
    #def __init__( self, id, initialPosition, tf):
    def __init__(self, id):
        """Constructor.

        Args:
            id (int): Integer ID.
        """
        self.id = id
        prefix = "/wheeltec" + str(id).rjust(2,'0')
        self.prefix = prefix

        rospy.init_node('wheeltec', anonymous=False)
        self.tf = TransformListener()
        self.rate = rospy.Rate(10)

        #self.cmdVelocityPublisher = rospy.Publisher(prefix + "/cmd_vel", TwistStamped, queue_size=1)
        self.cmdVelocityPublisher = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.cmdVelocityMsg = Twist()

        self.cmdgoToPublisher = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)
        #self.cmdgoToPublisher = rospy.Publisher(prefix + "/move_base_simple/goal", PoseStamped, queue_size=1)
        self.cmdgoToMsg = PoseStamped()
        self.cmdgoToMsg.header.seq = 0
        self.cmdgoToMsg.header.frame_id = "map"

        """后面补充其他功能函数
        self.cmdPositionPublisher = rospy.Publisher(prefix + "/move_base_simple/goal", PoseStamped, queue_size=1)
        self.cmdPositionMsg = PoseStamped()
        self.cmdPositionMsg.header.seq = 0
        self.cmdPositionMsg.header.frame_id = "/map"
        """

    
    def position(self):
        """Returns the last true pose measurement from motion capture.
        
        Returns:
            position(np.array[3]): current position(meters) and yaw(rad).
        """
        self.tf.waitForTransform("/world", self.prefix, rospy.Time(0), rospy.Duration(10))
        p, q = self.tf.lookupTransform("/world", self.prefix, rospy.Time(0))
        yaw = 2*np.arctan(q[2]/q[3])
        # if yaw < 0:
        #     yaw += 2*np.pi
        pose = np.float64([format(p[0], '.3f'), format(p[1], '.3f'),format(yaw, '.3f')])

        return pose


    def cmdVelocity(self, vel, yawRate):
        """Sends a streaming velocity controller setpoint command.

        Args:
            vel (array-like of float[2]): Velocity. Meters / second.
            yawRate (float): Yaw angular velocity. Degrees / second
        """
        self.cmdVelocityMsg.linear.x = vel[0]
        self.cmdVelocityMsg.linear.y = vel[1]
        self.cmdVelocityMsg.linear.z = 0.0
        self.cmdVelocityMsg.angular.x = 0.0
        self.cmdVelocityMsg.angular.y = 0.0
        self.cmdVelocityMsg.angular.z = yawRate
        self.cmdVelocityPublisher.publish(self.cmdVelocityMsg)


    def cmdPosition(self, pos, yaw=360, forward=True):
        """Sends a streaming command of absolute position and yaw setpoint.
        Moving velocity = 0.5 m/s.

        Args:
            pos (array-like of float[2]): Position. Meters.
            yaw (float): Yaw angle[-pi,pi]. Radians. 360 means any direction.
        """
        if forward:
            pose_current = self.position()
            if abs(pos[0]-pose_current[0]) < 0.01:
                if (pos[1]-pose_current[1]) > 0.01:
                    yaw_goal = np.pi
                elif (pos[1]-pose_current[1]) < 0.01:
                    yaw_goal = np.pi*3/2
                else:
                    yaw_goal = 0.0

            elif (pos[0]-pose_current[0]) > 0.01:
                if abs(pos[1]-pose_current[1]) > 0.01:
                    yaw_goal = np.arctan((pos[1]-pose_current[1])/(pos[0]-pose_current[0]))
                else:
                    yaw_goal = 0.0

            elif (pos[0]-pose_current[0]) < -0.01:
                if abs(pos[1]-pose_current[1] > 0.01):
                    yaw_goal = np.arctan((pos[1]-pose_current[1])/(pos[0]-pose_current[0])) + np.pi
                else:
                    yaw_goal = np.pi        

            print("The goal yaw is %.2frad." %yaw_goal)
            print("The start yaw is %.2frad." %pose_current[2])
            
            # Yaw controller
            while abs(yaw_goal-self.position()[2]) > 0.01:
                delta_yaw = yaw_goal-self.position()[2]
                if delta_yaw > np.pi:
                    delta_yaw = 2*np.pi - delta_yaw
                elif delta_yaw < -np.pi:
                    delta_yaw = 2*np.pi + delta_yaw
                print("Need to rotate %.2frad" %delta_yaw)
                yawRate = 0.8*delta_yaw/np.pi
                self.cmdVelocity(np.zeros(2), yawRate)
                rospy.sleep(0.5)
                
                if abs(yaw_goal-self.position()[2]) <= 0.03:
                    self.cmdVelocity(np.zeros(2), 0.0)
                    rospy.sleep(0.5)
                    break

            # Position controller
            while (pos[0]-self.position()[0])**2+(pos[1]-self.position()[1])**2 > 0.02:
                dis = np.sqrt((pos[0]-self.position()[0])**2 + (pos[1]-self.position()[1])**2)
                vel = 0.5*dis
                print("Moving at rate %.2frad" %vel)
                self.cmdVelocity([vel, 0.0], 0.0)
                rospy.sleep(0.5)

                if abs(dis) <= 0.02:
                    self.cmdVelocity(np.zeros(2), 0.0)
                    rospy.sleep(0.5)
                    break

            if yaw != 360:
                print("The final yaw is %.2frad." %yaw)
                while abs(yaw-self.position()[2]) > 0.01:
                    delta_yaw = yaw-self.position()[2]
                    if delta_yaw <= np.pi:
                        delta_yaw = 2*np.pi - delta_yaw
                    elif delta_yaw < -np.pi:
                        delta_yaw = 2*np.pi + delta_yaw
                    print("Need to rotate %.2frad" %delta_yaw)
                    yawRate = 2.0*delta_yaw/np.pi
                    self.cmdVelocity(np.zeros(2), yawRate)
                    rospy.sleep(0.5)

                if abs(yaw_goal-self.position()[2]) <= 0.01:
                    self.cmdVelocity(np.zeros(2), 0.0)
                    rospy.sleep(0.5)

            
        else:
            pass


    def stop(self):
        """Cuts power to the motors when operating in low-level command mode.

        Intended for non-emergency scenarios, e.g. landing with the possibility
        of taking off again later. Future low- or high-level commands will
        restart the motors.
        """
        print("Stopping!")
        for i in range(10):
            self.cmdVelocity(np.zeros(2), 0.0)
            self.rate.sleep()


    def goTo(self, goal, yaw, duration, relative=False):
        """Sends a streaming command of absolute position and yaw setpoint.

        Useful for slow maneuvers where a high-level planner determines the
        desired position, and the rest is left to the onboard controller.

        Args:
            pos (array-like of float[3]): Position. Meters.
            yaw (float): Yaw angle. Radians.
        """
        if relative:
            pos_current = self.position()
            pos = [(goal[0]+pos_current[0]), (goal[1]+pos_current[1])]
            #pos = np.sum([goal, self.position()[0:1]], axis=0)
        else:
            pos = goal

        self.cmdgoToMsg.header.stamp = rospy.Time.now()
        self.cmdgoToMsg.header.seq += 1
        self.cmdgoToMsg.pose.position.x = pos[0]
        self.cmdgoToMsg.pose.position.y = pos[1]
        self.cmdgoToMsg.pose.position.z = 0.00
        #self.cmdgoToMsg.pose.orientation.x = ax*np.sin(theta/2)
        #self.cmdgoToMsg.pose.orientation.y = ay*np.sin(theta/2)
        self.cmdgoToMsg.pose.orientation.z = 1*np.sin(yaw/2)        
        self.cmdgoToMsg.pose.orientation.w = np.cos(yaw/2)

        self.cmdgoToPublisher.publish(self.cmdgoToMsg)
        rospy.sleep(duration)


    def followPoints(self, waypoints, duration):
        """Follow the waypoints to reach target goal.
        
        Args:
            waypoints file.csv: x[m],y[m]
        """
        for i in range(len(waypoints)):
            pos = waypoints[i,:]
            
            if i == 0:
                pos_past = waypoints[i,:]
            else:
                pos_past = waypoints[i-1,:]

            if (pos[0]-pos_past[0]) == 0:
                yaw = 0
            else:
                yaw = np.arctan((pos[1]-pos_past[1])/(pos[0]-pos_past[0]))
            
            self.goTo(pos, yaw, duration)
            print("Moving to point: (%.2f, %.2f)" %(pos[0], pos[1]))
            
            """
            for i in range(100*duration):
                print(self.position())
                rospy.sleep(0.01)
            """
        return True