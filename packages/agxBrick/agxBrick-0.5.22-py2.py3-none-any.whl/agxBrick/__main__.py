from distutils import dist
import os
import sys
import click
import logging
import coloredlogs

logger = logging.getLogger('AGXBrick')

def initLogging(level=logging.INFO):
    logging.basicConfig(level=level)
    # coloredlogs.set_level(level=numeric_level)

    # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    # logFmt = '[%(relativeCreated)d] %(levelname)6s %(message)s'
    logFmt = '[%(relativeCreated)d] %(levelname)6s %(name)2s %(message)s'
    levelStyles = dict(coloredlogs.DEFAULT_LEVEL_STYLES)
    # Check colors with `humanfriendly --demo`
    levelStyles['info'] = dict()
    levelStyles['debug'] = dict(color=247)
    levelStyles['warning'] = dict(color=208)
    fieldStyles = dict(coloredlogs.DEFAULT_FIELD_STYLES)
    fieldStyles['name'] = dict(color='cyan')
    fieldStyles['levelname'] = dict(color='magenta')
    coloredlogs.install(
        level=level,
        fmt=logFmt,
        level_styles=levelStyles,
        field_styles=fieldStyles,
    )

@click.group()
@click.option('-l', '--log', help="Log level", default='info', type=click.Choice(['verbose', 'info', 'information', 'warn', 'warning', 'error']))
def cli(log):
    '''
    AGXBrick command line tool
    '''
    numeric_level = logging.getLogger().getEffectiveLevel()
    numeric_level = getattr(logging, log.upper(), None)
    if not isinstance(numeric_level, int):
        raise click.UsageError('Invalid log level: {}'.format(log))
    initLogging(numeric_level)


def brick_config_template(name: str):
    return f"""
ModuleConfig:
  name: {name}

  import:
    Physics: {{}}
    Math:
      autoImport: true
    Scene: {{}}
    Visual: {{}}
    Simulation: {{}}
""".strip()



def brick_physics_model_template(name: str):
    return f"""
.format: 4

.import:
  Physics.Mechanics: [RigidBody, HingeAttachment, HingeConnector]

RotatedBox:
  .extends: RigidBody

  lengths:
    .type: Vec3
    .value: Vec3(0.2, 0.2, 0.2)

  geometry:
    .type: Physics.Geometry.Box
    lengths: this.lengths

  localRotation: EulerAngles.Degrees(30, 15, 0)

BoxOnPlane:
  .extends: Physics.Component

  box:
    .type: RotatedBox
    localPosition: Vec3(0, 0, 0.5)

  floor:
    .type: Physics.Geometry.Box
    lengths: Vec3(1.2, 1.2, 0.1)

""".strip()

@cli.command()
@click.argument("project-directory-path", required=True, nargs=1)
@click.option("-n", "--name")
def new(project_directory_path, name):
    '''
    Create a new AGXBrick project
    '''
    logger.info(f'Create a new project in directory: {project_directory_path}')
    name = name or os.path.basename(project_directory_path)

    if not os.path.exists(project_directory_path):
        os.makedirs(project_directory_path)

    brick_config_path = os.path.join(project_directory_path, 'brick.config.yml')
    if (os.path.exists(brick_config_path)):
        raise click.UsageError(f'Brick project config file already exists: {brick_config_path}')

    brick_config = brick_config_template(name)
    logger.info(f'Write brick project config: {brick_config_path}')
    with open(brick_config_path, 'w') as f:
        f.write(brick_config)
        f.write("\n")


    brick_example_model_path = os.path.join(project_directory_path, 'BoxOnPlane.yml')

    example_model = brick_physics_model_template(name)
    logger.info(f'Write brick example model: {brick_example_model_path}')
    with open(brick_example_model_path, 'w') as f:
        f.write(example_model)
        f.write("\n")


    dir = os.path.dirname(__file__)
    if os.path.basename(dir) == 'site-packages':
        # installed package
        dist_dir = os.path.join(dir, 'dist')
    else:
        # local dev environment
        dist_dir = os.path.join(dir, '..', '..', 'dist')

    models_dir = os.path.join(dist_dir, 'AGXBrick', 'models')

    models_symlink_path = os.path.join(project_directory_path, 'models')
    if not os.path.islink(models_symlink_path) and os.name != 'nt':
        # This should work on Windows as well, given the following:
        # https://stackoverflow.com/questions/26787872/how-to-create-symlinks-in-windows-using-python
        # > os.symlink works out of the box since python 3.8 on windows, as long as Developer Mode is turned on.
        logger.info(f'Create symlink to installed models: {models_dir} -> {models_symlink_path}')
        os.symlink(models_dir, models_symlink_path, target_is_directory=True)


rest_args = []
agx_init = None

if '--' in sys.argv:
    i = sys.argv.index('--')
    rest_args = sys.argv[i+1:]
    sys.argv = sys.argv[:i]

def buildSceneDispatch():
    from agxBrick.loadBrickModel import buildScene
    buildScene()

@cli.command()
@click.option("--model", help="The path to a brick .yml file,followed by the name of the Physics.Component to be loaded: \n example: MyModelCar.yml:Car", required=True)
@click.option("--ros2in", help="Given ros2 local_setup is sources, ros2in will subscribe to input signals over ros2. Supported Signal types: [MotorVelocityInput, MotorForceInput,LockPositionInput]", flag_value=True)
@click.option("--ros2out", help="Given ros2 local_setup is sources, ros2out will publish signals over ros2. Supported Signal types: [MotorVelocityOutput, MotorForceOutput,MotorAngleOutput, ContactDepthOutput]", flag_value=True)
@click.option("--outputContent", help="List all agx RigidBodies, Constraints, Material and ContactMaterials in the initialized simulation", flag_value=True)
@click.option("--decorate", help="Setup camera and lights declared with Brick.Scene models", flag_value=True)
@click.option("--dotgraph", help="Generate dot graphs for the loaded model. Saved in brick/dotWebView/", flag_value=True)
@click.option("--visuals", help="Create agxOSG instances for Brick.Visual models", flag_value=True)
@click.option("--batch", help="List all agx RigidBodies, Constraints, Material and ContactMaterials in the initialized simulation", type=float)
@click.option("--threads", help="Set number of threads for AGX.", type=float)
@click.option("--shaders", help="Enable Shader State. No effect unless --decorate is used", flag_value=True)
@click.option("--plot", help="Enable pyqtgraph to plot. Make sure you have pyqtgraph==0.11.0rc0 and pyside2==5.14.1.", flag_value=True)
@click.option("--print-simulation-content", help="Print the constraints, bodies and materials in the simulation", flag_value=True)
def run(model, ros2in, ros2out, outputcontent, decorate, dotgraph, visuals, batch, threads, shaders, plot, print_simulation_content):
    '''
    Run a brick simulation model
    '''
    sys.argv = [sys.argv[0].replace('__main__.py', 'loadBrickModel.py')] + sys.argv[2:] + rest_args

    import agxBrick.loadBrickModel
    from agxPythonModules.utils.environment import simulation, root, application, init_app

    # print(f'argv: {sys.argv}')

    global agx_init

    agx_init = init_app(
        name=__name__,
        scenes=[('buildSceneDispatch', '1')],
        autoStepping=True
    )

    if agx_init.exit_code != 0:
        exit(agx_init.exit_code)

# MAIN
cli()
