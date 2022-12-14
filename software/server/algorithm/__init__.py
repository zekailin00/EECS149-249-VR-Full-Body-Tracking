import threading
import logging
import time

import numpy as np

import algorithm.input_struct as din
import algorithm.output_struct as dout
# import input_struct as din
# import output_struct as dout

from threading import Thread, Lock
import threading

mutex = Lock()
count = 0

algo_begin = False
calibration = 0
halfchestwidth = 1
spinelength = 1
armlength = 1
necklength = 1

# data buffer
BUFFER_SIZE=10
imu1_acc_buff, imu2_acc_buff, imu3_acc_buff, imu4_acc_buff, imu5_acc_buff, imu6_acc_buff, imu7_acc_buff, imu8_acc_buff, imu9_acc_buff, imu10_acc_buff = [],[],[],[],[],[],[],[],[],[]
imu1_gyro_buff, imu2_gyro_buff, imu3_gyro_buff, imu4_gyro_buff, imu5_gyro_buff, imu6_gyro_buff, imu7_gyro_buff, imu8_gyro_buff, imu9_gyro_buff, imu10_gyro_buff = [],[],[],[],[],[],[],[],[],[]
imu1_acc_prev, imu2_acc_prev, imu3_acc_prev, imu4_acc_prev, imu5_acc_prev, imu6_acc_prev, imu7_acc_prev, imu8_acc_prev, imu9_acc_prev, imu10_acc_prev = [np.zeros(3) for i in range(10)]
imu1_gyro_prev, imu2_gyro_prev, imu3_gyro_prev, imu4_gyro_prev, imu5_gyro_prev, imu6_gyro_prev, imu7_gyro_prev, imu8_gyro_prev, imu9_gyro_prev, imu10_gyro_prev = [np.zeros(3) for i in range(10)]

def VR_data_in(head_rot, head_pos, left_hand_rot, left_hand_pos, right_hand_rot, right_hand_pos):
    mutex.acquire()
    din.head_rot = head_rot
    din.head_pos = head_pos

    din.left_hand_rot = left_hand_rot
    din.left_hand_pos = left_hand_pos

    din.right_hand_rot = right_hand_rot
    din.right_hand_pos = right_hand_pos
    mutex.release()

def Sensor_data_in(imuNum, imu_accin, imu_gyroin):
    # swapped IMU9 with IMU1, swapped IMU10 with IMU6. Physical IMU changes: 
    # IMU1 -> left lower arm
    # IMU6 -> right lower arm
    # IMU9 -> waist
    # IMU10 -> chest
    mutex.acquire()
    global imu1_acc_prev, imu2_acc_prev, imu3_acc_prev, imu4_acc_prev, imu5_acc_prev, imu6_acc_prev, imu7_acc_prev, imu8_acc_prev, imu9_acc_prev, imu10_acc_prev, imu1_gyro_prev, imu2_gyro_prev, imu3_gyro_prev, imu4_gyro_prev, imu5_gyro_prev, imu6_gyro_prev, imu7_gyro_prev, imu8_gyro_prev, imu9_gyro_prev, imu10_gyro_prev
    use_buffer = False
    #<--- exponential moving average --->#
    if not use_buffer:
        alpha = 0.5
        if(imuNum == ["imu9"]):
            din.imu1_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu1_acc_prev
            din.imu1_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu1_gyro_prev
            imu1_acc_prev = din.imu1_acc
            imu1_gyro_prev = din.imu1_gyro
        elif(imuNum == ["imu2"]):
            din.imu2_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu2_acc_prev
            din.imu2_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu2_gyro_prev
            imu2_acc_prev = din.imu2_acc
            imu2_gyro_prev = din.imu2_gyro
        elif(imuNum == ["imu3"]):
            din.imu3_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu3_acc_prev
            din.imu3_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu3_gyro_prev
            imu3_acc_prev = din.imu3_acc
            imu3_gyro_prev = din.imu3_gyro
        elif(imuNum == ["imu4"]):
            din.imu4_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu4_acc_prev
            din.imu4_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu4_gyro_prev
            imu4_acc_prev = din.imu4_acc
            imu4_gyro_prev = din.imu4_gyro
        elif(imuNum == ["imu5"]):
            din.imu5_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu5_acc_prev
            din.imu5_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu5_gyro_prev
            imu5_acc_prev = din.imu5_acc
            imu5_gyro_prev = din.imu5_gyro
        elif(imuNum == ["imu10"]):
            din.imu6_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu6_acc_prev
            din.imu6_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu6_gyro_prev
            imu6_acc_prev = din.imu6_acc
            imu6_gyro_prev = din.imu6_gyro
        elif(imuNum == ["imu7"]):
            din.imu7_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu7_acc_prev
            din.imu7_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu7_gyro_prev
            imu7_acc_prev = din.imu7_acc
            imu7_gyro_prev = din.imu7_gyro
        elif(imuNum == ["imu8"]):
            din.imu8_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu8_acc_prev
            din.imu8_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu8_gyro_prev
            imu8_acc_prev = din.imu8_acc
            imu8_gyro_prev = din.imu8_gyro
        elif(imuNum == ["imu1"]):
            din.imu9_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu9_acc_prev
            din.imu9_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu9_gyro_prev
            imu9_acc_prev = din.imu9_acc
            imu9_gyro_prev = din.imu9_gyro
        elif(imuNum == ["imu6"]):
            din.imu10_acc = np.array([float(i) for i in imu_accin])*alpha+(1-alpha)*imu10_acc_prev
            din.imu10_gyro = np.array([float(i) for i in imu_gyroin])*alpha+(1-alpha)*imu10_gyro_prev
            imu10_acc_prev = din.imu10_acc
            imu10_gyro_prev = din.imu10_gyro
        mutex.release()
        return
    #<--- using flat weight average --->#
    if(imuNum == ["imu9"]):
        imu1_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu1_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu1_acc_buff)>BUFFER_SIZE:
            imu1_acc_buff.pop(0)
        if len(imu1_gyro_buff)>BUFFER_SIZE:
            imu1_gyro_buff.pop(0)
        din.imu1_acc = np.average(imu1_acc_buff, axis=0)
        din.imu1_gyro = np.average(imu1_gyro_buff, axis=0)
    elif(imuNum == ["imu2"]):
        imu2_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu2_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu2_acc_buff)>BUFFER_SIZE:
            imu2_acc_buff.pop(0)
        if len(imu2_gyro_buff)>BUFFER_SIZE:
            imu2_gyro_buff.pop(0)
        din.imu2_acc = np.average(imu2_acc_buff, axis=0)
        din.imu2_gyro = np.average(imu2_gyro_buff, axis=0)
    elif(imuNum == ["imu3"]):
        imu3_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu3_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu3_acc_buff)>BUFFER_SIZE:
            imu3_acc_buff.pop(0)
        if len(imu3_gyro_buff)>BUFFER_SIZE:
            imu3_gyro_buff.pop(0)
        din.imu3_acc = np.average(imu3_acc_buff, axis=0)
        din.imu3_gyro = np.average(imu3_gyro_buff, axis=0)
    elif(imuNum == ["imu4"]):
        imu4_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu4_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu4_acc_buff)>BUFFER_SIZE:
            imu4_acc_buff.pop(0)
        if len(imu4_gyro_buff)>BUFFER_SIZE:
            imu4_gyro_buff.pop(0)
        din.imu4_acc = np.average(imu4_acc_buff, axis=0)
        din.imu4_gyro = np.average(imu4_gyro_buff, axis=0)
    elif(imuNum == ["imu5"]):
        imu5_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu5_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu5_acc_buff)>BUFFER_SIZE:
            imu5_acc_buff.pop(0)
        if len(imu5_gyro_buff)>BUFFER_SIZE:
            imu5_gyro_buff.pop(0)
        din.imu5_acc = np.average(imu5_acc_buff, axis=0)
        din.imu5_gyro = np.average(imu5_gyro_buff, axis=0)
    elif(imuNum == ["imu10"]):
        imu6_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu6_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu6_acc_buff)>BUFFER_SIZE:
            imu6_acc_buff.pop(0)
        if len(imu6_gyro_buff)>BUFFER_SIZE:
            imu6_gyro_buff.pop(0)
        din.imu6_acc = np.average(imu6_acc_buff, axis=0)
        din.imu6_gyro = np.average(imu6_gyro_buff, axis=0)
    elif(imuNum == ["imu7"]):
        imu7_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu7_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu7_acc_buff)>BUFFER_SIZE:
            imu7_acc_buff.pop(0)
        if len(imu7_gyro_buff)>BUFFER_SIZE:
            imu7_gyro_buff.pop(0)
        din.imu7_acc = np.average(imu7_acc_buff, axis=0)
        din.imu7_gyro = np.average(imu7_gyro_buff, axis=0)
    elif(imuNum == ["imu8"]):
        imu8_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu8_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu8_acc_buff)>BUFFER_SIZE:
            imu8_acc_buff.pop(0)
        if len(imu8_gyro_buff)>BUFFER_SIZE:
            imu8_gyro_buff.pop(0)
        din.imu8_acc = np.average(imu8_acc_buff, axis=0)
        din.imu8_gyro = np.average(imu8_gyro_buff, axis=0)
    elif(imuNum == ["imu1"]):
        imu9_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu9_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu9_acc_buff)>BUFFER_SIZE:
            imu9_acc_buff.pop(0)
        if len(imu9_gyro_buff)>BUFFER_SIZE:
            imu9_gyro_buff.pop(0)
        din.imu9_acc = np.average(imu9_acc_buff, axis=0)
        din.imu9_gyro = np.average(imu9_gyro_buff, axis=0)
    elif(imuNum == ["imu6"]):
        imu10_acc_buff.append(np.array([float(i) for i in imu_accin]))
        imu10_gyro_buff.append(np.array([float(i) for i in imu_gyroin]))
        if len(imu10_acc_buff)>BUFFER_SIZE:
            imu10_acc_buff.pop(0)
        if len(imu10_gyro_buff)>BUFFER_SIZE:
            imu10_gyro_buff.pop(0)
        din.imu10_acc = np.average(imu10_acc_buff, axis=0)
        din.imu10_gyro = np.average(imu10_gyro_buff, axis=0)
    mutex.release()

def angle_between(v1, v2):
    # convert raidan to degree
    """ Returns the angle in radian between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))*180/np.pi


def get_imu_measured_rpy(acc,gyro,rpy_0,cur_angle_idx,deltaTime):
    global cur_angles
    # convert radian to degree using *180.0/np.pi
    roll_mea = rpy_0[0] + (np.arctan2(np.sqrt(acc[0]**2+acc[1]**2),acc[2])*180.0/np.pi  -  90)
    yaw_mea = rpy_0[2] - np.arctan2(acc[1],np.sqrt(acc[0]**2+acc[2]**2))*180.0/np.pi
    # pitch updates from gyro around +g/-g, also filter small rotation
    proj_vu = np.dot(acc,gyro)/(np.linalg.norm(acc)**2)*acc
    current_rot_g = np.linalg.norm(proj_vu)
    cur_angle = cur_angles[cur_angle_idx]
    if current_rot_g > 0.1:
        # print("rotated by:",current_rot_g)
        angle_diff = angle_between(acc,proj_vu)
        if abs(angle_diff)<5:
            cur_angle = cur_angle - current_rot_g*deltaTime*180.0/np.pi
        elif abs(angle_diff+180)<5 or abs(angle_diff-180)<5:
            cur_angle = cur_angle + current_rot_g*deltaTime*180.0/np.pi
    if cur_angle>180:
        cur_angle -= 360
    elif cur_angle<-180:
        cur_angle += 360
    cur_angles[cur_angle_idx] = cur_angle
    return np.array([roll_mea,cur_angle,yaw_mea])

def get_FK_calculated_rpy(chest_rpy,upper_arm_rpy,isleft,lower_arm_0):
    # here we assume rpy is rotation in xyz order, so that we have g=gz@gy@gx@g_p1@gz@gy@gx@g_p2
    # actually, in unity, we have extrinsic zxy order, so we have g=gy@gx@gz@g_p1@gy@gx@gz@g_p2
    L2 = halfchestwidth if isleft else -halfchestwidth
    L3 = armlength if isleft else -armlength
    c_r, c_p, c_y = chest_rpy
    u_r, u_p, u_y = upper_arm_rpy
    g_p1 = np.array([[1,0,0,L2],
                    [0,1,0,spinelength],
                    [0,0,1,0],
                    [0,0,0,1]])
    g_p2 = np.array([[1,0,0,L3],
                    [0,1,0,0],
                    [0,0,1,0],
                    [0,0,0,1]])
    g1 = np.matrix([[np.cos(-c_y), -np.sin(-c_y), 0, 0],
                [np.sin(-c_y), np.cos(-c_y), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    g2 = np.matrix([[np.cos(-c_p), 0, np.sin(-c_p), 0],
                [0, 1, 0, 0],
                [-np.sin(-c_p), 0, np.cos(-c_p),0],
                [0, 0, 0, 1]])
    g3 = np.matrix([[1, 0, 0, 0],
                [0, np.cos(c_r), -np.sin(c_r), 0],
                [0, np.sin(c_r), np.cos(c_r), 0],
                [0, 0, 0, 1]])
    g4 = np.matrix([[np.cos(-u_y), -np.sin(-u_y), 0, 0],
                [np.sin(-u_y), np.cos(-u_y), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
    g5 = np.matrix([[np.cos(-u_p), 0, np.sin(-u_p), 0],
                [0, 1, 0, 0],
                [-np.sin(-u_p), 0, np.cos(-u_p),0],
                [0, 0, 0, 1]])
    g6 = np.matrix([[1, 0, 0, 0],
                [0, np.cos(u_r), -np.sin(u_r), 0],
                [0, np.sin(u_r), np.cos(u_r), 0],
                [0, 0, 0, 1]])
    # g = g1 @ g2 @ g3 @ g_p1 @ g4 @ g5 @ g6 @ g_p2
    g = g2 @ g3 @ g1 @ g_p1 @ g5 @ g6 @ g4 @ g_p2
    # invert x so that we are in Unity coordinate, and because we need global position, reference x,y,z coordinate of head
    p_elbow = np.array([-g[0,3]+din.head_pos[0], g[1,3]+din.head_pos[1]-(necklength+spinelength), g[2,3]+din.head_pos[2]])
    p_hand = din.left_hand_pos if isleft else din.right_hand_pos
    p = p_hand - p_elbow
    roll_cal = lower_arm_0[0]
    # note: xyz rpy rotation is same as zyx euler rotation, also convert radian to degree with *180.0/np.pi
    # if not isleft:
    #     yaw_cal = lower_arm_0[2] + np.arctan2(p[1],p[0])*180.0/np.pi
    #     pitch_cal = lower_arm_0[1] - np.arcsin(p[2]/np.linalg.norm(p))*180.0/np.pi
    # else:
    #     yaw_cal = lower_arm_0[2] + np.arctan2(p[1],p[0])*180.0/np.pi - 180
    #     pitch_cal = lower_arm_0[1] + np.arcsin(p[2]/np.linalg.norm(p))*180.0/np.pi
    ##--------------- actually we are using extrinsic zxy, and pitch is inverted ---------------##
    if not isleft:
        yaw_cal = lower_arm_0[2] + np.arcsin(p[1]/np.linalg.norm(p))*180.0/np.pi
        # pitch_cal = lower_arm_0[1] + np.arcsin(p[2]/np.linalg.norm(p))*180.0/np.pi
        pitch_cal = lower_arm_0[1] - np.arctan2(p[2],p[0])*180.0/np.pi
    else:
        yaw_cal = lower_arm_0[2] - np.arcsin(p[1]/np.linalg.norm(p))*180.0/np.pi
        # pitch_cal = lower_arm_0[1] - np.arcsin(p[2]/np.linalg.norm(p))*180.0/np.pi
        pitch_cal = lower_arm_0[1] - (np.arctan2(p[2],p[0])*180.0/np.pi - 180)
    # if isleft:
    #     print("leftcheck:",p_elbow,p_hand,p,armlength,yaw_cal,lower_arm_0[2], np.arcsin(p[1]/np.linalg.norm(p))*180.0/np.pi)
    # else:
    #     print("rightcheck:",p_elbow)
    return np.array([roll_cal,pitch_cal,yaw_cal])

def algorithm(deltaTime):
    # detalTime: time in seconds that has passed since this function is called last time 

    # din: tracking data given to the algorithm. 
    # To access fields: din.head_rot, din.imu1_acc... See from input_struct file.

    # dout: joints data computed from tracking data
    # To access fields: out.left_upper_leg, out.waist... See from output_struct file.

    # numpy as np is imported. If others are used, list them in requirements.txt

    # IMU1 -> waist ; IMU2 -> left_upper_leg ; IMU3 -> right_upper_leg ;
    # IMU4 -> left_lower_leg ; IMU5 -> right_lower_leg ; IMU6 -> chest ;
    # IMU7 -> left_upper_arm ; IMU8 -> right_upper_arm; 
    # IMU9 -> left_lower_arm ; IMU10 -> right_lower_arm;
    # Unity performs the Euler rotations sequentially around the z-axis, the x-axis and then the y-axis.
    
    global calibration
    global waist_0,left_upper_leg_0,right_upper_leg_0,left_lower_leg_0,right_lower_leg_0,chest_0,left_upper_arm_0,right_upper_arm_0,left_lower_arm_0,right_lower_arm_0
    if calibration==0:
        # set the initial global rpy
        waist_0 = np.zeros(3)
        left_upper_leg_0 = np.zeros(3)
        right_upper_leg_0 = np.zeros(3)
        left_lower_leg_0 = np.zeros(3)  # setting it to global rpy of left upper leg
        right_lower_leg_0 = np.zeros(3) # setting it to global rpy of right upper leg
        chest_0 = np.zeros(3)
        left_upper_arm_0 = np.zeros(3)
        right_upper_arm_0 = np.zeros(3)
        left_lower_arm_0 = np.zeros(3)    # setting it to global rpy of left upper arm
        right_lower_arm_0 = np.zeros(3)   # setting it to global rpy of right upper arm
        # set the initial global rpy
        # waist_0 = np.array([0,0,0])
        # left_upper_leg_0 = np.array([-180,0,0])
        # right_upper_leg_0 = np.array([-180,0,0])
        # left_lower_leg_0 = np.array([-180,0,0])  # setting it to global rpy of left upper leg
        # right_lower_leg_0 = np.array([-180,0,0]) # setting it to global rpy of right upper leg
        # chest_0 = np.array([0,0,0])
        # left_upper_arm_0 = np.array([-75,81,-71])
        # right_upper_arm_0 = np.array([-75,-81,71])
        # left_lower_arm_0 = np.array([-75,81,-71])    # setting it to global rpy of left upper arm
        # right_lower_arm_0 = np.array([-75,-81,71])   # setting it to global rpy of right upper arm
    if calibration==1:
        # left_upper_leg = np.array([-180,0,0])
        # left_lower_leg = np.array([0,0,0])

        # right_upper_leg = np.array([-180,0,0]) 
        # right_lower_leg = np.array([0,0,0]) 

        # left_upper_arm = np.array([-75,81,-71])
        # left_lower_arm = np.array([0,0,0])
        # left_hand = np.zeros(3)

        # right_upper_arm = np.array([-75,-81,71])
        # right_lower_arm =  np.array([0,0,0])
        # right_hand = np.zeros(3)

        # waist = np.zeros(3)
        # chest = np.zeros(3)
        # head = np.zeros(3)
        # calibration phase, get halfchestwidth, spinelength, armlength

        # set the initial global rpy
        waist_0 = np.zeros(3)
        left_upper_leg_0 = np.zeros(3)
        right_upper_leg_0 = np.zeros(3)
        left_lower_leg_0 = np.zeros(3)  # setting it to global rpy of left upper leg
        right_lower_leg_0 = np.zeros(3) # setting it to global rpy of right upper leg
        chest_0 = np.zeros(3)
        left_upper_arm_0 = np.zeros(3)
        right_upper_arm_0 = np.zeros(3)
        left_lower_arm_0 = np.zeros(3)    # setting it to global rpy of left upper arm
        right_lower_arm_0 = np.zeros(3)   # setting it to global rpy of right upper arm
        # start calibration
        CALIBINTERVAL = 1
        global halfchestwidth, spinelength, armlength, necklength
        print("move controller to waist")
        time.sleep(CALIBINTERVAL)
        mutex.acquire()
        waist_pos = (din.head_pos[0], (din.left_hand_pos[1]+din.right_hand_pos[1])/2, din.head_pos[2])
        print("move controller to shoulder")
        mutex.release()
        time.sleep(CALIBINTERVAL)
        mutex.acquire()
        left_shoulder_pos = (din.left_hand_pos[0], din.left_hand_pos[1], din.head_pos[2])
        right_shoulder_pos = (din.right_hand_pos[0], din.right_hand_pos[1], din.head_pos[2])
        halfchestwidth = (right_shoulder_pos[0] - left_shoulder_pos[0])/2
        spinelength = (right_shoulder_pos[1] + left_shoulder_pos[1])/2 - waist_pos[1]
        necklength = din.head_pos[1] - (right_shoulder_pos[1] + left_shoulder_pos[1])/2
        mutex.release()
        print("T-pose")
        time.sleep(CALIBINTERVAL)
        mutex.acquire()
        armlength = (din.right_hand_pos[0] - din.left_hand_pos[0] - 2 * halfchestwidth) / 4
        print("check1:",waist_pos,left_shoulder_pos,right_shoulder_pos,din.left_hand_pos,din.right_hand_pos,din.head_pos)
        print("check2:",halfchestwidth,spinelength,necklength,armlength)
        # reset gyroscope angle to initial global pitch, the order is
        # [waist_angle,left_upper_leg_angle,right_upper_leg_angle,left_lower_leg_angle,right_lower_leg_angle,chest_angle,left_upper_arm_angle,right_upper_arm_angle,left_lower_arm_angle,right_lower_arm_angle]
        global cur_angles
        cur_angles = np.zeros(10)
        ## set initial global rpy
        empty_gyro = np.zeros(3)
        waist_0 = -get_imu_measured_rpy(din.imu1_acc,empty_gyro,waist_0,0,deltaTime)
        left_upper_leg_0 = -get_imu_measured_rpy(din.imu2_acc,empty_gyro,left_upper_leg_0,1,deltaTime)
        right_upper_leg_0 = -get_imu_measured_rpy(din.imu3_acc,empty_gyro,right_upper_leg_0,2,deltaTime)
        left_lower_leg_0 =  -get_imu_measured_rpy(din.imu4_acc,empty_gyro,left_lower_leg_0,3,deltaTime)
        right_lower_leg_0 =  -get_imu_measured_rpy(din.imu5_acc,empty_gyro,right_lower_leg_0,4,deltaTime)
        chest_0 =  -get_imu_measured_rpy(din.imu6_acc,empty_gyro,chest_0,5,deltaTime)
        left_upper_arm_0 = -get_imu_measured_rpy(din.imu7_acc,empty_gyro,left_upper_arm_0,6,deltaTime)
        right_upper_arm_0 = -get_imu_measured_rpy(din.imu8_acc,empty_gyro,right_upper_arm_0,7,deltaTime)
        left_lower_arm_0 = -get_imu_measured_rpy(din.imu9_acc,empty_gyro,left_lower_arm_0,8,deltaTime)
        right_lower_arm_0 = -get_imu_measured_rpy(din.imu10_acc,empty_gyro,right_lower_arm_0,9,deltaTime)
        calibration = 2
        mutex.release()
        return
    
    mutex.acquire()
    # local rpy of waist
    dout.waist = get_imu_measured_rpy(din.imu1_acc,din.imu1_gyro,waist_0,0,deltaTime)
    # local rpy of upper legs
    dout.left_upper_leg = get_imu_measured_rpy(din.imu2_acc,din.imu2_gyro,left_upper_leg_0,1,deltaTime)
    dout.right_upper_leg = get_imu_measured_rpy(din.imu3_acc,din.imu3_gyro,right_upper_leg_0,2,deltaTime)
    # local rpy of lower legs
    dout.left_lower_leg = get_imu_measured_rpy(din.imu4_acc,din.imu4_gyro,left_lower_leg_0,3,deltaTime) - dout.left_upper_leg
    dout.right_lower_leg = get_imu_measured_rpy(din.imu5_acc,din.imu5_gyro,right_lower_leg_0,4,deltaTime) - dout.right_upper_leg
    # local rpy of chest
    dout.chest = get_imu_measured_rpy(din.imu6_acc,din.imu6_gyro,chest_0,5,deltaTime) - dout.waist
    # local rpy of upper arms
    dout.left_upper_arm = get_imu_measured_rpy(din.imu7_acc,din.imu7_gyro,left_upper_arm_0,6,deltaTime) - dout.waist - dout.chest
    dout.right_upper_arm = get_imu_measured_rpy(din.imu8_acc,din.imu8_gyro,right_upper_arm_0,7,deltaTime) - dout.waist - dout.chest
    
    ##---------- for testing: disable pitch ----------##
    disable_pitch = False
    if disable_pitch:
        dout.waist[1] = waist_0[1]
        dout.left_upper_leg[1] = left_upper_leg_0[1]
        dout.right_upper_leg[1] = right_upper_leg_0[1]
        dout.left_lower_leg[1] = left_lower_leg_0[1]
        dout.right_lower_leg[1] = right_lower_leg_0[1]
        dout.chest[1] = chest_0[1]
        dout.left_upper_arm[1] = left_upper_arm_0[1]
        dout.right_upper_arm[1] = right_upper_arm_0[1]
    ##---------- end testing: disable pitch ----------##
    
    # local rpy of lower arms, here the input upper_arm_rpy and chest_rpy are set to be (0,0,0) in T-pose, and chest_rpy here should be global rpy, upper_arm_rpy should be local rpy
    # dout.left_lower_arm = get_FK_calculated_rpy(dout.chest+dout.waist,dout.left_upper_arm-left_upper_arm_0,True,left_lower_arm_0) - dout.waist - dout.chest - dout.left_upper_arm
    # dout.right_lower_arm = get_FK_calculated_rpy(dout.chest+dout.waist,dout.right_upper_arm-right_upper_arm_0,False,right_lower_arm_0) - dout.waist - dout.chest - dout.right_upper_arm
    dout.left_lower_arm = get_imu_measured_rpy(din.imu9_acc,din.imu9_gyro,left_lower_arm_0,8,deltaTime) - dout.waist - dout.chest - dout.left_upper_arm
    dout.right_lower_arm = get_imu_measured_rpy(din.imu10_acc,din.imu10_gyro,right_lower_arm_0,9,deltaTime) - dout.waist - dout.chest - dout.right_upper_arm
    # local rpy of hands (assuming din is global rpy)
    dout.left_hand = din.left_hand_rot - dout.waist - dout.chest - dout.left_upper_arm - dout.left_lower_arm
    dout.right_hand = din.right_hand_rot - dout.waist - dout.chest - dout.right_upper_arm - dout.right_lower_arm
    # local rpy of head (assuming din is global rpy)
    dout.head = din.head_rot - dout.waist - dout.chest

    # dout.waist[1] = -dout.waist[1]
    # dout.chest[1] = -dout.chest[1]
    mutex.release()
    

def intialize():
    x = threading.Thread(target=consumer_thread, args=(1,))
    x.daemon = True
    x.start()

    y = threading.Thread(target=thread_function, args=(1,))
    y.daemon = True
    y.start()

def begin_algorithm():
    global algo_begin, calibration
    algo_begin = True
    calibration = 1
    print("Begin algorithm and calibration: ", algo_begin)

def consumer_thread(_):
    # checkgyro()
    current_time = time.time()
    while(True):
        global algo_begin
        if (algo_begin):
            prev_time = current_time
            current_time = time.time()
            while (current_time - prev_time < 0.007):
                # Limit computation frame rate
                current_time = time.time()
            algorithm(current_time - prev_time)
            # print("Time elapsed: ", current_time - prev_time)
            # printdout()


"""
-----------------------------------------
--------- Test functions below ----------
""" 

def thread_function(name):
    time.sleep(3)
    while(True):
        global calibration
        
        logging.info("Thread %s: starting", name)
        if calibration is not 1:
            printdin()
            # printcheckgyro()
        if calibration==2:
            printdout()
        time.sleep(3)
        logging.info("Thread %s: finishing", name)

def checkgyro():
    print("\n===========start checking gyro==============\n")
    global acc_p,gyro_p,current_rot_p,current_rot_g_p,cur_angle,proj_vu_p
    current_time = time.time()
    cur_angle = 0
    while(True):
        prev_time = current_time
        current_time = time.time()
        while (current_time - prev_time < 0.007):
            # Limit computation frame rate
            current_time = time.time()
        deltaTime = current_time - prev_time
        #<---- check gyro scope 1 ---->#
        acc_p, gyro_p = din.imu1_acc,din.imu1_gyro
        current_rot_p = np.linalg.norm(gyro_p)
        proj_vu_p = np.dot(acc_p,gyro_p)/(np.linalg.norm(acc_p)**2)*acc_p
        current_rot_g_p = np.linalg.norm(proj_vu_p)
        if current_rot_g_p >0.1:
            angle_diff = angle_between(acc_p,proj_vu_p)
            if abs(angle_diff)<5:
                cur_angle = cur_angle - current_rot_g_p*deltaTime*180.0/np.pi
            elif abs(angle_diff+180)<5 or abs(angle_diff-180)<5:
                cur_angle = cur_angle + current_rot_g_p*deltaTime*180.0/np.pi

def printcheckgyro():
    global acc_p,gyro_p,current_rot_p,current_rot_g_p,cur_angle,proj_vu_p
    print("\n===========check gyro result==============\n")
    print("acc reading          :",acc_p)
    print("gyro reading         :",gyro_p)
    print("project_v(u)         :",proj_vu_p)
    print("angular velocity     :",current_rot_p)
    print("angular velocity to g:",current_rot_g_p)
    print("cur_angle            :",cur_angle)
    print("check:",np.dot(acc_p,gyro_p),(np.linalg.norm(acc_p)**2),acc_p)

def printdin():
    print("\n===========din==============\n")
    print(din.head_rot)
    print(din.head_pos)

    print(din.left_hand_rot)
    print(din.left_hand_pos)

    print(din.right_hand_rot)
    print(din.right_hand_pos)
    print("============================")
    print(din.imu1_acc)
    print(din.imu1_gyro)
    print(din.imu2_acc)
    print(din.imu2_gyro)
    print(din.imu3_acc)
    print(din.imu3_gyro)
    print(din.imu4_acc)
    print(din.imu4_gyro)
    print(din.imu5_acc)
    print(din.imu5_gyro)
    print(din.imu6_acc)
    print(din.imu6_gyro)
    print(din.imu7_acc)
    print(din.imu7_gyro)
    print(din.imu8_acc)
    print(din.imu8_gyro)
    print(din.imu9_acc)
    print(din.imu9_gyro)
    print(din.imu10_acc)
    print(din.imu10_gyro)
    print("\n============================\n")


def printdout():
    print("\n===========dout==============\n")
    print("waist: ", dout.waist)
    print("left_upper_leg: ", dout.left_upper_leg)
    print("right_upper_leg: ", dout.right_upper_leg)
    print("left_lower_leg: ", dout.left_lower_leg)
    print("right_lower_leg: ", dout.right_lower_leg)
    print("chest: ", dout.chest)
    print("left_upper_arm: ", dout.left_upper_arm)
    print("right_upper_arm: ", dout.right_upper_arm)
    print("left_lower_arm: ", dout.left_lower_arm)
    print("right_lower_arm: ", dout.right_lower_arm)
    print("left_hand: ", dout.left_hand)
    print("right_hand: ", dout.right_hand)
    print("head: ", dout.head)
    print("\n============================\n")

def test():
    print("test!")
    global calibration, halfchestwidth, spinelength, armlength, necklength
    calibration = False
    halfchestwidth = 0.2
    spinelength = 0.4
    armlength = 0.3
    necklength = 0.1
    # set the initial global rpy
    waist_0 = np.array([0,0,0])
    left_upper_leg_0 = np.array([-180,0,0])
    right_upper_leg_0 = np.array([-180,0,0])
    left_lower_leg_0 = np.array([-180,0,0])  # setting it to global rpy of left upper leg
    right_lower_leg_0 = np.array([-180,0,0]) # setting it to global rpy of right upper leg
    chest_0 = np.array([0,0,0])
    left_upper_arm_0 = np.array([-75,81,-71])
    right_upper_arm_0 = np.array([-75,-81,71])
    left_lower_arm_0 = np.array([-75,81,-71])    # setting it to global rpy of left upper arm
    right_lower_arm_0 = np.array([-75,-81,71])   # setting it to global rpy of right upper arm
    # reset gyroscope angle
    dout.waist[1] = waist_0[1]
    dout.left_upper_leg[1] = left_upper_leg_0[1]
    dout.right_upper_leg[1] = right_upper_leg_0[1]
    dout.left_lower_leg[1] = left_lower_leg_0[1]
    dout.right_lower_leg[1] = right_lower_leg_0[1]
    dout.chest[1] = chest_0[1]
    dout.left_upper_arm[1] = left_upper_arm_0[1]
    dout.right_upper_arm[1] = right_upper_arm_0[1]
    # initialize previous angular velocity
    global imu1_gyro_prev, imu2_gyro_prev, imu3_gyro_prev, imu4_gyro_prev, imu5_gyro_prev, imu6_gyro_prev, imu7_gyro_prev, imu8_gyro_prev
    imu1_gyro_prev = np.array([0,0,0])
    imu2_gyro_prev = np.array([0,0,0])
    imu3_gyro_prev = np.array([0,0,0])
    imu4_gyro_prev = np.array([0,0,0])
    imu5_gyro_prev = np.array([0,0,0])
    imu6_gyro_prev = np.array([0,0,0])
    imu7_gyro_prev = np.array([0,0,0])
    imu8_gyro_prev = np.array([0,0,0])
    din.imu1_acc = np.array([-9.8, 0, 0])
    din.imu1_gyro = np.array([0 ,0 ,0])
    din.imu2_acc = np.array([-9.8, 0, 0])
    din.imu2_gyro = np.array([0 ,0 ,0])
    din.imu3_acc = np.array([0, -9.8, 0])
    din.imu3_gyro = np.array([0 ,0 ,0])
    din.imu4_acc = np.array([-9.8, 0, 0])
    din.imu4_gyro = np.array([0 ,0 ,0])
    din.imu5_acc = np.array([-9.8, 0, 0])
    din.imu5_gyro = np.array([0 ,0 ,0])
    din.imu6_acc = np.array([-9.8, 0, 0])
    din.imu6_gyro = np.array([0 ,0 ,0])
    din.imu7_acc = np.array([-9.8, 0, 0])
    din.imu7_gyro = np.array([0 ,0 ,0])
    din.imu8_acc = np.array([0, 9.8, 0])
    din.imu8_gyro = np.array([0 ,0 ,0])
    din.head_pos = np.array([0 ,1.8, 0])
    din.head_rot = np.array([0 ,0 ,0])
    din.left_hand_pos = np.array([-0.6 ,1.7 ,0.1])
    din.left_hand_rot = np.array([0 ,0 ,0])
    din.right_hand_pos = np.array([0.8 ,1.7 ,0])
    din.right_hand_rot = np.array([0 ,0 ,0])
    algorithm(0.01)
    printdout()

if __name__ == "__main__":
    test()
