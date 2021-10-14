#!/usr/bin/env python
from controller_manager_msgs.srv import SwitchController

import rospy
import sys

if __name__ == '__main__':
    try:
        start_ctrl="arm_controller"
        print("argumento recibido",sys.argv[1])
        if (sys.argv[1]=="1"):
            start_ctrl="arm_controller"
            stop_ctrl="joint_group_position_controller"
            print("cambiando a: ", start_ctrl)
        if (sys.argv[1]=="2"):
            start_ctrl="joint_group_position_controller"
            stop_ctrl="arm_controller"
            print("cambiando a: ", start_ctrl)
        sw_controller = rospy.ServiceProxy('controller_manager/switch_controller', SwitchController)
        resp=sw_controller(stop_controllers=[stop_ctrl],
                            start_controllers=[start_ctrl],
                            strictness=2)
        print(resp)
    except rospy.ROSInterruptException:
        pass
