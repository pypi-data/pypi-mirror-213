'''
Example on how to use Brick from Python together with AGX python bindings.
This file can be launched using python interpreter directly, or using `agxViewer`.
'''

import sys
import os
import time

import agxCollide
import agx
import agxSDK
import agxOSG
import agxRender
import agxTerrain
import agxPython
import agxIO
import agxBrick

useRos = False

try:
    import rclpy
    useRos = True
except:
   print("Cant use ros, rclpy is not imported")

from agxPythonModules.utils.environment import simulation, root, application, init_app

from brickRos2ControllerUtils import extractModelFile

def initializePlot( brickSimulation):
    from brickRos2ControllerUtils import RosPlotListener
    return RosPlotListener(brickSimulation)




def buildScene():
    # Initialize ROS
    rclpy.init()

    # Load brick model just to understand what signals there are
    from Brick.Physics import Component
    from Brick.AGXBrick import BrickSimulation
    from Brick import Path, TypePath, Model, ModelRegistry
    file_path, model_name = extractModelFile(args)
    scene = Component.CreateFromFile(file_path, model_name)
    BrickSimulation.Default.AddComponent(scene)
    plot = initializePlot(BrickSimulation.Default)
    BrickSimulation.Default.Shutdown()
    count  = 0
    while True:
        plot.update(count)
        time.sleep(1)
        count = count + 1

try: args
except: args = None

try: parser
except: parser = None
if args is None:
    parser = createArgumentParser()
    args = list(sys.argv)



init = init_app(
    name=__name__,
    scenes=[('buildScene', '1')],
    autoStepping=True
)
