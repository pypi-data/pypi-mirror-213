import os

def get_agxBrick_dist_root():
    '''
    Return the root of the bundled agxBrick runtime and core models
    '''
    return os.path.join(os.path.dirname(__file__), 'dist', 'AGXBrick')


# Configure env for embedded Brick runtime
_dist_root = get_agxBrick_dist_root()

os.environ['AGXBRICK_DIST_DIR'] = _dist_root

_mp = os.getenv('BRICK_MODULEPATH')

_mp_ext = os.path.join(_dist_root, 'models', 'Brick')
if _mp:
    os.environ['BRICK_MODULEPATH'] = _mp + os.pathsep + _mp_ext
else:
    os.environ['BRICK_MODULEPATH'] = _mp_ext

from agxBrickHosting import (
    init,
    isInitialized,
    loadBrickFile,
    syncBrickInputs,
    syncBrickOutputs,
    parseBrickModelLoadingDeclaration,
    registerAgxSimulation,
    unregisterAgxSimulation,
    getRegisteredAgxSimulation,
    locateBrickRootFromEnvironment,
)
