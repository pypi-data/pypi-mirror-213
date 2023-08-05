# from __future__ import annotations
import os, sys
import logging
import importlib

from typing import Tuple, Any, Iterable, Union, Optional, Callable
from typing import List as tList
from typing import Dict as tMap
from typing import Set as tSet

from brick.Core.brick_typing import ForwardRef, typechecked
from brick.Core.ModelBase import getModelPath

logger = logging.getLogger('Brick.Model.Instance')

# Forward declaration for self


from brick.Core import Model, Path, TypePath, BaseInstance, InstanceMeta, toDict
from brick.Core import List, Map, Set, Timestamp

from brick.Physics._auto.Component.Component._base_Component import base_Component





class base_ExternalTest(base_Component, metaclass=type):

    """TODO: Documentation for ExternalModule.ExternalTest


    """

    _activeValueGetters = None

    ### Attributes ###

    # foo
    _foo_Fn = None
    _foo = None

    @property
    @typechecked
    def foo(self) -> Optional[int]:
        """No description"""
        if self._foo is None and (self._foo_Fn or not self._isDefault):
            if self._activeValueGetters is None:
                self._activeValueGetters = set()

            if 'foo' in self._activeValueGetters:
                raise Exception(f'[{id(self)}] Circular getter loop for foo, visited: {self._activeValueGetters}')
            self._activeValueGetters.add('foo')
            if not self._foo_Fn:
                raise Exception(f'[{id(self)}] foo is undefined (type: Int)')

            try:
                self._foo = self._foo_Fn(self)
            except Exception as e:
                if self._isDefault:
                    self.logWarn(f'Ignoring failed default value function for foo')
                else:
                    raise
            self._registerValue('foo', self._foo)
            self._activeValueGetters.remove('foo')

        return self._foo


    @foo.setter
    @typechecked
    def foo(self, val: Union[int, Callable]):
        if callable(val):
            self._foo_Fn = val
            self._foo = None
        else:
            def valFn(self): return val
            self._foo_Fn = valFn
            self._foo = val
            self._registerValue('foo', self._foo)




    def _diff(self, rhs):
        d = super()._diff(rhs)

        if self._foo != rhs._foo:
            d['foo'] = {'new': self._foo, 'old': rhs._foo}
        return d


    def _initDefaultValueFunctions(self, **kwargs):

        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        import brick.Core
        _DataBinding = importlib.import_module('brick.Core.DataBinding')
        _EulerAngles = importlib.import_module('brick.Core.EulerAngles')
        _Geometry_Frame = importlib.import_module('brick.Geometry.Frame.Frame')
        _Geometry_Transform = importlib.import_module('brick.Geometry.Transform.Transform')
        _Physics_Component = importlib.import_module('brick.Physics.Component.Component')
        _Physics_Connector = importlib.import_module('brick.Physics.Connector.Connector')
        _Vec3 = importlib.import_module('brick.Math.Vec3')


        from brick.Core.Model import StringModel, IntModel, RealModel, BoolModel
        from brick.Core.Model import ListModel, MapModel, SetModel, EnumModel, PathModel, TimestampModel, AnyModel
        # NOTE: We must handle parent
        # Make sure parent is not evaluated twice, __init__.super() and super call here as well
        super()._initDefaultValueFunctions(**kwargs)



        self._foo_Fn = None




    # NOTE: Using key-word only arguments for now
    # https://www.python.org/dev/peps/pep-3102/

    # @typechecked
    def __init__(self,*,

        connectors=None,

        dataBindings=None,

        foo=None,

        frame=None,

        isPlaced=None,

        name=None,

        wantInternalPositioning=None,

        **kwargs
    ):


        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        import brick.Core
        _DataBinding = importlib.import_module('brick.Core.DataBinding')
        _EulerAngles = importlib.import_module('brick.Core.EulerAngles')
        _Geometry_Frame = importlib.import_module('brick.Geometry.Frame.Frame')
        _Geometry_Transform = importlib.import_module('brick.Geometry.Transform.Transform')
        _Physics_Component = importlib.import_module('brick.Physics.Component.Component')
        _Physics_Connector = importlib.import_module('brick.Physics.Connector.Connector')
        _Vec3 = importlib.import_module('brick.Math.Vec3')


        attribute = kwargs.get('_attribute', None)
        skipLoad = kwargs.get('_skipLoad', False)
        skipInit = kwargs.get('_skipInit', False)
        skipArgs = kwargs.get('_skipArgs', False)
        skipArgSync = kwargs.get('_skipArgSync', False)
        self._isDefault = kwargs.get('_isDefault', False)
        superKwArgs = dict(kwargs)
        superKwArgs['_skipInit'] = True
        superKwArgs['_skipLoad'] = True
        super().__init__(**superKwArgs)

        self._initDefaultValueFunctions(**kwargs)

        if not skipArgs:
            self._registerMutations = kwargs.get('_registerMutations', True)


            if connectors is not None:
                self.connectors = connectors
            if dataBindings is not None:
                self.dataBindings = dataBindings
            if foo is not None:
                self.foo = foo
            if frame is not None:
                self.frame = frame
            if isPlaced is not None:
                self.isPlaced = isPlaced
            if name is not None:
                self.name = name
            if wantInternalPositioning is not None:
                self.wantInternalPositioning = wantInternalPositioning

            self._registerMutations = False

        if not skipInit:
            self._init()

        if not skipLoad and not self._isDefault:
            self._load()

    @classmethod
    def new(cls) -> 'ExternalTest':
        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        return _ExternalModule_ExternalTest.ExternalTest(_skipInit=True, _skipLoad=True, _skipArgs=True)

    def _validate(self):

        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        import brick.Core
        _DataBinding = importlib.import_module('brick.Core.DataBinding')
        _EulerAngles = importlib.import_module('brick.Core.EulerAngles')
        _Geometry_Frame = importlib.import_module('brick.Geometry.Frame.Frame')
        _Geometry_Transform = importlib.import_module('brick.Geometry.Transform.Transform')
        _Physics_Component = importlib.import_module('brick.Physics.Component.Component')
        _Physics_Connector = importlib.import_module('brick.Physics.Connector.Connector')
        _Vec3 = importlib.import_module('brick.Math.Vec3')

        # Make sure constructor was not inherited (trying to prevent user code before onLoad callback)
        if type(self).__init__ != base_ExternalTest.__init__:
            raise Exception(f'[{self._idStr}] Must not overload `__init__` for ExternalModule.ExternalTest')




        if self._connectors_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `connectors`')


        if self.connectors is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `connectors`')


        if self.connectors is not None and not isinstance(self.connectors, (Map, dict)):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.connectors)}` ({type(self.connectors).__name__}), expected `Map<String, Physics.Connector>`')



        if self._dataBindings_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `dataBindings`')



        if self.dataBindings is not None and not isinstance(self.dataBindings, (List, list)):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.dataBindings)}` ({type(self.dataBindings).__name__}), expected `List<DataBinding>`')



        if self._foo_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `foo`')


        if self.foo is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `foo`')


        if self.foo is not None and not isinstance(self.foo, int):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.foo)}` ({type(self.foo).__name__}), expected `Int`')



        if self._frame_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `frame`')


        if self.frame is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `frame`')


        if self.frame is not None and not isinstance(self.frame, _Geometry_Frame.Frame):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.frame)}` ({type(self.frame).__name__}), expected `Geometry.Frame`')



        if self._isPlaced_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `isPlaced`')



        if self.isPlaced is not None and not isinstance(self.isPlaced, bool):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.isPlaced)}` ({type(self.isPlaced).__name__}), expected `Bool`')



        if self._name_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `name`')


        if self.name is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `name`')


        if self.name is not None and not isinstance(self.name, str):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.name)}` ({type(self.name).__name__}), expected `String`')



        if self._wantInternalPositioning_Fn is None:
            raise Exception(f'[{self._idStr}] Missing required attribute `wantInternalPositioning`')



        if self.wantInternalPositioning is not None and not isinstance(self.wantInternalPositioning, bool):
            raise Exception(f'[{self._idStr}] Unexpected type `{getModelPath(self.wantInternalPositioning)}` ({type(self.wantInternalPositioning).__name__}), expected `Bool`')




    def _init(self, **kwargs):
        if self._isInitialized:
            raise Exception(f'[{self._idStr}] Instance is already initialized')

        # Initialize child attributes

        if self.connectors is not None and isinstance(self.connectors, BaseInstance) and not self.connectors._isInitialized:
            self.connectors._init(**kwargs)

        if self.dataBindings is not None and isinstance(self.dataBindings, BaseInstance) and not self.dataBindings._isInitialized:
            self.dataBindings._init(**kwargs)

        if self.foo is not None and isinstance(self.foo, BaseInstance) and not self.foo._isInitialized:
            self.foo._init(**kwargs)

        if self.frame is not None and isinstance(self.frame, BaseInstance) and not self.frame._isInitialized:
            self.frame._init(**kwargs)

        if self.isPlaced is not None and isinstance(self.isPlaced, BaseInstance) and not self.isPlaced._isInitialized:
            self.isPlaced._init(**kwargs)

        if self.name is not None and isinstance(self.name, BaseInstance) and not self.name._isInitialized:
            self.name._init(**kwargs)

        if self.wantInternalPositioning is not None and isinstance(self.wantInternalPositioning, BaseInstance) and not self.wantInternalPositioning._isInitialized:
            self.wantInternalPositioning._init(**kwargs)


        self.onInit(**kwargs)
        self._isInitialized = True


    def _load(self, **kwargs):
        if self._isLoaded:
            raise Exception(f'[{self._idStr}] Instance is already loaded')




        # Load child attributes

        if self.connectors is not None and isinstance(self.connectors, BaseInstance) and not self.connectors._isLoaded:
            self.connectors._load(**kwargs)

        if self.dataBindings is not None and isinstance(self.dataBindings, BaseInstance) and not self.dataBindings._isLoaded:
            self.dataBindings._load(**kwargs)

        if self.foo is not None and isinstance(self.foo, BaseInstance) and not self.foo._isLoaded:
            self.foo._load(**kwargs)

        if self.frame is not None and isinstance(self.frame, BaseInstance) and not self.frame._isLoaded:
            self.frame._load(**kwargs)

        if self.isPlaced is not None and isinstance(self.isPlaced, BaseInstance) and not self.isPlaced._isLoaded:
            self.isPlaced._load(**kwargs)

        if self.name is not None and isinstance(self.name, BaseInstance) and not self.name._isLoaded:
            self.name._load(**kwargs)

        if self.wantInternalPositioning is not None and isinstance(self.wantInternalPositioning, BaseInstance) and not self.wantInternalPositioning._isLoaded:
            self.wantInternalPositioning._load(**kwargs)


        # Evaluating bindings
        self._evaluateBindings()

        # Validate structure
        self._validate()

        # TODO: Explicitly call parent.onLoad, or assume `super().onLoad()` is called from implementation?
        self.onLoad(**kwargs)

        # Store post-loaded state for changeset calculations
        # self._oldState = self._clone({})
        self._isLoaded = True


    def _clone(self, cloned):

        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        import brick.Core
        _DataBinding = importlib.import_module('brick.Core.DataBinding')
        _EulerAngles = importlib.import_module('brick.Core.EulerAngles')
        _Geometry_Frame = importlib.import_module('brick.Geometry.Frame.Frame')
        _Geometry_Transform = importlib.import_module('brick.Geometry.Transform.Transform')
        _Physics_Component = importlib.import_module('brick.Physics.Component.Component')
        _Physics_Connector = importlib.import_module('brick.Physics.Connector.Connector')
        _Vec3 = importlib.import_module('brick.Math.Vec3')

        c = cloned.get(self)
        if c:
            return c

        c = _ExternalModule_ExternalTest.ExternalTest.new()
        cloned[self] = c
        # c._copyCustomAttributes(self)
        # Evaluating RHS values, setting raw value on LHS


        if self.connectors is None:
            c.connectors = None
        else:
            c.connectors = self.connectors._clone(cloned)
        # Evaluating RHS values, setting raw value on LHS


        if self.dataBindings is None:
            c.dataBindings = None
        else:
            c.dataBindings = self.dataBindings._clone(cloned)
        # Evaluating RHS values, setting raw value on LHS

        c.foo = self.foo

        # Evaluating RHS values, setting raw value on LHS


        if self.frame is None:
            c.frame = None
        else:
            c.frame = self.frame._clone(cloned)
        # Evaluating RHS values, setting raw value on LHS

        c.isPlaced = self.isPlaced

        # Evaluating RHS values, setting raw value on LHS

        c.name = self.name

        # Evaluating RHS values, setting raw value on LHS

        c.wantInternalPositioning = self.wantInternalPositioning


        return c

    def _applyChangeset(self, changeset):
        _ = changeset




        try:
            self.foo = changeset.data['foo']
        except KeyError:
            pass




        try:
            self.isPlaced = changeset.data['isPlaced']
        except KeyError:
            pass


        try:
            self.name = changeset.data['name']
        except KeyError:
            pass


        try:
            self.wantInternalPositioning = changeset.data['wantInternalPositioning']
        except KeyError:
            pass




    def _computeChangeSet(self, changeset):
        old = changeset.oldState
        if old is None:
            old = self._model.defaultValueWithoutLoad

        changeset.addNode('connectors', self.connectors, old and old.connectors)


        changeset.addNode('dataBindings', self.dataBindings, old and old.dataBindings)


        changeset.addScalar('foo', self.foo, old and old.foo)


        changeset.addNode('frame', self.frame, old and old.frame)


        changeset.addScalar('isPlaced', self.isPlaced, old and old.isPlaced)


        changeset.addScalar('name', self.name, old and old.name)


        changeset.addScalar('wantInternalPositioning', self.wantInternalPositioning, old and old.wantInternalPositioning)


    def _commit(self, visited, _attribute=None):

        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        import brick.Core
        _DataBinding = importlib.import_module('brick.Core.DataBinding')
        _EulerAngles = importlib.import_module('brick.Core.EulerAngles')
        _Geometry_Frame = importlib.import_module('brick.Geometry.Frame.Frame')
        _Geometry_Transform = importlib.import_module('brick.Geometry.Transform.Transform')
        _Physics_Component = importlib.import_module('brick.Physics.Component.Component')
        _Physics_Connector = importlib.import_module('brick.Physics.Connector.Connector')
        _Vec3 = importlib.import_module('brick.Math.Vec3')


        data = self._commitHeader(visited, _attribute)

        # Handle cyclic calls
        if '.ref' in data:
            return None

        rhs = self._oldState
        if not rhs:
            rhs = self._model.defaultValueWithoutLoad

        if self._connectors is not None:
            changeset = self._connectors._commit(visited, None)
            if changeset:
                data['connectors'] = changeset


        if self._dataBindings is not None:
            changeset = self._dataBindings._commit(visited, None)
            if changeset:
                data['dataBindings'] = changeset

        if self._foo != rhs._foo:
            data['foo'] = self._foo


        if self._frame is not None:
            changeset = self._frame._commit(visited, None)
            if changeset:
                data['frame'] = changeset

        if self._isPlaced != rhs._isPlaced:
            data['isPlaced'] = self._isPlaced

        if self._name != rhs._name:
            data['name'] = self._name

        if self._wantInternalPositioning != rhs._wantInternalPositioning:
            data['wantInternalPositioning'] = self._wantInternalPositioning

        self._changeSet = data

        # TODO: Apply changeset on old state is faster than creating new clone?
        self._oldState = self._clone({})
        return data


    @classmethod
    def _loadModelInstance(cls) -> Model:

        _ExternalModule_ExternalTest = importlib.import_module('brick.ExternalModule.ExternalTest')
        import brick.Core
        _DataBinding = importlib.import_module('brick.Core.DataBinding')
        _EulerAngles = importlib.import_module('brick.Core.EulerAngles')
        _Geometry_Frame = importlib.import_module('brick.Geometry.Frame.Frame')
        _Geometry_Transform = importlib.import_module('brick.Geometry.Transform.Transform')
        _Physics_Component = importlib.import_module('brick.Physics.Component.Component')
        _Physics_Connector = importlib.import_module('brick.Physics.Connector.Connector')
        _Vec3 = importlib.import_module('brick.Math.Vec3')

        from brick.Core.Model import StringModel, IntModel, RealModel, BoolModel
        from brick.Core.Model import ListModel, MapModel, SetModel, EnumModel, PathModel, TimestampModel, AnyModel

        from brick.Core.Model import Model, Value
        from brick.Core.Attribute import Attribute
        from brick.Core.Method import Method
        from brick.Core.Module import Module

        # m = Model.__new__(Model)
        m = Model(path=Path('ExternalModule.ExternalTest'), originalPath=Path('ExternalModule.ExternalTest.ExternalTest'))

        # pre-register for cyclic load
        m._cls = cls
        cls._modelInstance = m


        m.setParent(_Physics_Component.Component.model)



        a = Attribute(
            name='foo',
            description="""""",
            type=IntModel,

        )
        m.addAttribute(a)
        m._isLoaded = True
        return m








    @classmethod
    def _initConstructors(cls):
        logger.debug(f'[ExternalTest] Init constructors')
        cls._constructors = {}


    @classmethod
    def _getConstructor(cls, pattern: Union[TypePath, List[TypePath]]):
        if not hasattr(cls, '_constructors'):
            cls._initConstructors()

        if isinstance(pattern, TypePath):
            c = cls._constructors.get(pattern.str)
            if not c:
                raise Exception(f'[ExternalModule.ExternalTest] No constrcutor from {pattern}')
            return c
        else:
            raise Exception('[ExternalModule.ExternalTest] TODO: Multi-arg custom constructors')


    def dict(self, **kwargs):
        if kwargs.get('visited') is None:
            kwargs['visited'] = set()

        data = super().dict(**kwargs)
        # Handle cyclic calls
        if not isinstance(data, dict):
            return data


        data['foo'] = toDict(self.foo, **kwargs)

        return data







base_ExternalTest._modelPath = TypePath('ExternalModule.ExternalTest')
