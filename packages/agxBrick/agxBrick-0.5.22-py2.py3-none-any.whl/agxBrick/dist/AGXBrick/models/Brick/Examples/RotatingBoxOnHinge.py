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
import agxPython
import agxIO
import agxBrick

from agxPythonModules.utils.environment import simulation, root, application, init_app

def buildScene():
    from Brick.Physics import Component
    from Brick.AGXBrick import BrickSimulation
    from Brick import Path, TypePath, Model, ModelRegistry

    filepath = f'{os.path.dirname(__file__)}/RotatingBoxOnHinge.yml'
    # scene = Component.CreateFromPath(TypePath('Examples.RotatingBoxOnHinge'))
    scene = Component.CreateFromFile(filepath, 'RotatingBoxOnHinge')
    BrickSimulation.Default.AddComponent(scene)
    boxBody = simulation().getRigidBodies()[0]
    boxBody.setPosition(1, 0, 0)
    agxOSG.createVisual(simulation(), root())


init = init_app(
    name=__name__,
    scenes=[('buildScene', '1')],
    autoStepping=True
)
