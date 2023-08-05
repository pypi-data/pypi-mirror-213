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
import rclpy
from agxPythonModules.utils.environment import simulation, root, application, init_app
from brickLoaderUtils import createArgumentParser, extractModelFilePathAndName
from brickRos2ControllerUtils import BrickModelController
from keyPoller import KeyPoller

def try_publish(brick_controller, c, key_1, key_2, key_3, index ):
    if len(brick_controller._orderedPublisherNames) <= index:
        return
    publisher_name = brick_controller._orderedPublisherNames[index]
    publisher = brick_controller._publishers[publisher_name]
    default_speed = publisher.default_value
    if c == key_1:
        brick_controller.send_data(publisher_name,default_speed)
    if c == key_2:
        brick_controller.send_data(publisher_name,0.0)
    if c == key_3:
        brick_controller.send_data(publisher_name,-default_speed)


def buildScene():
    # Initialize ROS
    rclpy.init()

    # Load brick model just to understand what signals there are
    from Brick.Physics import Component
    from Brick.AGXBrick import BrickSimulation
    from Brick import Path, TypePath, Model, ModelRegistry
    file_path, model_name = extractModelFilePathAndName(args)
    scene = Component.CreateFromFile(file_path, model_name)
    BrickSimulation.Default.AddComponent(scene)

    brick_controller = BrickModelController(BrickSimulation.Default.InputSignals)
    BrickSimulation.Default.Shutdown()

    default_speed = 0.4

    with KeyPoller() as keyPoller:
        while True:
            c = keyPoller.poll()
            if not c is None:
                if c == "p":
                    break
                # Support up to 8 controlled motors
                try_publish(brick_controller, c, 'q', 'a', 'z', 0 )
                # if c == 'q' and len(brick_controller._orderedPublisherNames) > 0:
                #     brick_controller.send_data(brick_controller._orderedPublisherNames[0],default_speed)
                # if c == 'a' and len(brick_controller._orderedPublisherNames) > 0:
                #     brick_controller.send_data(brick_controller._orderedPublisherNames[0],0.0)
                # if c == 'z' and len(brick_controller._orderedPublisherNames) > 0:
                #     brick_controller.send_data(brick_controller._orderedPublisherNames[0],-default_speed)
                if c == 'w' and len(brick_controller._orderedPublisherNames) > 1:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[1],default_speed)
                if c == 's' and len(brick_controller._orderedPublisherNames) > 1:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[1],0.0)
                if c == 'x' and len(brick_controller._orderedPublisherNames) > 1:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[1],-default_speed)
                if c == 'e' and len(brick_controller._orderedPublisherNames) > 2:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[2],default_speed)
                if c == 'd' and len(brick_controller._orderedPublisherNames) > 2:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[2],0.0)
                if c == 'c' and len(brick_controller._orderedPublisherNames) > 2:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[2],-default_speed)
                if c == 'r' and len(brick_controller._orderedPublisherNames) > 3:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[3],default_speed)
                if c == 'f' and len(brick_controller._orderedPublisherNames) > 3:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[3],0.0)
                if c == 'v' and len(brick_controller._orderedPublisherNames) > 3:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[3],-default_speed)
                if c == 't' and len(brick_controller._orderedPublisherNames) > 4:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[4],default_speed)
                if c == 'g' and len(brick_controller._orderedPublisherNames) > 4:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[4],0.0)
                if c == 'b' and len(brick_controller._orderedPublisherNames) > 4:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[4],-default_speed)
                if c == 'y' and len(brick_controller._orderedPublisherNames) > 5:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[5],default_speed)
                if c == 'h' and len(brick_controller._orderedPublisherNames) > 5:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[5],0.0)
                if c == 'n' and len(brick_controller._orderedPublisherNames) > 5:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[5],-default_speed)
                if c == 'u' and len(brick_controller._orderedPublisherNames) > 6:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[6],default_speed)
                if c == 'j' and len(brick_controller._orderedPublisherNames) > 6:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[6],0.0)
                if c == 'm' and len(brick_controller._orderedPublisherNames) > 6:
                    brick_controller.send_data(brick_controller._orderedPublisherNames[6],-default_speed)
        shutdown()

def shutdown():
    print("\nShutting down...")

    # Shutdown ROS2
    rclpy.shutdown()

    # Exit the application
    exit()

try: args
except: args = None

if args is None:
    parser, args, leftover_args = createArgumentParser()


init = init_app(
    name=__name__,
    scenes=[('buildScene', '1')],
    autoStepping=True
)
