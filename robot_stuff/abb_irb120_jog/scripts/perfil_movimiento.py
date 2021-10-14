#!/usr/bin/env python
import rospy
from geometry_msgs.msg import TwistStamped
import std_msgs.msg

import matplotlib.pyplot as plt
import numpy as np
from math import pi, radians
from time import sleep,time
import copy
import sys

def send(perfil):
    pub = rospy.Publisher('servo_server/delta_twist_cmds', TwistStamped, queue_size=100)
    rospy.init_node('jog_publisher', anonymous=True)
    rate = rospy.Rate(100) # 10hz
    rate.sleep()
    twist_stamped= TwistStamped()
    h = std_msgs.msg.Header()
    cont=0
    last_time=time()
    while(1):
        h.stamp = rospy.Time.now()
        twist_stamped.header=h
        # twist_stamped.twist.linear.z=perfil[cont]
        twist_stamped.twist.linear.z=float(sys.argv[1])
        pub.publish(twist_stamped)
        if (time()-last_time)>=1:
            print("segundo ",time()-last_time)
            last_time=time()
            break;
            # if cont>len(perfil)-2:
            #     cont=0
            # else:
            #     cont=cont+1

        sleep(0.001)
    # twist_stamped.twist.linear.z=float(0)
    # pub.publish(twist_stamped)

def do_perfil():
    # vel_perfil=np.array([1,1,1])
    # print(vel_perfil)
    in_array = np.linspace(-np.pi, np.pi, 12)
    out_array = np.sin(in_array)
    out_array=np.array([-0.1,0.0])
    # print("in_array : ", in_array)
    # print("\nout_array : ", out_array)
    send(out_array)

    # plt.plot(in_array, out_array, color = 'red', marker = "o")
    # plt.title("numpy.sin()")
    # plt.xlabel("X")
    # plt.ylabel("Y")
    # plt.show()

if __name__ == '__main__':
    try:
        do_perfil()
        # send()
    except rospy.ROSInterruptException:
        pass
