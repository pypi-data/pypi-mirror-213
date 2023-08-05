import time
import math
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


class InputSignalCallback():
    def __init__(self, signal):
        self.signal = signal

    def callback_set_float(self, msg):
        print("Setting data: {}".format(msg.data))
        self.signal.SetData(msg.data)


class OutputSignalCallback():
    def __init__(self):
        self.plotData = []

    def callback_get_float(self, msg):
        print("Plotting data: {}".format(msg.data))
        self.plotData.append( msg.data)
        #Last 100 values
        self.plotData = self.plotData[-100:]



try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float32
except Exception as e:
    print("ROS2 could not be imported. Please ensure that the ROS2 script 'local_setup.bat' has been run.\n")
    #traceback.print_exc()
    #sys.exit(2)
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

class BrickModelController(Node):
    def __init__(self, signals):
        super().__init__('brick_controller')
        self._publishers = {}
        self._orderedPublisherNames = []
        
        for signal in signals:
            topic = None
            default_value = 0.4
            value_type = "Speed"
            if hasattr(signal,'Motor'):
                topic = signal['Motor']['Name']
            if hasattr(signal,'Lock'):
                topic = signal['Lock']['Name']
            elif hasattr(signal, 'ContactMaterial'):
                topic = signal['ContactMaterial']['Name']
                default_value = 100.0
                value_type = "Force"
            if topic is not None:
                publisher = self.create_publisher(Float32, topic,10)
                publisher.default_value = default_value
                publisher.value_type = value_type
                self._publishers[topic] = publisher
                self._orderedPublisherNames.append(topic)
                print("controlling {}".format(topic))
            

    def send_data(self, topic, data):
        msg = Float32()
        msg.data = data
        if topic not in self._publishers:
            print("Unknown topic: ", topic)
            return
        publisher = self._publishers[topic]
        print("publishing {} on topic {}".format(msg.data, topic))
        publisher.publish(msg)

class BrickModelOutput(Node):
    def __init__(self, outputSignals):
        super().__init__('brick_signal_output')
        self._publishers = {}
        self._orderedPublisherNames = []
        for signal in outputSignals:
            publisher = None
            topic = None
            default_value = 0.4
            value_type = "Speed"
            if hasattr(signal,'Motor'):
                motor = signal['Motor']
                topic = motor['Name']
                publisher = self.create_publisher(Float32, topic,10)
                
            elif hasattr(signal,'Lock'):
                motor = signal['Lock']
                topic = motor['Name']
                publisher = self.create_publisher(Float32, topic,10)
            elif hasattr(signal, 'ContactMaterial'):
                cm = signal['ContactMaterial']
                topic = cm['Name']
                publisher = self.create_publisher(Float32, topic,10)
                default_value = 100
                value_type = "Force"
            if publisher is not None:
                publisher.default_value = default_value
                publisher.value_type = value_type
                publisher.signal = signal
                self._publishers[topic] = publisher
                self._orderedPublisherNames.append(topic)
                print("plotting {}".format(topic))

    def send_data(self, topic, data):
        msg = Float32()
        msg.data = data
        if topic not in self._publishers:
            print("Unknown topic: ", topic)
            return
        publisher = self._publishers[topic]
        print("publishing {} on topic {}".format(msg.data, topic))
        publisher.publish(msg)

class RosPlotPublisher(agxSDK.StepEventListener):
    def __init__(self, outputSignals):
        super().__init__()
        self.brick_model_output = BrickModelOutput(outputSignals)
    def pre(self, time):
        for pubName in self.brick_model_output._orderedPublisherNames:
            publisher = self.brick_model_output._publishers[pubName]
            self.brick_model_output.send_data(pubName,publisher.signal.GetData())

    def removeNotification(self):
        self.brick_model_output.destroy_node()



# Class representing the communication, containing ROS2 nodes
class RosControlListener(agxSDK.StepEventListener):
    def __init__(self, brickSimulation):
        super().__init__()

        self.ros_subscriber = RosSubscriber("ros_brick_input_listener")
        self._signalCallbacks = []

        for signal in brickSimulation.InputSignals:
            signalCallback = InputSignalCallback(signal)
            self._signalCallbacks.append(signalCallback)
            if hasattr(signal, 'Motor'):
                motor = signal['Motor']
                name = motor['Name']
                print("COntrolled signal: {}".format(name))
                self.ros_subscriber.register_callback(name, signalCallback.callback_set_float)
            elif hasattr(signal, 'Lock'):
                motor = signal['Lock']
                name = motor['Name']
                print("COntrolled signal: {}".format(name))
                self.ros_subscriber.register_callback(name, signalCallback.callback_set_float)
            elif hasattr(signal, 'ContactMaterial'):
                cm = signal['ContactMaterial']
                name = cm['Name']
                print("COntrolled signal: {}".format(name))
                self.ros_subscriber.register_callback(name, signalCallback.callback_set_float)

    def pre(self, time):
        rclpy.spin_once(self.ros_subscriber, timeout_sec=0.0)

    def removeNotification(self):
        self.ros_subscriber.destroy_node()


import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# Class representing the communication, containing ROS2 nodes
class RosPlotListener():
    def __init__(self, brickSimulation):

        import datetime as dt
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        self.ros_subscriber = RosSubscriber("ros_brick_plot_listener")
        self._signalCallbacks = []
        self.timeData = []
        self.axs = []
        count = 1
        for signal in brickSimulation.OutputSignals:
            signalCallback = OutputSignalCallback( )
            signalCallback.fig = plt.figure()
            ax = signalCallback.fig.add_subplot(count, 1, count)
            signalCallback.ax = ax
            self._signalCallbacks.append(signalCallback)
            motor = None
            if hasattr(signal, 'Motor'):
                motor = signal['Motor']
            elif hasattr(signal, 'Lock'):
                motor = signal['Lock']
            if motor is None:
                continue
            name = motor['Name']
            self.ros_subscriber.register_callback(name, signalCallback.callback_get_float)
            count = count + 1

        def update(i, ros_subscriber, plotData):
            rclpy.spin_once(ros_subscriber, timeout_sec=0.0)

            for sc in self._signalCallbacks:
                sc.ax.clear()
                tim = []
                for i in range(len(sc.plotData)):
                    tim.append(i)
                tim = tim[-100:]
                print(tim)
                print(sc.plotData)
                sc.ax.plot(tim, sc.plotData)

            # Format plot
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Torques or velocities')
            plt.ylabel('Output Values')

        for sc in self._signalCallbacks:
            animation.FuncAnimation(sc.fig, update, fargs=(self.ros_subscriber, sc.plotData), interval=1000)
        plt.show()




    def removeNotification(self):
        self.ros_subscriber.destroy_node()



