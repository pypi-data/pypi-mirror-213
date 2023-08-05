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
from brickLoaderUtils import createArgumentParser, extractModelFilePathAndName,  printSimulationBodiesAndConstraints

def printConfig(batch):
    print("Current configuration")
    batchNames = batch.GetCurrentBatchVariableNames()
    batchValues = batch.GetCurrentBatchVariableValues()
    for i in range(len(batchNames)):
        name = batchNames[i]
        value = batchValues[i]
        print("{}: {}".format(name, value))
# Class for resetting the state of the scene with a specific time interval
class StepByStep(agxSDK.StepEventListener):
    def __init__(self, brickSimulation, model):
        super().__init__()
        self.model = model
        self.brickSimulation = brickSimulation
        self.connectorsUsed = 0

    def pre(self, time):
        from Brick.Physics import ComponentLoader

        self.model['OrderedConnectorLimit'] = self.connectorsUsed
        self.connectorsUsed = self.connectorsUsed + 1
        if self.connectorsUsed > self.model['DefinedConnectorsOrder'].Count:
            self.connectorsUsed = 0


        ComponentLoader.RepositionComponent(self.model)
        self.brickSimulation.ResetAgx()



def buildScene():
    # Make sim global to use the C# bindings to AGX all the way
    # Otherwise pythonnet migth confuse
    global sim
    from Brick.Physics import Component
    from Brick.AGXBrick import BrickSimulation
    from Brick import Path, TypePath, Model, ModelRegistry

    if sim is None:
        sim = simulation()

    if args.model == "":
        return

    file_path, model_name = extractModelFilePathAndName(args)
    scene = Component.CreateFromFile(file_path, model_name)
    #scene['LogPositioningResults'] = True
    brickSimulation = BrickSimulation.Default
    brickSimulation.AddComponent(scene)
    # All models loaded with this application
    simulation().setUniformGravity(agx.Vec3(0,0,0))

    printSimulationBodiesAndConstraints(sim)
    for geom in sim.getGeometries():
        geom.setEnableCollisions(False)
    for constraint in sim.getConstraints():
        constraint.setEnable(False)
    sbs = StepByStep(brickSimulation, scene)
    sim.add(sbs)
    agxOSG.createVisual(simulation(), root())

try: args
except: args = None

if args is None:
    parser, args, leftover_args = createArgumentParser()

sim = None

init = init_app(
    name=__name__,
    scenes=[('buildScene', '1')],
    autoStepping=True
)
