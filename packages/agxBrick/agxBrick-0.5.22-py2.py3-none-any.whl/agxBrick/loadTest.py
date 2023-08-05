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

useRos = False
rclpyIsInitialized = False
controlListenerCreated = False
plotPublisherCreated = False
try:
    import rclpy
    useRos = True
except:
   print("Cant use ros, rclpy is not imported")

from agxPythonModules.utils.environment import simulation, root, application, init_app


def printSimulationBodies():
    global sim
    for body in sim.getRigidBodies():
        print("{} # geometries.UUID: {}".format(body.getName(),body.getUuid()))
    # for body in sim.getRigidBodies():
    #     print("{} - {} # geometries.UUID: {}".format(body.getName(),body.getGeometries().Count,body.getUuid().str()))

def buildScene():
    global sim
    # Class for resetting the state of the scene with a specific time interval
    class PrintListener(agxSDK.StepEventListener):
        def __init__(self, brickSimulation):
            super().__init__()
            self.brickSimulation = brickSimulation

        def pre(self, time):
            print("hek")
            printSimulationBodies()
    from Brick.Physics import Component
    from Brick.AGXBrick import BrickSimulation
    from Brick import Path, TypePath, Model, ModelRegistry

    if sim is None:
        sim = simulation()

    scene = Component.CreateFromFile("modules/Examples/MyRobot.yml", "MyRobot")
    brickSimulation = BrickSimulation.Default
    brickSimulation.AddComponent(scene)

    printSimulationBodies()
    pl = PrintListener(brickSimulation)
    simulation().add(pl)
    agxOSG.createVisual(simulation(), root())

try: args
except: args = None

if args is None:
    args = list(sys.argv)

sim = None

init = init_app(
    name=__name__,
    scenes=[('buildScene', '1')],
    autoStepping=True
)
