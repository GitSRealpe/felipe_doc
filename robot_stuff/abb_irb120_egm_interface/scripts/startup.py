#!/usr/bin/env python3
import rospy
import math
import time

from abb_rapid_sm_addin_msgs.srv import *
from abb_robot_msgs.srv import *
from controller_manager_msgs.srv import *

rospy.wait_for_service('/rws/sm_addin/get_egm_settings')
rospy.wait_for_service('/rws/sm_addin/set_egm_settings')
get_egm_settings = rospy.ServiceProxy("/rws/sm_addin/get_egm_settings", GetEGMSettings)
set_egm_settings = rospy.ServiceProxy("/rws/sm_addin/set_egm_settings", SetEGMSettings)

taskname='T_ROB1'
current_settings = get_egm_settings(task=taskname)
settings = current_settings.settings

# max_speed_deviation is in deg/s, we convert from rad/s
settings.activate.max_speed_deviation = math.degrees(3.0)
settings.run.cond_time=1800
print (settings)

set_egm_settings(task=taskname, settings=settings)

#inicia sesion EGM
rospy.wait_for_service('/rws/sm_addin/start_egm_joint')
start_egm_joint = rospy.ServiceProxy("/rws/sm_addin/start_egm_joint", TriggerWithResultCode)
start_egm_joint()

#cambiar al controlador joint_trajectory_controller
time.sleep(1)
rospy.wait_for_service('/egm/controller_manager/switch_controller')
switch_controller = rospy.ServiceProxy("/egm/controller_manager/switch_controller", SwitchController)
controller="joint_trajectory_controller"
ret=switch_controller(start_controllers=[controller],strictness=1)
print(ret)
