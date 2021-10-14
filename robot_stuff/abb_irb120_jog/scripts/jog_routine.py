#!/usr/bin/env python
from geometry_msgs.msg import TwistStamped
import std_msgs.msg
from math import pi, radians
from time import sleep

import rospy
import copy

pub = rospy.Publisher('servo_server/delta_twist_cmds', TwistStamped, queue_size=10)
rospy.init_node('jog_publisher', anonymous=True)
rate = rospy.Rate(10) # 10hz
# rate.sleep()

twist_stamped= TwistStamped()

h = std_msgs.msg.Header()

while(1):
    h.stamp = rospy.Time.now()
    twist_stamped.header=h
    twist_stamped.twist.linear.z=-0.01
    # twist_stamped.twist.linear.y=-0.01
    # twist_stamped.twist.linear.x=0.01
    pub.publish(twist_stamped)
    # sleep(0.1)
    rate.sleep()

print("enviado")
