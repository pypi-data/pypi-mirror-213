from brick.Core.brick_typing import ForwardRef, typechecked
from brick.ExternalModule._auto.ExternalTest._base_ExternalTest import base_ExternalTest
from brick.Physics.Component import Component
from typing import Tuple, Any, Iterable, Union, Optional, List, Set, Dict, Callable


# ExternalTest = ForwardRef('ExternalTest')

class ExternalTest(base_ExternalTest, Component):

    # Called when model is initialized
    def onInit(self):
        super().onInit()

    # Called when model is loaded
    def onLoad(self):
        super().onLoad()
