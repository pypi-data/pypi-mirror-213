'''
Example on how to use Brick from Python together with AGX python bindings.
This file can be launched using python interpreter directly, or using `agxViewer`.
'''

import sys
import os

import agxCollide
import agx
import agxSDK
import agxOSG
import agxRender
import agxTerrain
import agxPython
import agxIO
import agxBrick

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float32

except Exception as e:
    print("ROS2 could not be imported. Please ensure that the ROS2 script 'local_setup.bat' has been run.\n")
    #traceback.print_exc()
    sys.exit(2)

# ROS2 subscriber node class
class RosSubscriber(Node):
    def __init__(self, node_name):
        super().__init__(node_name)

    def register_callback(self, topic, callback_function):
        self.create_subscription(
            Float32,
            topic,
            callback_function,
            10)

# # ROS2 publisher node class
# class RosPublisher(Node):

#     def __init__(self, node_name, topic_name):
#         super().__init__(node_name)

#         self.publisher = self.create_publisher(Float32, topic_name, 1)

#     def send_data(self, data):
#         msg = Float32()
#         msg.data = data

#         self.publisher.publish(msg)

class SignalCallback():
    def __init__(self, signal):
        self.signal = signal

    def callback_set_speed(self, msg):
        print("Setting data: {}".format(msg.data))
        self.signal.SetData(msg.data)

# Class representing the communication, containing ROS2 nodes
class RosCommunicator(agxSDK.StepEventListener):
    def __init__(self, brickSimulation):
        super().__init__()

        self.ros_subscriber = RosSubscriber("ros_brick_listener")
        self._signalCallbacks = []
        for signal in brickSimulation.InputSignals:
            signalCallback = SignalCallback(signal)
            self._signalCallbacks.append(signalCallback)
            motor = signal['Motor']
            name = motor['Name']
            print("COntrolled signal: {}".format(name))
            self.ros_subscriber.register_callback(name, signalCallback.callback_set_speed)


    def pre(self, time):
        # Spin once will generate callback if a new message has been received
        print("spin once")
        rclpy.spin_once(self.ros_subscriber, timeout_sec=0.0)

    def removeNotification(self):
        self.ros_subscriber.destroy_node()
