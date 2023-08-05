import os
import sys
import time

try:
    import gym
    from gym import spaces
except ImportError:
    print("Could not find gym")
    sys.exit(42)

import numpy as np

import agx
import agxIO
import agxOSG
import agxSDK
import agxOSG
import agxPython
from . import locateBrickRootFromEnvironment, init as brick_init, registerAgxSimulation, unregisterAgxSimulation, getRegisteredAgxSimulation

from agxPythonModules.utils.environment import create_or_set_script_context, simulation as get_context_simulation, \
                                               application as get_context_application

class ExitException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


# TODO: This should be imported from agxPythonModules.utils.environment instead
def get_script_context_type():
    sm = agxPython.ScriptManager.instance()
    sci = sm.getScriptContext()
    return sci.getType() if sci is not None else None


def create_gym_space(observations_or_actions):
    from Brick.Math import Vec3
    import Brick
    _ = Brick.MachineLearning.ReinforcementLearning.Action.ContinuousAction

    low = []
    high = []
    for s in observations_or_actions:
        signal = s.GetSignal()
        if signal is None:
            continue
        if type(signal.GetData()) == float:
            n = 1
        elif type(signal.GetData()) == Vec3:
            n = 3
        for _ in range(n):
            low.append(s.MinValue)
            high.append(s.MaxValue)
    return spaces.Box(np.array(low), np.array(high), dtype=np.float32)


def find_brick_sim_name(name):
    for i in range(5):
        try_name = name + str(i)
        if getRegisteredAgxSimulation(try_name) is None:
            return try_name
    raise Exception("Could not find an available name to register the AGX simulation")


class BrickGymEnv(gym.Env):
    '''
    This is the environment. So it loads the entire Brick Scene.

    Right now the it is only assumed to be one agent per environment.
    '''
    metadata = {'render.modes': ['human']}

    def __init__(self, file_path, model_name):
        super().__init__()
        # TODO: Possible that it is already initialized. In that case we should not clean up the initialization..
        self.init = agx.AutoInit()

        # Check if context with simulation. If created by AGXViewer we do not need to create our own
        # simulation or ExampleApplication. Or initialize Brick
        if get_script_context_type() is None or \
           get_script_context_type() == agxPython.SCRIPTCONTEXT_PYTHON:
            sim = agxSDK.Simulation()
            sim.setUniformGravity(agx.Vec3(0.0, 0.0, -9.80665))
            app = None

            # Initialize brick as in ExampleApplication::initBrickInterop
            brick_dir = locateBrickRootFromEnvironment()
            disable_python_net = os.getenv("BRICK_DISABLE_PYTHONNET") is None
            print(f"Brick dir: {brick_dir}")
            brick_init(brick_dir, "info", disable_python_net)

            self.brick_sim_name = find_brick_sim_name("env")
            registerAgxSimulation(sim, self.brick_sim_name)
            create_or_set_script_context(sim, app, None)
        elif get_script_context_type() == agxPython.SCRIPTCONTEXT_AGXVIEWER:
            sim = get_context_simulation()
            app = get_context_application()
            self.brick_sim_name = "default"

        from Brick.Physics import Component
        from Brick.AGXBrick import BrickSimulation
        from Brick import InvalidAttributeException

        self.sim = sim
        self.brickSimulation = BrickSimulation.GetSimulation(self.brick_sim_name)
        self.app = app
        self.agents = {}
        self.closed = False
        self.done = False

        self.component = Component.CreateFromFile(file_path, model_name)
        self.brickSimulation.AddComponent(self.component)
        self.brickSimulation.PositionAgxBodies()

        # Find the agent in the scene.
        # TODO: support several agents. For this we must be able to get every sub-node with
        # a given type: see https://git.algoryx.se/algoryx/brick/-/issues/241
        # aswell as handle several for observations and actions etc. Which
        # need some design choices.
        try:
            self.agent = self.component["agent"]
        except InvalidAttributeException:
            sys.exit("Exiting! No agent in the loaded component.")
        # TODO: Same as above. Want to get all parameterspaces on the type not the name
        try:
            self.parameter_space = self.component["parameterSpace"]
        except InvalidAttributeException:
            # We do not require a parameter space. So just continue
            self.parameter_space = None

        self.observation_space = create_gym_space(self.agent["observations"])
        self.action_space = create_gym_space(self.agent["actions"])

        self.max_episode_steps = self.agent["maxSteps"]
        self.steps_per_action = 1
        self.episode_step = 0
        self.sync_time = 0.0


    def init_render(self, sync_real_time=False):
        if self.app is None and get_script_context_type() != agxPython.SCRIPTCONTEXT_AGXVIEWER:
            app = agxOSG.ExampleApplication()
            app.init(agxIO.ArgumentParser([sys.executable]))
            app.setAutoStepping(False)
            # Need to reset the time step after calling initSimulation.
            # Because it will reset the timestep to 1/60
            time_step = self.brickSimulation.TimeStep
            app.initSimulation(self.sim, True)
            self.brickSimulation.SetTimeStep(time_step)
            self.app = app

            create_or_set_script_context(self.sim, app, app.getSceneRoot())

            root = self.app.getSceneRoot()
            for b in self.sim.getRigidBodies():
                agxOSG.createVisual(b, root)
            self.app.fitSceneIntoView()

            app.setEnableDebugRenderer(True)

            if sync_real_time:
                self.sync_time = time.perf_counter()

    def reset(self):
        ''' Re-position the scene. This should use the possibility to vary the initial config '''
        from Brick.Physics import ComponentLoader
        self.episode_step = 0
        self.component.UpdateParameterSpace()
        ComponentLoader.RepositionComponent(self.component)

        self.brickSimulation.ResetAgx()
        self.brickSimulation.SyncOutputParameters()
        self.sim.setTimeStamp(0.0)
        self.done = False
        if self.sync_time > 0:
            self.sync_time = time.perf_counter()

        return np.array(self.agent.GetSignalObservations(), dtype=np.float32)

    def step(self, action):
        ''' Set the action on signals and step simulation '''
        if self.app is not None:
            if self.app.done() and get_script_context_type() == agxPython.SCRIPTCONTEXT_PYTHON:
                raise ExitException("*** User has close the application")
        # This assumes that the action signal from the policy is normalized between -1.0 and 1.0.
        # The SetActionSignals method will clamp the action between -1.0, 1.0 to enforce this.
        # And then scale each action to its min and max value configured in the brick model file.
        self.agent.SetActionSignals(action, -1.0, 1.0)
        for _ in range(self.steps_per_action):
            self.brickSimulation.StepForward()
        self.episode_step += 1
        obs = np.array(self.agent.GetSignalObservations(), dtype=np.float32)
        done = self.is_state_terminal()

        reward = self.reward()
        info = {}
        return obs, reward, done, info

    def render(self, mode='human'):
        if mode == 'human':
            if self.app:
                self.app.executeOneStepWithGraphics()
                # Sync stepping against realtime
                if self.sync_time > 0:
                    sleep_time = self.sim.getTimeStamp() - (time.perf_counter() - self.sync_time)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
            else:
                self.init_render()

    def reward(self):
        ''' Child class must implement '''
        raise NotImplementedError

    def is_state_terminal(self):
        return self.episode_step >= self.max_episode_steps

    def close(self):
        ''' Close and cleanup '''
        # TODO: Crashes here after training is run... I do not understand why..
        # I cannot call agx.isShutdown or anything.. It is like import agx have been undone or something.
        if not self.closed:
            self.sim.cleanup()
            unregisterAgxSimulation(self.brick_sim_name)
            del self.init
            self.init = None
            self.closed = True

    def seed(self, seed=None):
        if self.parameter_space is not None:
            self.parameter_space.SetSeed(seed)

    def __del__(self):
        self.close()

    def set_curriculum(self, lesson_nr=0, use_last_lesson=False):
        '''Methos can be used to set curriculum learning start lesson number'''
        for currParam in self.parameter_space.CurriculumDimensions:
            if use_last_lesson:
                lesson_nr=currParam.Thresholds.Count
            currParam.LessonNumber = lesson_nr

    def update_curriculum_lesson(self, reward):
        lessons = []
        updated = False
        for currParam in self.parameter_space.CurriculumDimensions:
            lessonUpdated = currParam.TestThresholdAndUpdateLesson(reward)
            lessons += [currParam.LessonNumber]
            if lessonUpdated:
                updated = True
        return updated, lessons


class RLController(agxSDK.StepEventListener):
    def __init__(self, env: BrickGymEnv, policy):
        super().__init__()
        self.policy = policy
        self.env = env
        self.obs = self.env.reset()
        self.done = False

    def pre(self, t):
        if self.done:
            self.obs = self.env.reset()
        # calculate the action
        action = self.policy(self.obs)
        # Fake step to set the action
        self.obs, r, self.done, _ = self.env.step(action)
