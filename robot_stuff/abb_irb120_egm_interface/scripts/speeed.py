#!/usr/bin/env python3
import rospy
import math

from abb_rapid_sm_addin_msgs.srv import *

rospy.wait_for_service('/rws/sm_addin/get_egm_settings')
rospy.wait_for_service('/rws/sm_addin/set_egm_settings')
get_egm_settings = rospy.ServiceProxy("/rws/sm_addin/get_egm_settings", GetEGMSettings)
set_egm_settings = rospy.ServiceProxy("/rws/sm_addin/set_egm_settings", SetEGMSettings)

taskname='T_ROB1'
current_settings = get_egm_settings(task=taskname)
settings = current_settings.settings
print (settings)

# max_speed_deviation is in deg/s, we convert from rad/s
settings.activate.max_speed_deviation = math.degrees(3.0)
print (settings)

set_egm_settings(task=taskname, settings=settings)
