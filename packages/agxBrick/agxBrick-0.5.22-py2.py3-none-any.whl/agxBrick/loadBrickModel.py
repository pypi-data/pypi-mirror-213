'''
Example on how to use Brick from Python together with AGX python bindings.
This file can be launched using python interpreter directly, or using `agxViewer`.
'''

import sys
import os

import agxCollide
import agx
import agxUtil
import agxOSG
import agxRender
import agxTerrain
import agxPython
import agxIO
import agxBrick

enable_plotting = True

try:
    import numpy as np
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui, QtCore
except:
    enable_plotting = False

from agxPythonModules.tools.simulation_content import SimulationContent
from agxPythonModules.utils.environment import simulation, root, application, init_app
from agxBrick.brickLoaderUtils import createArgumentParser, create_visuals, setup_camera_and_lights


def buildScene():
    # Make sim global to use the C# bindings to AGX all the way
    # Otherwise pythonnet migth confuse
    global sim
    from Brick.Physics import Component
    from Brick.Simulation import DotGraphGenerator
    from Brick.AGXBrick import BrickSimulation
    from Brick import Path, TypePath, Model, ModelRegistry
    from brickLoaderUtils import extractModelFilePathAndName, setupBatch, printSimulationBodiesAndConstraints, setupPlots

    if sim is None:
        sim = simulation()

    if args.model == "":
        print('no brick model defined')
        return

    file_path, model_name = extractModelFilePathAndName(args)
    scene = Component.CreateFromFile(file_path, model_name)
    if scene is None:
        raise Exception(f'Failed to load scene')
    brickSimulation = BrickSimulation.Default

    brickSimulation.AddComponent(scene)

    if (args.dotgraph):
        DotGraphGenerator.GenerateComponentInheritanceFile(scene)
        DotGraphGenerator.GenerateComponentHierachyFile(scene)

    brickSimulation.ConnectToROS()

    # All models loaded with this application
    sim.setUniformGravity(agx.Vec3(0, 0, -9.80665))

    if hasattr( args, 'outputContent') and args.outputContent is not None and args.outputContent:
        printSimulationBodiesAndConstraints(sim)

    plot_data = None
    if args.plot and enable_plotting:
        plot_data = setupPlots(scene)
        sim.add(plot_data)

    if hasattr( args, 'batch') and args.batch is not None:
        setupBatch(args.batch,brickSimulation, sim, scene, plot_data)

    agx.setNumThreads(args.threads)

    if args.decorate:
        setup_camera_and_lights(application(), simulation(), root(), brickSimulation, scene, args.shaders)

    if args.visuals:
        create_visuals(application(), simulation(), root(), brickSimulation, scene)
    else:
        agxOSG.createVisual(sim, root())

    if args.print_simulation_content:
        content = SimulationContent(simulation=sim)
        if not content.initialize():
            return
        content.print()



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
