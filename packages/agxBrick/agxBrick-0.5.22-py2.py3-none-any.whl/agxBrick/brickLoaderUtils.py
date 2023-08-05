import time
import math
import sys
import os
import argparse

import agxCollide
import agx
import agxSDK
import agxOSG
import agxUtil
import agxRender
import agxTerrain
import agxPython
import agxIO
import agxBrick

try:
    from agxPythonModules.utils.plot_pyqt import Window, Plot, Curve
    import pyqtgraph as pg
    pg.setConfigOptions(antialias = True)
except:
    print("pyqtgraph not found")

def createArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="", help="The path to a brick .yml file,followed by the name of the Physics.Component to be loaded: \n example: MyModelCar.yml:Car" )
    parser.add_argument('--ros2in', dest='ros2in', action='store_true', help="Given ros2 local_setup is sources, ros2in will subscribe to input signals over ros2. Supported Signal types: [MotorVelocityInput, MotorForceInput,LockPositionInput]" )
    parser.add_argument('--ros2out', dest='ros2out', action='store_true', help="Given ros2 local_setup is sources, ros2out will publish signals over ros2. Supported Signal types: [MotorVelocityOutput, MotorForceOutput,MotorAngleOutput, ContactDepthOutput]" )
    parser.add_argument('--outputContent', dest='outputContent', action='store_true', help="List all agx RigidBodies, Constraints, Material and ContactMaterials in the initialized simulation" )
    parser.add_argument('--decorate', dest='decorate', action='store_true', help="Setup camera and lights" )
    parser.add_argument('--dotgraph', dest='dotgraph', action='store_true', help="Generate dot graphs for the loaded model. Saved in brick/dotWebView/" )
    parser.add_argument('--visuals', dest='visuals', action='store_true', help="Create visuals according to declaration" )
    parser.add_argument('--batch', type=float, help="Run a Batch for the current BatchVariables on scene root level" )
    parser.add_argument('--threads', dest='threads', type=int,default=2, help="num threads for AGX application." )
    parser.add_argument('--shaders', dest='shaders', action='store_true', help="Enable Shader State. No effect unless --decorate is used" )
    parser.add_argument('--plot', dest='plot', action='store_true', help="Enable pyqtgraph to plot. Make sure you have pyqtgraph==0.11.0rc0 and pyside2==5.14.1." )
    parser.add_argument("--print-simulation-content", dest='print_simulation_content', action='store_true', help="Print the constraints, bodies and materials in the simulation")

    args, unknown_args = parser.parse_known_args()
    return parser, args, unknown_args

def extractModelFilePathAndName(args):
    # Take first two arguments as model file and model name
    file_name = None
    model_name = None
    brick_dir = os.getcwd() # os.getenv('BRICK_DIR')
    file_path = None
    if args.model is not None:
        print(args.model)
        model_arg = args.model
        model_args = model_arg.split(':')

        if len(model_args) > 2 or len(model_args) == 0:
            return
        file_name = model_args[0]
        #filepath = f'{os.path.dirname(__file__)}/{file_name}'
        file_path = f'{brick_dir}/{file_name}'
        if len(model_args) == 2:
            model_name = model_args[1]
        else:
            model_name = ""
    else:
        raise Exception("No brick model specified")

    return file_path, model_name


def printConfig(batch):
    print("Current configuration")
    batchNames = batch.GetCurrentBatchVariableNames()
    batchValues = batch.GetCurrentBatchVariableValues()
    for i in range(len(batchNames)):
        name = batchNames[i]
        value = batchValues[i]
        print("{}: {}".format(name, value))


def getConstraintType(constraint):
    if constraint.asPrismatic():
        return "Prismatic"
    if constraint.asHinge():
        return "Hinge"
    if constraint.asCylindricalJoint():
        return "Cylindrical"
    if constraint.asBallJoint():
        return "Ball"
    if constraint.asLockJoint():
        return "Lock"
    return "unknown"

def printSimulationBodiesAndConstraints(sim):
    for body in sim.getRigidBodies():
        print("{} - {} # geometries.UUID: {}".format(body.getName(),len(body.getGeometries()),body.getUuid()))

    for constraint in sim.getConstraints():
        if constraint.getBodyAt(0) != None:
            b1n = constraint.getBodyAt(0).getName()
            b2n = ""
            if constraint.getBodyAt(1) != None:
                b2n = constraint.getBodyAt(1).getName()
            print("{} -Type: {}. Bodies: {}, {}".format(constraint.getName(),getConstraintType(constraint), b1n, b2n))
    for m in sim.getMaterialManager().getMaterialVector():
        print("M: {}, uuid: {}".format(m.getName(),m.getUuid()))
    for cm in sim.getMaterialManager().getContactMaterialVector():
        m1 = cm.getMaterial1()
        m2 = cm.getMaterial2()
        print(cm)
        print("M1: {} M2: {},  uuid1: {}, uuid2: {}, uuid: {}, y: {}".format(m1.getName(),m2.getName(),m1.getUuid(),m2.getUuid(), cm.getUuid(),cm.getYoungsModulus()))

class DataCurve():
    def __init__(self, plot, name: str) -> None:
        self.curve = plot.createCurve( name )
        self.x = []
        self.y = []

class SignalCurve():
    def __init__(self, plot, signal, name) -> None:
        self.data_curves = []
        self.signal = signal
        data = self.signal.GetData()
        if isinstance(data, float):
            dc = DataCurve(plot, name)
            self.data_curves.append(dc)
        elif data._ModelPath.Str == "Math.Vec3":
            dc = DataCurve(plot, name + "_X" )
            self.data_curves.append(dc)
            dc = DataCurve(plot, name + "_Y" )
            self.data_curves.append(dc)
            dc = DataCurve(plot, name + "_Z" )
            self.data_curves.append(dc)


    def append_data(self, time):

        data = self.signal.GetData()
        data_vector = []
        if isinstance(data,float):
            data_vector.append(data)
        elif data._ModelPath.Str == "Math.Vec3":
            data_vector.append(data.X)
            data_vector.append(data.Y)
            data_vector.append(data.Z)

        i = 0
        assert len(self.data_curves) == len(data_vector)
        for dc in self.data_curves:
            dc.x.append(time)
            dc.y.append(data_vector[i])
            dc.curve.setData(dc.x, dc.y)
            i = i + 1


class PlotData(agxSDK.StepEventListener):
    def __init__(self, scene) -> None:
        super().__init__(agxSDK.StepEventListener.LAST_STEP)
        self.curves = []
        self.allCurves = []
        self.sortedSensors = self.sortSensors(scene)
        self.sortedSignals = self.sortSignals(scene)
        self.plots = {}
        self.window = None
        self.previousStartTime = 0
        self.updatePlots()


    def last(self, t):
        for sensor_curve in self.curves:
            x = t - self.previousStartTime
            sensor_curve.append_data(x)



    def updatePlot(self, modelPath, time):

        if self.window is None:
            self.window = Window( title = "Sensor Data",
                            closeWhenRemoved = True )
            self.window.graphicsWindow.setBackground('w')

        if self.sortedSensors is not None and modelPath in self.sortedSensors:
            sensors = self.sortedSensors[modelPath]
            if self.window.isValid:
                plot = None

                if modelPath in self.plots:
                    plot = self.plots[modelPath]
                else:
                    plot = self.window.createPlot( title  = modelPath,
                                                    units  = ( 's', '?' ),
                                                    labels = ( 'Time', '?' ) )
                    self.plots[modelPath] = plot

                for sensor in sensors:
                    name = sensor["name"] + "{}".format(time)

                    sensor_curve = SignalCurve(plot, sensor.GetOrCreateSignal(), name)
                    self.curves.append(sensor_curve)
                    self.allCurves.append(sensor_curve)

        if self.sortedSignals is not None and modelPath in self.sortedSignals:
            signals = self.sortedSignals[modelPath]
            if self.window.isValid:
                plot = None

                if modelPath in self.plots:
                    plot = self.plots[modelPath]
                else:
                    plot = self.window.createPlot( title  = modelPath,
                                                    units  = ( 's', '?' ),
                                                    labels = ( 'Time', '?' ) )
                    self.plots[modelPath] = plot

                for signal in signals:
                    name = signal["name"] + "{}".format(time)

                    signal_curve = SignalCurve(plot, signal, name)
                    self.curves.append(signal_curve)
                    self.allCurves.append(signal_curve)
        return

    def sortSensors(self, scene):
        from Brick import InvalidAttributeException
        sensors = None
        try:
            sensors = scene['plotSensors']
        except InvalidAttributeException:
            return None

        sortedSensors = {}
        for sensor in sensors:
            signal = sensor.GetOrCreateSignal()
            modelPath = signal._ModelPath.Path.ToString()
            if modelPath not in sortedSensors:
                sortedSensors[modelPath] = []
            sortedSensors[modelPath].append(sensor)
        return sortedSensors

    def sortSignals(self, scene):
        from Brick import InvalidAttributeException
        signals = None
        try:
            signals = scene['plotSignals']
        except InvalidAttributeException:
            return None

        sortedSignals = {}
        for signal in signals:
            modelPath = signal._ModelPath.Path.ToString()
            if modelPath not in sortedSignals:
                sortedSignals[modelPath] = []
            sortedSignals[modelPath].append(signal)
        return sortedSignals  

    def updatePlots(self, time = 0):
        if self.sortedSignals is not None or self.sortedSensors is not None:
            self.curves.clear()
            if self.sortedSensors is not None:
                for modelPath in self.sortedSensors:
                    self.updatePlot(modelPath, time)
                self.previousStartTime = time
            if self.sortedSignals is not None:
                for modelPath in self.sortedSignals:
                    self.updatePlot(modelPath, time)
                self.previousStartTime = time

def setupPlots(scene):

    plot_data = PlotData(scene)
    return plot_data

def setupBatch(iteration_time,brickSimulation, sim, scene, plot_data):

    # if t is None or scene.GetNumBatchConfigurations() < 2:
    #     return
    if iteration_time is None:
        return
    msu = ModelStateUpdate(brickSimulation.Default, scene, iteration_time, plot_data)
    sim.add(msu)


def set_visual(sim, agxGeometry, root, diffuse_color: agx.Vec4f, specular_color: agx.Vec4f, ambient_color: agx.Vec4f, set_color: bool, texture_path = None):
    g = None

    uuid = agxGeometry.getUuid()
    g = sim.getGeometry(agx.Uuid(str(uuid)))

    osgNode = agxOSG.createVisual(g, root)
    if texture_path is not None and texture_path != "":
        agxOSG.setTexture(g, root, texture_path )
    if set_color:
        agxOSG.setDiffuseColor(osgNode, diffuse_color)
        agxOSG.setSpecularColor(osgNode, specular_color)
        agxOSG.setAmbientColor(osgNode, ambient_color)

def get_parent_body(brick_simulation, brick_node):
    import Brick
    from Brick import Physics
    # Some (PythonNet?) bug make MassProperties3D lack .Parent attribute
    try:
       brick_node.Parent
    except AttributeError:
        return None
    if brick_node.Parent is None:
        return None
    if isinstance(brick_node.Parent, Brick.Visual.Shape):
        return None # Will not suport Visuals in Visuals for now

    if isinstance(brick_node.Parent, Brick.Physics.Mechanics.RigidBody):
        return brick_simulation.GetAgxBody(brick_node.Parent)

    if isinstance(brick_node.Parent, Brick.Physics.Geometry):
        agxGeom = brick_simulation.GetAgxGeometry(brick_node.Parent)
        if agxGeom is None:
            return None
        return agxGeom.getRigidBody()

# Assuming the node is a Brick.Visual.Shape
# If the Parent is not a Geometry, we assume it is a RigidBody
# If it is a geometry, the transform is actually the combination of two transforms
def get_local_transform(brick_node):
    import Brick
    from Brick import Physics
    a4x4 = agx.AffineMatrix4x4()
    p = brick_node.LocalTransform.Position
    a4x4.setTranslate(p.X, p.Y, p.Z)
    r = brick_node.LocalTransform.Rotation
    a4x4.setRotate(agx.Quat(r.X,r.Y,r.Z,r.W))
    ## Includ the transform from Geometry to Body
    if brick_node.Parent.__class__ is Brick.Physics.Geometry:
        a4x4_2 = agx.AffineMatrix4x4()
        p = brick_node.Parent.LocalTransform.Position
        a4x4_2.setTranslate(p.X, p.Y, p.Z)
        r = brick_node.Parent.LocalTransform.Rotation
        a4x4_2.setRotate(agx.Quat(r.X,r.Y,r.Z,r.W))
        a4x4 = a4x4 * a4x4_2
    return a4x4

def append_visual_to_agx(sim: agxSDK.Simulation, root: agxOSG.GeometryNode, agxGeometry: agxCollide.Geometry, agxRigidBody: agx.RigidBody, brick_visual):
    agxGeometry.setEnableCollisions(False)
    relative_transform = get_local_transform(brick_visual)
    sim.add(agxGeometry)
    if agxRigidBody is not None:
        agxGeometry.setSensor(True)
        uuid = agxRigidBody.getUuid()
        rb = sim.getRigidBody(agx.Uuid(uuid.str()))
        rb.add(agxGeometry, relative_transform)
    else:
        agxGeometry.setTransform(relative_transform)
    color = brick_visual["color"]
    texture_path = brick_visual["texture"]
    if texture_path is not None and texture_path != '':
        texture_path = brick_visual.AbsoluteTextureFilepath
    op = 1
    onlyColor = agx.Vec4f(color.X,color.Y,color.Z,op)
    set_visual(sim, agxGeometry, root, onlyColor, onlyColor, onlyColor, True, texture_path)

### We would here like to ask the Brick Model if it at some level extends Physics.Geometry
### Instead we check the model path, and know which models that we exist, for the moment
def is_geometry(node):
    model_path = node._ModelPath.Path.ToString()
    words = model_path.split(".")
    if len(words) < 2:
        return False
    # All Physics.Geometry + some special AGXBrick geometries are counted as geometries
    return (words[0] == "Physics" and words[1] == "Geometry") or (words[0] == "AGXBrick" and ("Decomposed" in words[1] or "SurfaceVelocity" in words[1]))

def enable_light(decorator: agxOSG.SceneDecorator, brick_decorator, shadow_light, idx: int, light_enum):
    decorator.setEnableCalculateLightPositions(light_enum, False)
    light = decorator.getLightSource(light_enum)
    p1 = brick_decorator.Lights[idx].Position
    light.setPosition(agx.Vec4(p1.X, p1.Y, p1.Z, 0))
    if shadow_light is None and brick_decorator.Lights[idx].GenerateShadow:
        shadow_light = light_enum
    return shadow_light

def setup_lights(app: agxOSG.ExampleApplication, sim: agxSDK.Simulation, root: agxOSG.GeometryNode, brick_decorator, shader_state):
    decorator = app.getSceneDecorator()
    bc1 = brick_decorator.BackgroundColor1
    c1 = agx.Vec4f(bc1.X, bc1.Y, bc1.Z, 1)
    bc2 = brick_decorator.BackgroundColor2
    c2 = agx.Vec4f(bc2.X, bc2.Y, bc2.Z, 1)
    decorator.setBackgroundColor(c1, c2)

    shadow_light = None
    num_lights = brick_decorator.Lights.Count
    # First we find how many lights we should use
    # At least one is required
    mask = agxOSG.SceneDecorator.LIGHT0
    if num_lights > 1:
        mask = mask + agxOSG.SceneDecorator.LIGHT1
    if num_lights > 2:
        mask = mask + agxOSG.SceneDecorator.LIGHT2
    # We must set enable all lights just once.
    decorator.setEnableLights( mask )

    # now we enable them one by one according to the brick_decorator
    if num_lights > 0:
        shadow_light = enable_light(decorator, brick_decorator, shadow_light, 0, agxOSG.SceneDecorator.LIGHT0)
    if num_lights > 1:
        shadow_light = enable_light(decorator, brick_decorator, shadow_light, 1, agxOSG.SceneDecorator.LIGHT1)
    if num_lights > 2:
        shadow_light = enable_light(decorator, brick_decorator, shadow_light, 2, agxOSG.SceneDecorator.LIGHT2)

    if shadow_light is not None:
        decorator.setEnableShadows(True)
        decorator.setShadowLightSource(shadow_light)
        decorator.setShadowMethod(agxOSG.SceneDecorator.SOFT_SHADOWMAP)
        decorator.setEnableShaderState(shader_state)
    else:
        decorator.setEnableShadows(False)



def setup_camera(app: agxOSG.ExampleApplication, brick_camera):
    cameraData = app.getCameraData()
    cameraData.nearClippingPlane = brick_camera.Clip.Near
    cameraData.farClippingPlane = brick_camera.Clip.Far
    cameraData.eye = agx.Vec3(brick_camera.Eye.X, brick_camera.Eye.Y, brick_camera.Eye.Z)
    cameraData.center = agx.Vec3(brick_camera.Center.X, brick_camera.Center.Y, brick_camera.Center.Z)
    cameraData.up = agx.Vec3(brick_camera.Up.X, brick_camera.Up.Y, brick_camera.Up.Z)
    cameraData.fieldOfView = brick_camera.FieldOfView
    app.applyCameraData(cameraData)
    app.setCameraHome(cameraData.eye, cameraData.center, cameraData.up)

def setup_camera_and_lights(app: agxOSG.ExampleApplication, sim: agxSDK.Simulation, root: agxOSG.GeometryNode, brick_simulation, brick_node, shader_state):
    import Brick

    # Some (PythonNet?) bug make some Scene.Node's lack .Children attribute
    try:
        brick_node.Children
    except AttributeError:
        return

    for child in brick_node.Children:

        if isinstance(child, Brick.Scene.SceneDecorator):
            setup_lights(app, sim, root, child, shader_state)
            continue
        if isinstance(child, Brick.Scene.Camera):
            setup_camera(app, child)
            continue

def create_visuals(app: agxOSG.ExampleApplication, sim: agxSDK.Simulation, root: agxOSG.GeometryNode, brick_simulation, brick_node):
    import Brick
    default_color = agx.Vec4f(0.5,0.5,0.5,1)

    # Some (PythonNet?) bug make some Scene.Node's lack .Children attribute
    try:
        brick_node.Children
    except AttributeError:
        return

    for child in brick_node.Children:

        create_visuals(app, sim, root, brick_simulation, child )
        parent_body = get_parent_body(brick_simulation, child)
        if is_geometry(child):
            agxGeometry = None
            try:
                agxGeometry = brick_simulation.GetAgxGeometry(child)
            except Exception as e:
                assert False, "The Brick Geometry could not be found in AGX"

            diffuse_color = default_color
            specular_color = default_color
            ambient_color = default_color
            set_color = False
            texture_path = None
            if child["renderMaterial"] is not None:
                set_color = True
                dc = child["renderMaterial"]["diffuseColor"]
                sc = child["renderMaterial"]["specularColor"]
                ac = child["renderMaterial"]["ambientColor"]
                op = child["renderMaterial"]["opacity"]
                if child["renderMaterial"]["texture"] != "":
                    texture_path =child["renderMaterial"].AbsoluteTextureFilepath
                diffuse_color = agx.Vec4f(dc.X,dc.Y,dc.Z,op)
                specular_color = agx.Vec4f(sc.X,sc.Y,sc.Z,op)
                #emerssive_color = agx.Vec4f(ec.X,ec.Y,ec.Z,op)
                ambient_color = agx.Vec4f(ac.X,ac.Y,ac.Z,op)
            ## Lets create visual if it had render material, or it is an external geometry
            if (set_color or child["externalReference"] != None):
                set_visual(sim, agxGeometry, root, diffuse_color, specular_color, ambient_color, set_color, texture_path)
        if isinstance(child, Brick.Visual.Sphere):
            bv_sphere = agxCollide.Geometry(agxCollide.Sphere(child.Radius))
            append_visual_to_agx(sim, root, bv_sphere, parent_body, child)
        elif isinstance(child, Brick.Visual.Box):
            bv_box = agxCollide.Geometry(agxCollide.Box(child.Lengths.X*0.5,child.Lengths.Y*0.5,child.Lengths.Z*0.5))
            append_visual_to_agx(sim, root, bv_box, parent_body, child)
        elif isinstance(child,Brick.Visual.Cylinder):
            bv_cylinder = agxCollide.Geometry(agxCollide.Cylinder(child.Radius,child.Length))
            append_visual_to_agx(sim, root, bv_cylinder, parent_body, child)
        elif isinstance(child,Brick.Visual.File):
            scale = agx.Matrix3x3(1,0,0,0,1,0,0,0,1)
            try:
                s = child["scaling"]
                scale = agx.Matrix3x3(s.X,0,0,0,s.Y,0,0,0,s.Z)
            except Exception as e:
                pass
            tm = agxCollide.Trimesh.REMOVE_DUPLICATE_VERTICES
            mesh = agxUtil.createTrimesh(child.AbsoluteFilepath,tm, scale)
            bv_trimesh =  agxCollide.Geometry(mesh)

            append_visual_to_agx(sim, root, bv_trimesh, parent_body, child)

# Class for resetting the state of the scene with a specific time interval
class ModelStateUpdate(agxSDK.StepEventListener):
    def __init__(self, brickSimulation, batchModel, batchTime, plot_data):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE)
        self.batch = batchModel
        self.plot_data = plot_data
        printConfig(self.batch)
        self.brickSimulation = brickSimulation
        self.iterationLength = batchTime
        self.iterationsDone = 1

    def preCollide(self, time):
        from Brick.Physics import ComponentLoader

        if time > self.iterationsDone * self.iterationLength:

            self.batch.UpdateBatchConfiguration()
            self.batch.UpdateParameterSpace()
            printConfig(self.batch)

            ComponentLoader.RepositionComponent(self.batch)
            self.brickSimulation.ResetAgx()
            # Update sensor outputs accordig to new state
            self.brickSimulation.SyncOutputParameters()
            self.iterationsDone = self.iterationsDone + 1
            if self.plot_data is not None:
                self.plot_data.updatePlots(time)

class InputSignalCallback():
    def __init__(self, signal):
        self.signal = signal

    def callback_set_float(self, msg):
        print("Setting data: {}".format(msg.data))
        self.signal.SetData(msg.data)


class OutputSignalCallback():
    def __init__(self, plotData, index):
        self.plotData = plotData
        self.index = index

    def callback_get_float(self, msg):
        print("Plotting data: {}".format(msg.data))
        self.plotData[self.index].append( msg.data)
        #Last 100 values
        self.plotData[self.index] = self.plotData[self.index][-100:]
