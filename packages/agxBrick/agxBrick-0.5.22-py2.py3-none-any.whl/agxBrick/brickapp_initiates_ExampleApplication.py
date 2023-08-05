''' Main loop in python Example - Simulation with Brick without ExampleApplication.
Demonstrates 
- how to create a basic simulation in python that can be run with either python3 or agxViewer
- how to add an ExampleApplication listener that is invoked each frame, as opposed to StepEventListener which is 
  invoked each simulation step


# brick scene:
python3 brick/python/agxBrick/brickapp_initiates_ExampleApplication.py
agxViewer --python-interpreter-mode brick/python/agxBrick/brickapp_initiates_ExampleApplication.py

# brick scene no graphics:
python3 brick/python/agxBrick/brickapp_initiates_ExampleApplication.py -a
agxViewer --python-interpreter-mode brick/python/agxBrick/brickapp_initiates_ExampleApplication.py -a

Inspired by data/python/tutorials/tutorial_independent_of_ExampleApplication.py
'''

# AGX Dynamics imports
import agx
import agxSDK
import agxPython
import agxCollide
import agxOSG
import agxIO

# Python modules
import sys
import time
import argparse

from agxPythonModules.utils.environment import simulation, root, application, create_or_set_script_context
from agxBrickHosting import registerAgxSimulation


class FrameListener(agxOSG.ExampleApplicationListener):
    def __init__(self):
        super().__init__()
        self.num_pres = 0
        self.num_posts = 0

    def preFrame(self, app):
        self.num_pres = self.num_pres + 1

    def postFrame(self, app):
        self.num_posts = self.num_posts + 1

class StepListener(agxSDK.StepEventListener):
    def __init__(self):
        super().__init__()
        self.num_pres = 0
        self.num_posts = 0

    def pre(self, _):
        self.num_pres = self.num_pres + 1

    def post(self, _):
        self.num_posts = self.num_posts + 1


def main(args):
    ap = argparse.ArgumentParser()
    ap.add_argument('--use-brickenv', action='store_true')
    args1, _ = ap.parse_known_args()
    args1 = vars(args1)

    # Creates an Example Application
    app = agxOSG.ExampleApplication()
    app.init(agxIO.ArgumentParser([sys.executable] + args))

    # Create a Simulation with example scene
    if args1['use_brickenv']:
        from brick_env import BrickEnv
        brickenv = BrickEnv()
        scene = brickenv.load_from_file("brick/Examples/DriveTrainRobot.yml", "DriveTrainRobot")
        sim = brickenv.sim
        agxOSG.createVisual(sim, app.getSceneRoot())
    else:
        from Brick.Physics import Component
        from Brick.AGXBrick import BrickSimulation
        sim = agxSDK.Simulation()
        component = Component.CreateFromFile("brick/Examples/DriveTrainRobot.yml", "DriveTrainRobot")
        registerAgxSimulation(sim, "Default")
        BrickSimulation.GetSimulation("Default").AddComponent(component)
        agxOSG.createVisual(sim, app.getSceneRoot())

    # Create the agxPyton context, so we can use for example agxPythonModules.utils.environment.simulation()
    create_or_set_script_context(sim, app, app.getSceneRoot() if app is not None else None)

    # Initialize the simulation in the application
    # TODO: True should be False if not have_graphics?
    app.initSimulation(sim, True)
    have_graphics = app.getViewer()

    frame_listener = FrameListener()
    app.addListener(frame_listener)
    step_listener = StepListener()
    sim.addEventListener(step_listener)

    num_frames = 0
    while sim.getTimeStamp() <= 5.0:
        # executeOneStep also steps simulation "sometimes", ie when simfreq >> renderfreq always, when simfreq < renderfreq sometimes.
        # If we want to throttle to match viewing realtime, then fetch messages in preFrame, and use them in StepEventListener
        if have_graphics:
            app.executeOneStepWithGraphics()
        else:
            app.executeOneStepWithoutGraphics()
        num_frames = num_frames + 1
    print(f"Executed {num_frames} frames and {sim.getClock().getFrame()} simulation steps")
    print(f"Frame listener pre invoked {frame_listener.num_pres} and post invoked {frame_listener.num_pres} times")
    print(f"Step listener pre invoked {step_listener.num_pres} and post invoked {step_listener.num_pres} times")

# Entry point when this script is loaded with python
if agxPython.getContext() is None:
    init = agx.AutoInit()
    main(sys.argv)
