"""openDAQ python bindings"""
from __future__ import annotations
import opendaq._opendaq
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "ArgumentInfo",
    "BaseObject",
    "BasicFileLoggerSink",
    "BlockReader",
    "BlockReaderFromExisting",
    "BoolProperty",
    "Boolean",
    "CallableInfo",
    "Client",
    "Coercer",
    "ComplexNumber",
    "Component",
    "Connection",
    "ConstantDataRule",
    "Context",
    "CoreType",
    "DataDescriptor",
    "DataDescriptorFromExisting",
    "DataPacket",
    "DataPacketWithDomain",
    "DataRule",
    "DataRuleFromExisting",
    "DataRuleType",
    "DeviceInfoConfig",
    "Dict",
    "DictProperty",
    "Dimension",
    "DimensionFromExisting",
    "DimensionFromRule",
    "DimensionRule",
    "DimensionRuleFromExisting",
    "DimensionRuleType",
    "EvalValue",
    "EvalValueArgs",
    "EvalValueFunc",
    "EventArgs",
    "EventPacket",
    "ExplicitDataRule",
    "ExternalAllocator",
    "Float",
    "FloatProperty",
    "Folder",
    "FolderWithItemType",
    "FunctionBlockType",
    "FunctionProperty",
    "IAllocator",
    "IArgumentInfo",
    "IAwaitable",
    "IBaseObject",
    "IBlockReader",
    "IBoolean",
    "ICallableInfo",
    "IChannel",
    "ICoercer",
    "IComplexNumber",
    "IComponent",
    "IConnection",
    "IContext",
    "IDataDescriptor",
    "IDataDescriptorConfig",
    "IDataPacket",
    "IDataRule",
    "IDataRuleConfig",
    "IDevice",
    "IDeviceDomain",
    "IDeviceInfo",
    "IDeviceInfoConfig",
    "IDict",
    "IDimension",
    "IDimensionConfig",
    "IDimensionRule",
    "IDimensionRuleConfig",
    "IEvalValue",
    "IEventArgs",
    "IEventPacket",
    "IFloat",
    "IFolder",
    "IFolderConfig",
    "IFunctionBlock",
    "IFunctionBlockType",
    "IGraphVisualization",
    "IInputPort",
    "IInputPortConfig",
    "IInputPortNotifications",
    "IInstance",
    "IInteger",
    "IIterable",
    "IIterator",
    "IList",
    "ILogger",
    "ILoggerComponent",
    "ILoggerSink",
    "ILoggerThreadPool",
    "IModule",
    "IModuleManager",
    "IOwnable",
    "IPacket",
    "IPacketReader",
    "IProcObject",
    "IProperty",
    "IPropertyConfig",
    "IPropertyObject",
    "IPropertyObjectClass",
    "IPropertyObjectClassConfig",
    "IPropertyObjectClassManager",
    "IPropertyObjectProtected",
    "IPropertyValueEventArgs",
    "IRange",
    "IRatio",
    "IReader",
    "IRemovable",
    "ISampleReader",
    "IScaling",
    "IScalingConfig",
    "IScheduler",
    "IServer",
    "IServerType",
    "IServerTypeConfig",
    "ISignal",
    "ISignalConfig",
    "ISignalDescriptor",
    "ISignalDescriptorConfig",
    "ISignalEvents",
    "IStreamReader",
    "IString",
    "ITags",
    "ITagsConfig",
    "ITailReader",
    "ITask",
    "ITaskGraph",
    "IUnit",
    "IUnitConfig",
    "IValidator",
    "InputPort",
    "Instance",
    "IntProperty",
    "Integer",
    "IoFolder",
    "LinearDataRule",
    "LinearDimensionRule",
    "LinearScaling",
    "List",
    "ListDimensionRule",
    "ListProperty",
    "LogLevel",
    "LogarithmicDimensionRule",
    "Logger",
    "LoggerComponent",
    "LoggerThreadPool",
    "MallocAllocator",
    "ModuleManager",
    "ObjectProperty",
    "PacketReader",
    "PacketReadyNotification",
    "PacketType",
    "Procedure",
    "Property",
    "PropertyEventType",
    "PropertyObject",
    "PropertyObjectClass",
    "PropertyObjectClassManager",
    "PropertyObjectClassWithManager",
    "PropertyObjectWithClassAndManager",
    "PropertyValueEventArgs",
    "PropertyWithName",
    "Range",
    "Ratio",
    "RatioProperty",
    "ReadTimeoutType",
    "ReferenceProperty",
    "RotatingFileLoggerSink",
    "Scaling",
    "ScalingFromExisting",
    "ScalingType",
    "Scheduler",
    "SelectionProperty",
    "ServerTypeConfig",
    "Signal",
    "SignalDescriptor",
    "SignalDescriptorChangedEventPacket",
    "SignalDescriptorFromExisting",
    "SignalWithDescriptor",
    "SparseSelectionProperty",
    "StdErrLoggerSink",
    "StdOutLoggerSink",
    "StreamReader",
    "StreamReaderFromExisting",
    "String",
    "StringProperty",
    "Tags",
    "TagsFromExisting",
    "TailReader",
    "TailReaderFromExisting",
    "Task",
    "TaskGraph",
    "Unit",
    "UnitEmpty",
    "UnitFromExisting",
    "Validator",
    "WinDebugLoggerSink",
    "clear_error_info",
    "get_tracked_object_count",
    "print_tracked_objects"
]


class CoreType():
    """
    Members:

      ctBool

      ctInt

      ctFloat

      ctString

      ctList

      ctDict

      ctRatio

      ctProc

      ctObject

      ctBinaryData

      ctFunc

      ctComplexNumber

      ctUndefined
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    __members__: dict # value = {'ctBool': <CoreType.ctBool: 0>, 'ctInt': <CoreType.ctInt: 1>, 'ctFloat': <CoreType.ctFloat: 2>, 'ctString': <CoreType.ctString: 3>, 'ctList': <CoreType.ctList: 4>, 'ctDict': <CoreType.ctDict: 5>, 'ctRatio': <CoreType.ctRatio: 6>, 'ctProc': <CoreType.ctProc: 7>, 'ctObject': <CoreType.ctObject: 8>, 'ctBinaryData': <CoreType.ctBinaryData: 9>, 'ctFunc': <CoreType.ctFunc: 10>, 'ctComplexNumber': <CoreType.ctComplexNumber: 11>, 'ctUndefined': <CoreType.ctUndefined: 65535>}
    ctBinaryData: opendaq._opendaq.CoreType # value = <CoreType.ctBinaryData: 9>
    ctBool: opendaq._opendaq.CoreType # value = <CoreType.ctBool: 0>
    ctComplexNumber: opendaq._opendaq.CoreType # value = <CoreType.ctComplexNumber: 11>
    ctDict: opendaq._opendaq.CoreType # value = <CoreType.ctDict: 5>
    ctFloat: opendaq._opendaq.CoreType # value = <CoreType.ctFloat: 2>
    ctFunc: opendaq._opendaq.CoreType # value = <CoreType.ctFunc: 10>
    ctInt: opendaq._opendaq.CoreType # value = <CoreType.ctInt: 1>
    ctList: opendaq._opendaq.CoreType # value = <CoreType.ctList: 4>
    ctObject: opendaq._opendaq.CoreType # value = <CoreType.ctObject: 8>
    ctProc: opendaq._opendaq.CoreType # value = <CoreType.ctProc: 7>
    ctRatio: opendaq._opendaq.CoreType # value = <CoreType.ctRatio: 6>
    ctString: opendaq._opendaq.CoreType # value = <CoreType.ctString: 3>
    ctUndefined: opendaq._opendaq.CoreType # value = <CoreType.ctUndefined: 65535>
    pass
class DataRuleType():
    """
    Members:

      Other

      Linear

      Constant

      Explicit
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Constant: opendaq._opendaq.DataRuleType # value = <DataRuleType.Constant: 2>
    Explicit: opendaq._opendaq.DataRuleType # value = <DataRuleType.Explicit: 3>
    Linear: opendaq._opendaq.DataRuleType # value = <DataRuleType.Linear: 1>
    Other: opendaq._opendaq.DataRuleType # value = <DataRuleType.Other: 0>
    __members__: dict # value = {'Other': <DataRuleType.Other: 0>, 'Linear': <DataRuleType.Linear: 1>, 'Constant': <DataRuleType.Constant: 2>, 'Explicit': <DataRuleType.Explicit: 3>}
    pass
class DimensionRuleType():
    """
    Members:

      Other

      Linear

      Logarithmic

      List
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Linear: opendaq._opendaq.DimensionRuleType # value = <DimensionRuleType.Linear: 1>
    List: opendaq._opendaq.DimensionRuleType # value = <DimensionRuleType.List: 3>
    Logarithmic: opendaq._opendaq.DimensionRuleType # value = <DimensionRuleType.Logarithmic: 2>
    Other: opendaq._opendaq.DimensionRuleType # value = <DimensionRuleType.Other: 0>
    __members__: dict # value = {'Other': <DimensionRuleType.Other: 0>, 'Linear': <DimensionRuleType.Linear: 1>, 'Logarithmic': <DimensionRuleType.Logarithmic: 2>, 'List': <DimensionRuleType.List: 3>}
    pass
class IBaseObject():
    def __eq__(self, arg0: object) -> bool: ...
    def __float__(self) -> float: ...
    def __hash__(self) -> int: ...
    def __init__(self, arg0: IBaseObject) -> None: ...
    def __int__(self) -> int: ...
    def __str__(self) -> str: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IBaseObject: ...
    @property
    def core_type(self) -> daq::CoreType:
        """
        :type: daq::CoreType
        """
    pass
class IArgumentInfo(IBaseObject):
    """
    Provides the name and type of a single function/procedure argument
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IArgumentInfo: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IArgumentInfo: ...
    @property
    def name(self) -> str:
        """
        Gets the name of the argument.

        :type: str
        """
    @property
    def type(self) -> CoreType:
        """
        Gets the core type of the argument.

        :type: CoreType
        """
    pass
class IAwaitable(IBaseObject):
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    def cancel(self) -> int: 
        """
        Cancels the outstanding work if it has not already started.
        """
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IAwaitable: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IAwaitable: ...
    def has_completed(self) -> int: 
        """
        Checks if the execution has already finished.
        """
    def wait(self) -> None: ...
    @property
    def result(self) -> object:
        """
        Waits until the awaitable has a valid result and retrieves it or re-throws the exception that occurred during the execution.

        :type: object
        """
    pass
class IAllocator(IBaseObject):
    """
    An allocator used to allocate memory.
    """
    def allocate(self, descriptor: ISignalDescriptor, bytes: int, align: int) -> capsule: 
        """
        Allocates a chunk of memory for a packet.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IAllocator: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IAllocator: ...
    def free(self, address: capsule) -> None: 
        """
        Releases a chunk of memory allocated by allocate().
        """
    pass
class IReader(IBaseObject):
    """
    A basic signal reader that simplifies accessing the signals's data stream.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IReader: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IReader: ...
    @property
    def available_count(self) -> int:
        """
        Gets the number of segments available to read

        :type: int
        """
    @property
    def on_descriptor_changed(self) -> None:
        """
        Gets the user the option to invalidate the reader when the signal descriptor changes.

        :type: None
        """
    @on_descriptor_changed.setter
    def on_descriptor_changed(self, arg1: daq::IFunction) -> None:
        """
        Gets the user the option to invalidate the reader when the signal descriptor changes.
        """
    pass
class IBoolean(IBaseObject):
    """
    Represents boolean variable as `IBoolean` interface. Use this interface to wrap boolean variable when you need to add the variable to lists, dictionaries and other containers which accept `IBaseObject` interface.
    """
    def __bool__(self) -> bool: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IBoolean: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IBoolean: ...
    @property
    def value(self) -> bool:
        """
        Gets a boolean value stored in the object.

        :type: bool
        """
    pass
class ICallableInfo(IBaseObject):
    """
    Provides information about the argument count and types, as well as the return type of Function/Procedure-type properties.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ICallableInfo: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ICallableInfo: ...
    @property
    def arguments(self) -> IList:
        """
        Gets the list of arguments the callable function/procedure expects.

        :type: IList
        """
    @property
    def return_type(self) -> CoreType:
        """
        Gets the return type of the callable function.

        :type: CoreType
        """
    pass
class IPropertyObject(IBaseObject):
    """
    A container of Properties and their corresponding Property values.
    """
    def add_property(self, property: IProperty) -> None: 
        """
        Adds the property to the Property object.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyObject: ...
    def clear_property_value(self, property_name: str) -> None: 
        """
        Clears the Property value from the Property object
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyObject: ...
    def get_property(self, property_name: str) -> IProperty: 
        """
        Gets the Property with the given `propertyName`.
        """
    def get_property_selection_value(self, property_name: str) -> object: 
        """
        Gets the selected value of the Property, if the Property is a Selection property.
        """
    def get_property_value(self, property_name: str) -> object: 
        """
        Gets the value of the Property with the given name.
        """
    def has_property(self, property_name: str) -> int: 
        """
        Checks if the Property object contains a property named `propertyName`.
        """
    def remove_property(self, property_name: str) -> None: 
        """
        Removes the Property named `propertyName` from the Property object.
        """
    def set_property_value(self, property_name: str, value: object) -> None: 
        """
        Sets the value of the Property with the given name.
        """
    @property
    def all_properties(self) -> IList:
        """
        Returns a list of all properties contained in the Property object.

        :type: IList
        """
    @property
    def class_name(self) -> str:
        """
        Gets the name of the class the Property object was constructed with.

        :type: str
        """
    @property
    def property_order(self) -> None:
        """
        Sets a custom order of properties as defined in the list of property names.

        :type: None
        """
    @property_order.setter
    def property_order(self, arg1: IList) -> None:
        """
        Sets a custom order of properties as defined in the list of property names.
        """
    @property
    def visible_properties(self) -> IList:
        """
        Returns a list of visible properties contained in the Property object.

        :type: IList
        """
    pass
class ICoercer(IBaseObject):
    """
    Used by openDAQ properties to coerce a value to match the restrictions imposed by the Property.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ICoercer: ...
    def coerce(self, prop_obj: object, value: object) -> object: 
        """
        Coerces `value` to match the coercion restrictions and outputs the result.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ICoercer: ...
    @property
    def eval(self) -> str:
        """
        Gets the string expression used when creating the coercer.

        :type: str
        """
    pass
class IComplexNumber(IBaseObject):
    """
    Represents a complex number as `IComplexNumber` interface. Use this interface to wrap complex number when you need to add the number to lists, dictionaries and other containers which accept `IBaseObject` and derived interfaces. Complex numbers have two components: real and imaginary. Both of them are of Float type.
    """
    def __complex__(self) -> complex: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IComplexNumber: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IComplexNumber: ...
    @staticmethod
    def equals_value(*args, **kwargs) -> typing.Any: 
        """
        Compares stored complex value to the complex number parameter.
        """
    @property
    def imaginary(self) -> float:
        """
        Gets the imaginary part of the complex number value.

        :type: float
        """
    @property
    def real(self) -> float:
        """
        Gets the real part of the complex number value.

        :type: float
        """
    @property
    def value(self) -> complex:
        """
        Gets a complex value stored in the object.

        :type: complex
        """
    pass
class IComponent(IPropertyObject, IBaseObject):
    """
    Acts as a base interface for components, such as device, function block, channel and signal.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IComponent: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IComponent: ...
    @property
    def active(self) -> int:
        """
        Returns true if the component is active; false otherwise. / Sets the component to be either active or inactive.

        :type: int
        """
    @active.setter
    def active(self, arg1: bool) -> None:
        """
        Returns true if the component is active; false otherwise. / Sets the component to be either active or inactive.
        """
    @property
    def context(self) -> IContext:
        """
        Gets the context object.

        :type: IContext
        """
    @property
    def global_id(self) -> str:
        """
        Gets the global ID of the component.

        :type: str
        """
    @property
    def local_id(self) -> str:
        """
        Gets the local ID of the component.

        :type: str
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the component.

        :type: str
        """
    @property
    def parent(self) -> IComponent:
        """
        Gets the parent of the component.

        :type: IComponent
        """
    @property
    def tags(self) -> ITagsConfig:
        """
        Gets the tags of the component.

        :type: ITagsConfig
        """
    pass
class IConnection(IBaseObject):
    """
    Represents a connection between an Input port and Signal. Acts as a queue for packets sent by the signal, which can be read by the input port and the input port's owner.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IConnection: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IConnection: ...
    def dequeue(self) -> IPacket: 
        """
        Removes the packet at the front of the queue and returns it.
        """
    def enqueue(self, packet: IPacket) -> None: 
        """
        Places a packet at the back of the queue.
        """
    def peek(self) -> IPacket: 
        """
        Returns the packet at the front of the queue without removing it.
        """
    @property
    def available_samples(self) -> int:
        """
        Gets the number of samples available in the queued packets. The returned value ignores any Sample-Descriptor changes.

        :type: int
        """
    @property
    def input_port(self) -> IInputPort:
        """
        Gets the Input port to which packets are being sent.

        :type: IInputPort
        """
    @property
    def packet_count(self) -> int:
        """
        Gets the number of queued packets.

        :type: int
        """
    @property
    def signal(self) -> ISignal:
        """
        Gets the Signal that is sending packets through the Connection.

        :type: ISignal
        """
    pass
class IContext(IBaseObject):
    """
    The Context serves as a container for the Scheduler and Logger. It originates at the instance, and is passed to the root device, which forwards it to components such as function blocks and signals.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IContext: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IContext: ...
    @property
    def logger(self) -> ILogger:
        """
        Gets the logger.

        :type: ILogger
        """
    @property
    def property_object_class_manager(self) -> IPropertyObjectClassManager:
        """
        :type: IPropertyObjectClassManager
        """
    @property
    def scheduler(self) -> IScheduler:
        """
        Gets the scheduler.

        :type: IScheduler
        """
    pass
class IDataDescriptor(IBaseObject):
    """
    Describes the data sent by a signal, defining how they are to be interpreted by anyone receiving the signal's packets.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDataDescriptor: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDataDescriptor: ...
    @property
    def dimensions(self) -> IList:
        """
        Gets the list of the descriptor's dimension's.

        :type: IList
        """
    @property
    def name(self) -> str:
        """
        Gets a descriptive name of the signal value.

        :type: str
        """
    @property
    def origin(self) -> str:
        """
        Gets the absolute origin of a signal value component.

        :type: str
        """
    @property
    def post_scaling(self) -> IScaling:
        """
        :type: IScaling
        """
    @property
    def rule(self) -> IDataRule:
        """
        Gets the value Data rule.

        :type: IDataRule
        """
    @property
    def sample_type(self) -> daq::SampleType:
        """
        Gets the descriptor's sample type.

        :type: daq::SampleType
        """
    @property
    def struct_fields(self) -> IList:
        """
        Gets the fields of the struct, forming a recursive value descriptor definition.

        :type: IList
        """
    @property
    def tick_resolution(self) -> IRatio:
        """
        Gets the Resolution which scales the an explicit or implicit value to the physical unit defined in `unit`. It is defined as domain (usualy time) between two consecutive ticks.

        :type: IRatio
        """
    @property
    def unit(self) -> IUnit:
        """
        Gets the unit of the data in a signal's packets.

        :type: IUnit
        """
    @property
    def value_range(self) -> IRange:
        """
        Gets the value range of the data in a signal's packets defining the lowest and highest expected values.

        :type: IRange
        """
    pass
class IDataDescriptorConfig(IDataDescriptor, IBaseObject):
    """
    Configuration component of Data descriptor objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDataDescriptorConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDataDescriptorConfig: ...
    @property
    def dimensions(self) -> None:
        """
        Sets the list of the descriptor's dimension's.

        :type: None
        """
    @dimensions.setter
    def dimensions(self, arg1: IList) -> None:
        """
        Sets the list of the descriptor's dimension's.
        """
    @property
    def name(self) -> None:
        """
        Sets a descriptive name for the signal's value.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets a descriptive name for the signal's value.
        """
    @property
    def origin(self) -> None:
        """
        Sets the absolute origin of a signal value component.

        :type: None
        """
    @origin.setter
    def origin(self, arg1: str) -> None:
        """
        Sets the absolute origin of a signal value component.
        """
    @property
    def post_scaling(self) -> None:
        """
        Sets the scaling rule that needs to be applied to explicit/implicit data by readers.

        :type: None
        """
    @post_scaling.setter
    def post_scaling(self, arg1: IScaling) -> None:
        """
        Sets the scaling rule that needs to be applied to explicit/implicit data by readers.
        """
    @property
    def rule(self) -> None:
        """
        Sets the value Data rule.

        :type: None
        """
    @rule.setter
    def rule(self, arg1: IDataRule) -> None:
        """
        Sets the value Data rule.
        """
    @property
    def sample_type(self) -> None:
        """
        Sets the descriptor's sample type.

        :type: None
        """
    @sample_type.setter
    def sample_type(self, arg1: daq::SampleType) -> None:
        """
        Sets the descriptor's sample type.
        """
    @property
    def struct_fields(self) -> None:
        """
        Sets the fields of the struct, forming a recursive value descriptor definition.

        :type: None
        """
    @struct_fields.setter
    def struct_fields(self, arg1: IList) -> None:
        """
        Sets the fields of the struct, forming a recursive value descriptor definition.
        """
    @property
    def tick_resolution(self) -> None:
        """
        Sets the Resolution which scales the an explicit or implicit value to the physical unit defined in `unit`.

        :type: None
        """
    @tick_resolution.setter
    def tick_resolution(self, arg1: IRatio) -> None:
        """
        Sets the Resolution which scales the an explicit or implicit value to the physical unit defined in `unit`.
        """
    @property
    def unit(self) -> None:
        """
        Sets the unit of the data in a signal's packets.

        :type: None
        """
    @unit.setter
    def unit(self, arg1: IUnit) -> None:
        """
        Sets the unit of the data in a signal's packets.
        """
    @property
    def value_range(self) -> None:
        """
        Sets the value range of the data in a signal's packets defining the lowest and highest expected values.

        :type: None
        """
    @value_range.setter
    def value_range(self, arg1: IRange) -> None:
        """
        Sets the value range of the data in a signal's packets defining the lowest and highest expected values.
        """
    pass
class IPacket(IBaseObject):
    """
    Base packet type. Data, Value, and Event packets are all also packets. Provides the packet's unique ID that is unique to a given device, as well as the packet type.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPacket: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPacket: ...
    @property
    def type(self) -> PacketType:
        """
        Gets the packet's type.

        :type: PacketType
        """
    pass
class IDataRule(IBaseObject):
    """
    Rule that defines how a signal value is calculated from an implicit initialization value when the rule type is not `Explicit`.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDataRule: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDataRule: ...
    @property
    def parameters(self) -> IDict:
        """
        Gets a dictionary of string-object key-value pairs representing the parameters used to evaluate the rule.

        :type: IDict
        """
    @property
    def type(self) -> DataRuleType:
        """
        Gets the type of the data rule.

        :type: DataRuleType
        """
    pass
class IDataRuleConfig(IDataRule, IBaseObject):
    """
    Configuration component of Data rule objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDataRuleConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDataRuleConfig: ...
    @property
    def parameters(self) -> None:
        """
        Sets a dictionary of string-object key-value pairs representing the parameters used to evaluate the rule.

        :type: None
        """
    @parameters.setter
    def parameters(self, arg1: IDict) -> None:
        """
        Sets a dictionary of string-object key-value pairs representing the parameters used to evaluate the rule.
        """
    @property
    def type(self) -> None:
        """
        Sets the type of the data rule.

        :type: None
        """
    @type.setter
    def type(self, arg1: DataRuleType) -> None:
        """
        Sets the type of the data rule.
        """
    pass
class IFolder(IComponent, IPropertyObject, IBaseObject):
    """
    Acts as a container for other components
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IFolder: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IFolder: ...
    def get_item(self, local_id: str) -> IComponent: 
        """
        Gets the item component with the specified localId.
        """
    @property
    def items(self) -> IList:
        """
        Gets the list of the items in the folder.

        :type: IList
        """
    pass
class IDeviceDomain(IBaseObject):
    """
    Contains information about the domain of the device.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDeviceDomain: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDeviceDomain: ...
    @property
    def origin(self) -> str:
        """
        Gets the device's absolute origin. Most often this is a time epoch in the ISO 8601 format.

        :type: str
        """
    @property
    def tick_resolution(self) -> IRatio:
        """
        Gets domain (usually time) between two consecutive ticks. Resolution is provided in a domain unit.

        :type: IRatio
        """
    @property
    def ticks_since_origin(self) -> int:
        """
        Gets the number of ticks passed since the device's absolute origin.

        :type: int
        """
    @property
    def unit(self) -> IUnit:
        """
        Gets the domain unit (eg. seconds, hours, degrees...)

        :type: IUnit
        """
    pass
class IDeviceInfo(IPropertyObject, IBaseObject):
    """
    Contains standard information about an openDAQ device. Also allows for custom metadata to be provided as a dictionary of <string, string> key-value pairs.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDeviceInfo: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDeviceInfo: ...
    @property
    def connection_string(self) -> str:
        """
        Gets the string representation of a connection address used to connect to the device.

        :type: str
        """
    @property
    def device_class(self) -> str:
        """
        Gets the purpose of the device. For example "TestMeasurementDevice".

        :type: str
        """
    @property
    def device_manual(self) -> str:
        """
        Gets the address of the user manual. It may be a pathname in the file system or a URL (Web address)

        :type: str
        """
    @property
    def hardware_revision(self) -> str:
        """
        Gets the revision level of the hardware

        :type: str
        """
    @property
    def manufacturer(self) -> str:
        """
        Gets the company that manufactured the device

        :type: str
        """
    @property
    def manufacturer_uri(self) -> str:
        """
        Gets the unique identifier of the company that manufactured the device This identifier should be a fully qualified domain name; however, it may be a GUID or similar construct that ensures global uniqueness.

        :type: str
        """
    @property
    def model(self) -> str:
        """
        Gets the model of the device

        :type: str
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the device

        :type: str
        """
    @property
    def product_code(self) -> str:
        """
        Gets the unique combination of numbers and letters used to identify the device.

        :type: str
        """
    @property
    def product_instance_uri(self) -> str:
        """
        Gets the globally unique resource identifier provided by the manufacturer. The recommended syntax of the ProductInstanceUri is: <ManufacturerUri>/<any string> where <any string> is unique among all instances using the same ManufacturerUri.

        :type: str
        """
    @property
    def revision_counter(self) -> str:
        """
        Gets the incremental counter indicating the number of times the configuration data has been modified.

        :type: str
        """
    @property
    def serial_number(self) -> str:
        """
        Gets the unique production number provided by the manufacturer

        :type: str
        """
    @property
    def software_revision(self) -> str:
        """
        Gets the revision level of the software component

        :type: str
        """
    pass
class IDeviceInfoConfig(IDeviceInfo, IPropertyObject, IBaseObject):
    """
    Configuration component of Device info objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDeviceInfoConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDeviceInfoConfig: ...
    @property
    def connection_string(self) -> None:
        """
        Sets the string representation of a connection address used to connect to the device.

        :type: None
        """
    @connection_string.setter
    def connection_string(self, arg1: str) -> None:
        """
        Sets the string representation of a connection address used to connect to the device.
        """
    @property
    def device_class(self) -> None:
        """
        Sets the purpose of the device. For example "TestMeasurementDevice".

        :type: None
        """
    @device_class.setter
    def device_class(self, arg1: str) -> None:
        """
        Sets the purpose of the device. For example "TestMeasurementDevice".
        """
    @property
    def device_manual(self) -> None:
        """
        Sets the address of the user manual. It may be a pathname in the file system or a URL (Web address)

        :type: None
        """
    @device_manual.setter
    def device_manual(self, arg1: str) -> None:
        """
        Sets the address of the user manual. It may be a pathname in the file system or a URL (Web address)
        """
    @property
    def hardware_revision(self) -> None:
        """
        Sets the revision level of the hardware

        :type: None
        """
    @hardware_revision.setter
    def hardware_revision(self, arg1: str) -> None:
        """
        Sets the revision level of the hardware
        """
    @property
    def manufacturer(self) -> None:
        """
        Sets the company that manufactured the device

        :type: None
        """
    @manufacturer.setter
    def manufacturer(self, arg1: str) -> None:
        """
        Sets the company that manufactured the device
        """
    @property
    def manufacturer_uri(self) -> None:
        """
        Sets the unique identifier of the company that manufactured the device. This identifier should be a fully qualified domain name; however, it may be a GUID or similar construct that ensures global uniqueness.

        :type: None
        """
    @manufacturer_uri.setter
    def manufacturer_uri(self, arg1: str) -> None:
        """
        Sets the unique identifier of the company that manufactured the device. This identifier should be a fully qualified domain name; however, it may be a GUID or similar construct that ensures global uniqueness.
        """
    @property
    def model(self) -> None:
        """
        Sets the model of the device

        :type: None
        """
    @model.setter
    def model(self, arg1: str) -> None:
        """
        Sets the model of the device
        """
    @property
    def name(self) -> None:
        """
        Sets the name of the device

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the name of the device
        """
    @property
    def product_code(self) -> None:
        """
        Sets the unique combination of numbers and letters used to identify the device.

        :type: None
        """
    @product_code.setter
    def product_code(self, arg1: str) -> None:
        """
        Sets the unique combination of numbers and letters used to identify the device.
        """
    @property
    def product_instance_uri(self) -> None:
        """
        Sets the globally unique resource identifier provided by the manufacturer. The recommended syntax of the ProductInstanceUri is: <ManufacturerUri>/<any string> where <any string> is unique among all instances using the same ManufacturerUri.

        :type: None
        """
    @product_instance_uri.setter
    def product_instance_uri(self, arg1: str) -> None:
        """
        Sets the globally unique resource identifier provided by the manufacturer. The recommended syntax of the ProductInstanceUri is: <ManufacturerUri>/<any string> where <any string> is unique among all instances using the same ManufacturerUri.
        """
    @property
    def revision_counter(self) -> None:
        """
        Sets the incremental counter indicating the number of times the configuration data has been modified.

        :type: None
        """
    @revision_counter.setter
    def revision_counter(self, arg1: str) -> None:
        """
        Sets the incremental counter indicating the number of times the configuration data has been modified.
        """
    @property
    def serial_number(self) -> None:
        """
        Sets the serial number of the device

        :type: None
        """
    @serial_number.setter
    def serial_number(self, arg1: str) -> None:
        """
        Sets the serial number of the device
        """
    @property
    def software_revision(self) -> None:
        """
        sets the revision level of the software component

        :type: None
        """
    @software_revision.setter
    def software_revision(self, arg1: str) -> None:
        """
        sets the revision level of the software component
        """
    pass
class IDict(IBaseObject):
    """
    Represents a heterogeneous dictionary of objects.
    """
    def __delitem__(self, arg0: object) -> None: ...
    def __getitem__(self, arg0: object) -> object: ...
    def __iter__(self) -> object: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg0: object, arg1: object) -> None: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDict: ...
    def clear(self) -> None: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDict: ...
    def items(self) -> list: ...
    def keys(self) -> IIterable: ...
    def pop(self, arg0: object) -> IBaseObject: ...
    def values(self) -> IIterable: ...
    pass
class IDimension(IBaseObject):
    """
    Describes a dimension of the signal's data. Eg. a column/row in a matrix.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDimension: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDimension: ...
    @property
    def labels(self) -> IList:
        """
        Gets a list of labels that defines the dimension.

        :type: IList
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the dimension.

        :type: str
        """
    @property
    def rule(self) -> IDimensionRule:
        """
        Gets the rule that defines the labels and size of the dimension.

        :type: IDimensionRule
        """
    @property
    def size(self) -> int:
        """
        Gets the size of the dimension.

        :type: int
        """
    @property
    def unit(self) -> IUnit:
        """
        Gets the unit of the dimension's labels.

        :type: IUnit
        """
    pass
class IDimensionConfig(IDimension, IBaseObject):
    """
    Configuration component of Dimension objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDimensionConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDimensionConfig: ...
    @property
    def name(self) -> None:
        """
        Sets the name of the dimension.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the name of the dimension.
        """
    @property
    def rule(self) -> None:
        """
        Sets the rule that defines the labels and size of the dimension.

        :type: None
        """
    @rule.setter
    def rule(self, arg1: IDimensionRule) -> None:
        """
        Sets the rule that defines the labels and size of the dimension.
        """
    @property
    def unit(self) -> None:
        """
        Sets the unit of the dimension's labels.

        :type: None
        """
    @unit.setter
    def unit(self, arg1: IUnit) -> None:
        """
        Sets the unit of the dimension's labels.
        """
    pass
class IDimensionRule(IBaseObject):
    """
    Rule that defines the labels (alternatively called bins, ticks) of a dimension.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDimensionRule: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDimensionRule: ...
    @property
    def parameters(self) -> IDict:
        """
        Gets a dictionary of string-object key-value pairs representing the parameters used to evaluate the rule.

        :type: IDict
        """
    @property
    def type(self) -> DimensionRuleType:
        """
        Gets the type of the dimension rule.

        :type: DimensionRuleType
        """
    pass
class IDimensionRuleConfig(IDimensionRule, IBaseObject):
    """
    Configuration component of Dimension rule objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDimensionRuleConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDimensionRuleConfig: ...
    @property
    def parameters(self) -> None:
        """
        Sets a dictionary of string-object key-value pairs representing the parameters used to evaluate the rule.

        :type: None
        """
    @parameters.setter
    def parameters(self, arg1: IDict) -> None:
        """
        Sets a dictionary of string-object key-value pairs representing the parameters used to evaluate the rule.
        """
    @property
    def type(self) -> None:
        """
        Sets the type of the dimension rule. Rule parameters must be configured to match the requirements of the rule type.

        :type: None
        """
    @type.setter
    def type(self, arg1: DimensionRuleType) -> None:
        """
        Sets the type of the dimension rule. Rule parameters must be configured to match the requirements of the rule type.
        """
    pass
class IEvalValue(IBaseObject):
    """
    Dynamic expression evaluator
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IEvalValue: ...
    def clone_with_owner(self, owner: IPropertyObject) -> IEvalValue: 
        """
        Clones the object and attaches an owner.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IEvalValue: ...
    def get_parse_error_code(self) -> None: 
        """
        Returns the parse error code.
        """
    @property
    def eval(self) -> str:
        """
        Gets the expression.

        :type: str
        """
    @property
    def property_references(self) -> IList:
        """
        Returns the names of all properties referenced by the eval value.

        :type: IList
        """
    @property
    def result(self) -> object:
        """
        Gets the result of the expression.

        :type: object
        """
    pass
class IEventArgs(IBaseObject):
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IEventArgs: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IEventArgs: ...
    @property
    def event_id(self) -> int:
        """
        :type: int
        """
    @property
    def event_name(self) -> str:
        """
        :type: str
        """
    pass
class IEventPacket(IPacket, IBaseObject):
    """
    As with Data packets, Event packets travel along the signal paths. They are used to notify recipients of any relevant changes to the signal sending the packet.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IEventPacket: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IEventPacket: ...
    @property
    def event_id(self) -> str:
        """
        Gets the ID of the event as a string. In example "SIGNAL_DESCRIPTOR_CHANGED".

        :type: str
        """
    @property
    def parameters(self) -> IDict:
        """
        Dictionary containing parameters as <String, BaseObject> pairs relevant to the event signalized by the Event packet.

        :type: IDict
        """
    pass
class IFloat(IBaseObject):
    """
    Represents float number as `IFloat` interface. Use this interface to wrap float variable when you need to add the number to lists, dictionaries and other containers which accept `IBaseObject` and derived interfaces. Float type is defined as double-precision IEEE 754 value.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IFloat: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IFloat: ...
    @property
    def value(self) -> float:
        """
        Gets a float value stored in the object.

        :type: float
        """
    pass
class IFunctionBlock(IFolder, IComponent, IPropertyObject, IBaseObject):
    """
    Function blocks perform calculations on inputs/generate data, outputting new data in its output signals as packets.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IFunctionBlock: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IFunctionBlock: ...
    @property
    def function_block_type(self) -> IFunctionBlockType:
        """
        Gets an information structure contain metadata of the function block type.

        :type: IFunctionBlockType
        """
    @property
    def function_blocks(self) -> IList:
        """
        Gets a list of sub-function blocks.

        :type: IList
        """
    @property
    def input_ports(self) -> IList:
        """
        Gets a list of the function block's input ports.

        :type: IList
        """
    @property
    def signals(self) -> IList:
        """
        Gets the list of the function block's output signals.

        :type: IList
        """
    @property
    def signals_recursive(self) -> IList:
        """
        Gets the list of the function block's output signals including signals from child function blocks.

        :type: IList
        """
    @property
    def status_signal(self) -> ISignal:
        """
        Gets the function block's status signal.

        :type: ISignal
        """
    pass
class IFolderConfig(IFolder, IComponent, IPropertyObject, IBaseObject):
    """
    Allows write access to folder.
    """
    def add_item(self, item: IComponent) -> None: 
        """
        Adds a component to the folder.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IFolderConfig: ...
    def clear(self) -> None: 
        """
        Removes all items from the folder.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IFolderConfig: ...
    def remove_item(self, item: IComponent) -> None: 
        """
        Removes the item from the folder.
        """
    def remove_item_with_local_id(self, local_id: str) -> None: 
        """
        Removes the item from the folder using local id of the component.
        """
    @property
    def name(self) -> None:
        """
        Sets the name of the folder.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the name of the folder.
        """
    pass
class IChannel(IFunctionBlock, IFolder, IComponent, IPropertyObject, IBaseObject):
    """
    Channels represent physical sensors of openDAQ devices. Internally they are standard function blocks with an additional option to provide a list of tags.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IChannel: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IChannel: ...
    pass
class IFunctionBlockType(IBaseObject):
    """
    Provides information about the function block.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IFunctionBlockType: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IFunctionBlockType: ...
    def create_default_config(self) -> IPropertyObject: 
        """
        Creates a default configuration objects for given function block type.
        """
    @property
    def description(self) -> str:
        """
        Gets the description.

        :type: str
        """
    @property
    def id(self) -> str:
        """
        Gets the unique id.

        :type: str
        """
    @property
    def name(self) -> str:
        """
        Gets the name.

        :type: str
        """
    pass
class IGraphVisualization(IBaseObject):
    """
    Represents a way to get a string representation of a graph usually in some diagram description language like DOT, mermaid or D2.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IGraphVisualization: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IGraphVisualization: ...
    def dump(self) -> str: 
        """
        Returns the graph representation as a string.
        """
    pass
class IInputPort(IComponent, IPropertyObject, IBaseObject):
    """
    Signals accepted by input ports can be connected, forming a connection between the input port and signal, through which Packets can be sent.
    """
    def accepts_signal(self, signal: ISignal) -> int: 
        """
        Returns true if the signal can be connected to the input port; false otherwise.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IInputPort: ...
    def connect(self, signal: ISignal) -> None: 
        """
        Connects the signal to the input port, forming a Connection.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IInputPort: ...
    def disconnect(self) -> None: 
        """
        Disconnects the signal from the input port.
        """
    @property
    def connection(self) -> IConnection:
        """
        Gets the Connection object formed between the Signal and Input port.

        :type: IConnection
        """
    @property
    def requires_signal(self) -> int:
        """
        Returns true if the input port requires a signal to be connected; false otherwise.

        :type: int
        """
    @property
    def signal(self) -> ISignal:
        """
        Gets the signal connected to the input port.

        :type: ISignal
        """
    pass
class IInputPortConfig(IInputPort, IComponent, IPropertyObject, IBaseObject):
    """
    The configuration component of input ports. Provides access to Input port owners to internal components of the input port.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IInputPortConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IInputPortConfig: ...
    def notify_packet_enqueued(self) -> None: 
        """
        Gets called when a packet was enqueued in a connection.
        """
    @property
    def custom_data(self) -> object:
        """
        Get a custom data attached to the object. / Set a custom data attached to the object.

        :type: object
        """
    @custom_data.setter
    def custom_data(self, arg1: object) -> None:
        """
        Get a custom data attached to the object. / Set a custom data attached to the object.
        """
    @property
    def listener(self) -> None:
        """
        Set the object receiving input-port related events and notifications.

        :type: None
        """
    @listener.setter
    def listener(self, arg1: IInputPortNotifications) -> None:
        """
        Set the object receiving input-port related events and notifications.
        """
    @property
    def notification_method(self) -> None:
        """
        Sets the input-ports response to the packet enqueued notification.

        :type: None
        """
    @notification_method.setter
    def notification_method(self, arg1: PacketReadyNotification) -> None:
        """
        Sets the input-ports response to the packet enqueued notification.
        """
    @property
    def requires_signal(self) -> None:
        """
        Sets requires signal flag of the input port.

        :type: None
        """
    @requires_signal.setter
    def requires_signal(self, arg1: bool) -> None:
        """
        Sets requires signal flag of the input port.
        """
    pass
class IInputPortNotifications(IBaseObject):
    """
    Notifications object passed to the input port on construction by its owner (listener).
    """
    def accepts_signal(self, port: IInputPort, signal: ISignal) -> int: 
        """
        Called when the Input port method `acceptsSignal` is called. Should return true if the signal is accepted; false otherwise.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IInputPortNotifications: ...
    def connected(self, port: IInputPort) -> None: 
        """
        Called when a signal is connected to the input port.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IInputPortNotifications: ...
    def disconnected(self, port: IInputPort) -> None: 
        """
        Called when a signal is disconnected from the input port.
        """
    def packet_received(self, port: IInputPort) -> None: 
        """
        Notifies the listener of the newly received packet on the specified input-port.
        """
    pass
class IDevice(IFolder, IComponent, IPropertyObject, IBaseObject):
    """
    Represents an openDAQ device. The device contains a list of signals and physical channels. Some devices support adding function blocks, or connecting to devices. The list of available function blocks/devices can be obtained via the `getAvailable` functions, and added via the `add` functions.
    """
    def add_device(self, connection_string: str, config: IPropertyObject = None) -> IDevice: 
        """
        Connects to a device at the given connection string and returns it.
        """
    def add_function_block(self, type_id: str, config: IPropertyObject = None) -> IFunctionBlock: 
        """
        Creates and adds a function block to the device with the provided unique ID and returns it.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDevice: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDevice: ...
    def remove_device(self, device: IDevice) -> None: 
        """
        Disconnects from the device provided as argument and removes it from the internal list of devices.
        """
    def remove_function_block(self, function_block: IFunctionBlock) -> None: 
        """
        Removes the function block provided as argument, disconnecting its signals and input ports.
        """
    @property
    def available_devices(self) -> IDict:
        """
        Gets a list of available devices, containing their Device Info.

        :type: IDict
        """
    @property
    def available_function_blocks(self) -> IDict:
        """
        Gets all function block types that are supported by the device, containing their description.

        :type: IDict
        """
    @property
    def channels(self) -> IList:
        """
        Gets a flat list of the device's physical channels.

        :type: IList
        """
    @property
    def channels_recursive(self) -> IList:
        """
        Gets a flat list of the device's physical channels. Also finds all channels of child devices

        :type: IList
        """
    @property
    def custom_components(self) -> IList:
        """
        Gets a list of all components/folders in a device that are not titled 'io', 'sig', 'dev' or 'fb'

        :type: IList
        """
    @property
    def devices(self) -> IList:
        """
        Gets a list of child devices that the device is connected to.

        :type: IList
        """
    @property
    def domain(self) -> IDeviceDomain:
        """
        Gets the device's domain data. It allows for querying the device for its domain (time) values.

        :type: IDeviceDomain
        """
    @property
    def function_blocks(self) -> IList:
        """
        Gets the list of added function blocks.

        :type: IList
        """
    @property
    def info(self) -> IDeviceInfo:
        """
        Gets the device info. It contains data about the device such as the device's serial number, location, and connection string.

        :type: IDeviceInfo
        """
    @property
    def inputs_outputs_folder(self) -> IFolder:
        """
        Gets a folder containing channels.

        :type: IFolder
        """
    @property
    def signals(self) -> IList:
        """
        Gets a list of the device's signals.

        :type: IList
        """
    @property
    def signals_recursive(self) -> IList:
        """
        Gets a list of the signals that belong to the device.

        :type: IList
        """
    pass
class IInteger(IBaseObject):
    """
    Represents int number as `IInteger` interface. Use this interface to wrap integer variable when you need to add the number to lists, dictionaries and other containers which accept `IBaseObject` and derived interfaces.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IInteger: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IInteger: ...
    @property
    def value(self) -> int:
        """
        Gets an int value stored in the object.

        :type: int
        """
    pass
class IIterable(IBaseObject):
    """
    An iterable object can construct iterators and use them to iterate through items.
    """
    def __iter__(self) -> IIterator: 
        """
        Creates and returns the object's start iterator.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IIterable: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IIterable: ...
    pass
class IIterator(IBaseObject):
    """
    Interface to iterate through items of a container object.
    """
    def __next__(self) -> object: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IIterator: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IIterator: ...
    pass
class IList(IBaseObject):
    """
    Represents a heterogeneous collection of objects that can be individually accessed by index.
    """
    @typing.overload
    def __getitem__(self, arg0: int) -> object: ...
    @typing.overload
    def __getitem__(self, arg0: slice) -> IList: ...
    def __iter__(self) -> object: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def __setitem__(self, arg0: int, arg1: object) -> None: ...
    def __str__(self) -> str: ...
    def append(self, arg0: object) -> None: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IList: ...
    def clear(self) -> None: 
        """
        Removes all elements from the list.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IList: ...
    def popBack(self) -> object: ...
    def popFront(self) -> object: ...
    def pushBack(self, arg0: object) -> None: ...
    def pushFront(self, arg0: object) -> None: ...
    pass
class ILogger(IBaseObject):
    """
    Represents a collection of @ref ILoggerComponent "Logger Components" with multiple
    """
    def add_component(self, name: str) -> ILoggerComponent: 
        """
        Creates a component with a given name and adds it to the Logger object.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ILogger: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ILogger: ...
    def flush(self) -> None: 
        """
        Triggers writing out the messages stored in temporary buffers for added components and sinks associated with the Logger object.
        """
    @staticmethod
    def flush_on_level(*args, **kwargs) -> typing.Any: 
        """
        Sets the minimum severity level of messages to be automatically flushed by components of Logger object.
        """
    def get_component(self, name: str) -> ILoggerComponent: 
        """
        Gets an added component by name.
        """
    def get_or_add_component(self, name: str) -> ILoggerComponent: 
        """
        Gets an added component by name or creates a new one with a given name and adds it to the Logger object.
        """
    def remove_component(self, name: str) -> None: 
        """
        Removes the component with a given name from the Logger object.
        """
    @property
    def components(self) -> IList:
        """
        Gets a list of added components.

        :type: IList
        """
    @property
    def level(self) -> daq::LogLevel:
        """
        Gets the default log severity level. / Sets the default log severity level.

        :type: daq::LogLevel
        """
    @level.setter
    def level(self, arg1: daq::LogLevel) -> None:
        """
        Gets the default log severity level. / Sets the default log severity level.
        """
    pass
class ILoggerComponent(IBaseObject):
    """
    Logs messages produced by a specific part of openDAC SDK. The messages are written into the @ref ILoggerSink "Logger Sinks" associated with the Logger Component object.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ILoggerComponent: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ILoggerComponent: ...
    def flush(self) -> None: 
        """
        Triggers writing out the messages stored in temporary buffers.
        """
    @staticmethod
    def flush_on_level(*args, **kwargs) -> typing.Any: 
        """
        Sets the minimum severity level of messages to be automatically written to the associated sinks bypassing the temporary buffers.
        """
    @staticmethod
    def log_message(*args, **kwargs) -> typing.Any: 
        """
        Logs a message with the provided severity level.

        Logs a message with the provided source location and severity level.
        """
    @staticmethod
    def should_log(*args, **kwargs) -> typing.Any: 
        """
        Checks whether the messages with given log severity level will be logged or not.
        """
    @property
    def level(self) -> daq::LogLevel:
        """
        Gets the minimal severity level of messages to be logged by the component. / Sets the minimal severity level of messages to be logged by the component.

        :type: daq::LogLevel
        """
    @level.setter
    def level(self, arg1: daq::LogLevel) -> None:
        """
        Gets the minimal severity level of messages to be logged by the component. / Sets the minimal severity level of messages to be logged by the component.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the component.

        :type: str
        """
    @property
    def pattern(self) -> None:
        """
        Sets the custom formatter pattern for the component.

        :type: None
        """
    @pattern.setter
    def pattern(self, arg1: str) -> None:
        """
        Sets the custom formatter pattern for the component.
        """
    pass
class ILoggerSink(IBaseObject):
    """
    Represents the object that actually writes the log messages to the target. Each Logger Sink is responsible for only single target: file, console etc.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ILoggerSink: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ILoggerSink: ...
    def flush(self) -> None: 
        """
        Triggers writing out the messages from temporary buffers to the target.
        """
    def should_log(self, level: LogLevel) -> int: 
        """
        Checks whether the messages with given log severity level will be written to the target or not.
        """
    @property
    def level(self) -> LogLevel:
        """
        Gets the minimal severity level of messages to be written to the target. / Sets the minimal severity level of messages to be written to the target.

        :type: LogLevel
        """
    @level.setter
    def level(self, arg1: LogLevel) -> None:
        """
        Gets the minimal severity level of messages to be written to the target. / Sets the minimal severity level of messages to be written to the target.
        """
    @property
    def pattern(self) -> None:
        """
        Sets the custom formatter pattern for the sink.

        :type: None
        """
    @pattern.setter
    def pattern(self, arg1: str) -> None:
        """
        Sets the custom formatter pattern for the sink.
        """
    pass
class ILoggerThreadPool(IBaseObject):
    """
    Container for messages queue and backing threads used for asynchronous logging.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ILoggerThreadPool: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ILoggerThreadPool: ...
    pass
class IModule(IBaseObject):
    """
    A module is an object that provides device and function block factories. The object is usually implemented in an external dynamic link / shared library. IModuleManager is responsible for loading all modules.
    """
    def accepts_connection_parameters(self, connection_string: str, config: IPropertyObject = None) -> int: 
        """
        Checks if connection string can be used to connect to devices supported by this module and if the configuration object provided to this module is valid.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IModule: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IModule: ...
    def create_device(self, connection_string: str, parent: IComponent, config: IPropertyObject = None) -> IDevice: 
        """
        Creates a device object that can communicate with the device described in the specified connection string. The device object is not automatically added as a sub-device of the caller, but only returned by reference.
        """
    def create_function_block(self, id: str, parent: IComponent, local_id: str) -> IFunctionBlock: 
        """
        Creates and returns a function block with the specified id. The function block is not automatically added to the FB list of the caller.
        """
    def create_server(self, server_type_id: str, server_config: IPropertyObject, root_device: IDevice) -> IServer: 
        """
        Creates and returns a server with the specified server type. To prevent cyclic reference, we should not use the Instance instead of rootDevice.
        """
    @property
    def available_devices(self) -> IDict:
        """
        Returns a dictionary of devices that can be created for values, and their connection strings as keys. The implementation can start discovery in background and only return the results in this function.

        :type: IDict
        """
    @property
    def available_function_blocks(self) -> IDict:
        """
        Returns a list of known and available function blocks this module can create.

        :type: IDict
        """
    @property
    def available_servers(self) -> IDict:
        """
        Returns a dictionary of known and available servers types that this module can create.

        :type: IDict
        """
    @property
    def name(self) -> str:
        """
        Gets the module name.

        :type: str
        """
    @property
    def version_info(self) -> daq::IVersionInfo:
        """
        Retrieves the module version information.

        :type: daq::IVersionInfo
        """
    pass
class IModuleManager(IBaseObject):
    """
    Loads all available modules in a implementation-defined manner. User can also side-load custom modules via `addModule` call.
    """
    def add_module(self, module: IModule) -> None: 
        """
        Side-load a custom module in run-time from memory that was not found by default.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IModuleManager: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IModuleManager: ...
    @property
    def modules(self) -> IList:
        """
        Retrieves all modules known to the manager. Whether they were found or side-loaded.

        :type: IList
        """
    pass
class IOwnable(IBaseObject):
    """
    An ownable object can have IPropertyObject as the owner.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IOwnable: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IOwnable: ...
    @property
    def owner(self) -> None:
        """
        Sets the owner of the object.

        :type: None
        """
    @owner.setter
    def owner(self, arg1: IPropertyObject) -> None:
        """
        Sets the owner of the object.
        """
    pass
class IDataPacket(IPacket, IBaseObject):
    """
    Packet that contains data sent by a signal. The data can be either explicit, or implicit.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IDataPacket: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IDataPacket: ...
    @property
    def domain_packet(self) -> IDataPacket:
        """
        Gets the associated domain Data packet.

        :type: IDataPacket
        """
    @property
    def offset(self) -> daq::INumber:
        """
        Gets current packet offset. This offset is later applied to the data rule used by a signal to calculate actual data value. This value is usually a time or other domain value. Packet offset is particularly useful when one wants to transfer a gap in otherwise equidistant samples. If we have a linear data rule, defined by equation f(x) = k*x + n, then the fila data value will be calculated by the equation g(x) = offset + f(x).

        :type: daq::INumber
        """
    @property
    def sample_count(self) -> int:
        """
        Gets the number of samples in the packet.

        :type: int
        """
    @property
    def sample_mem_size(self) -> int:
        """
        Gets a sample memory size in bytes, calculated from data descriptor.

        :type: int
        """
    @property
    def signal_descriptor(self) -> ISignalDescriptor:
        """
        Gets the signal descriptor of the signal that sent the packet at the time of sending.

        :type: ISignalDescriptor
        """
    pass
class IPacketReader(IReader, IBaseObject):
    """
    A signal reader reads packets from a signal data stream.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPacketReader: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPacketReader: ...
    def read(self) -> IPacket: 
        """
        Retrieves the next available packet in the data-stream.
        """
    def read_all(self) -> IList: 
        """
        Retrieves all the currently available packets in the data-stream.
        """
    pass
class IProcObject(IBaseObject):
    """
    Holds a callback function without return value.
    """
    def __call__(self, *args) -> None: ...
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IProcObject: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IProcObject: ...
    pass
class IProperty(IBaseObject):
    """
    Defines a set of metadata that describes the values held by a Property object stored under the key equal to the property's name.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IProperty: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IProperty: ...
    @property
    def callable_info(self) -> ICallableInfo:
        """
        Gets the Callable information objects of the Property that specifies the argument and return types of the callable object stored as the Property value.

        :type: ICallableInfo
        """
    @property
    def coercer(self) -> ICoercer:
        """
        Gets the coercer of the Property.

        :type: ICoercer
        """
    @property
    def default_value(self) -> object:
        """
        Gets the Default value of the Property. The Default value must always be configured for a Property to be in a valid state. Exceptions are Function/Procedure and Reference properties.

        :type: object
        """
    @property
    def description(self) -> str:
        """
        Gets the short string Description of the Property.

        :type: str
        """
    @property
    def is_referenced(self) -> int:
        """
        Used to determine whether the Property is referenced by another property.

        :type: int
        """
    @property
    def item_type(self) -> CoreType:
        """
        Gets the Item type of the Property. Configured only if the Value type is `ctDict` or `ctList`. If so, the item types of the list/dictionary must match the Property's Item type.

        :type: CoreType
        """
    @property
    def key_type(self) -> CoreType:
        """
        Gets the Key type of the Property. Configured only if the Value type is `ctDict`. If so, the key type of the dictionary Property values must match the Property's Key type.

        :type: CoreType
        """
    @property
    def max_value(self) -> daq::INumber:
        """
        Gets the Maximum value of the Property. Available only if the Value type is `ctInt` or `ctFloat`.

        :type: daq::INumber
        """
    @property
    def min_value(self) -> daq::INumber:
        """
        Gets the Minimum value of the Property. Available only if the Value type is `ctInt` or `ctFloat`.

        :type: daq::INumber
        """
    @property
    def name(self) -> str:
        """
        Gets the Name of the Property. The names of Properties in a Property object must be unique. The name is used as the key to the corresponding Property value when getting/setting the value.

        :type: str
        """
    @property
    def read_only(self) -> int:
        """
        Used to determine whether the Property is a read-only property or not.

        :type: int
        """
    @property
    def referenced_property(self) -> IProperty:
        """
        Gets the referenced property. If set, all getters except for the `Name`, `Referenced property`, and `Is referenced` getters will return the value of the `Referenced property`.

        :type: IProperty
        """
    @property
    def selection_values(self) -> object:
        """
        Gets the list or dictionary of selection values. If the list/dictionary is not empty, the property is a Selection property, and must have the Value type `ctInt`.

        :type: object
        """
    @property
    def suggested_values(self) -> IList:
        """
        Gets the list of Suggested values. Contains values that are the optimal settings for the corresponding Property value. These values, however, are not enforced when setting a new Property value.

        :type: IList
        """
    @property
    def unit(self) -> IUnit:
        """
        Gets the Unit of the Property.

        :type: IUnit
        """
    @property
    def validator(self) -> IValidator:
        """
        Gets the validator of the Property.

        :type: IValidator
        """
    @property
    def value_type(self) -> CoreType:
        """
        Gets the Value type of the Property. Values written to the corresponding Property value must be of the same type.

        :type: CoreType
        """
    @property
    def visible(self) -> int:
        """
        Used to determine whether the property is visible or not.

        :type: int
        """
    pass
class IPropertyConfig(IProperty, IBaseObject):
    """
    The configuration interface of Properties. Allows for their modification until the Property is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyConfig: ...
    @property
    def callable_info(self) -> None:
        """
        Sets the Callable information objects of the Property that specifies the argument and return types of the callable object stored as the Property value.

        :type: None
        """
    @callable_info.setter
    def callable_info(self, arg1: ICallableInfo) -> None:
        """
        Sets the Callable information objects of the Property that specifies the argument and return types of the callable object stored as the Property value.
        """
    @property
    def coercer(self) -> None:
        """
        Sets the coercer of the Property.

        :type: None
        """
    @coercer.setter
    def coercer(self, arg1: ICoercer) -> None:
        """
        Sets the coercer of the Property.
        """
    @property
    def default_value(self) -> None:
        """
        Sets the Default value of the Property. The Default value must always be configured for a Property to be in a valid state. Exceptions are Function/Procedure and Reference properties.

        :type: None
        """
    @default_value.setter
    def default_value(self, arg1: object) -> None:
        """
        Sets the Default value of the Property. The Default value must always be configured for a Property to be in a valid state. Exceptions are Function/Procedure and Reference properties.
        """
    @property
    def description(self) -> None:
        """
        Sets the short string Description of the Property.

        :type: None
        """
    @description.setter
    def description(self, arg1: str) -> None:
        """
        Sets the short string Description of the Property.
        """
    @property
    def max_value(self) -> None:
        """
        Sets the Maximum value of the Property. Available only if the Value type is `ctInt` or `ctFloat`.

        :type: None
        """
    @max_value.setter
    def max_value(self, arg1: daq::INumber) -> None:
        """
        Sets the Maximum value of the Property. Available only if the Value type is `ctInt` or `ctFloat`.
        """
    @property
    def min_value(self) -> None:
        """
        Sets the Minimum value of the Property. Available only if the Value type is `ctInt` or `ctFloat`.

        :type: None
        """
    @min_value.setter
    def min_value(self, arg1: daq::INumber) -> None:
        """
        Sets the Minimum value of the Property. Available only if the Value type is `ctInt` or `ctFloat`.
        """
    @property
    def name(self) -> None:
        """
        Sets the Name of the Property. The names of Properties in a Property object must be unique. The name is used as the key to the corresponding Property value when getting/setting the value.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the Name of the Property. The names of Properties in a Property object must be unique. The name is used as the key to the corresponding Property value when getting/setting the value.
        """
    @property
    def read_only(self) -> None:
        """
        Used to determine whether the Property is a read-only property or not.

        :type: None
        """
    @read_only.setter
    def read_only(self, arg1: IBoolean) -> None:
        """
        Used to determine whether the Property is a read-only property or not.
        """
    @property
    def referenced_property(self) -> None:
        """
        Sets the referenced property. If set, all getters except for the `Name`, `Referenced property`, and `Is referenced` getters will return the value of the `Referenced property`.

        :type: None
        """
    @referenced_property.setter
    def referenced_property(self, arg1: IEvalValue) -> None:
        """
        Sets the referenced property. If set, all getters except for the `Name`, `Referenced property`, and `Is referenced` getters will return the value of the `Referenced property`.
        """
    @property
    def selection_values(self) -> None:
        """
        Sets the list or dictionary of selection values. If the list/dictionary is not empty, the property is a Selection property, and must have the Value type `ctInt`.

        :type: None
        """
    @selection_values.setter
    def selection_values(self, arg1: object) -> None:
        """
        Sets the list or dictionary of selection values. If the list/dictionary is not empty, the property is a Selection property, and must have the Value type `ctInt`.
        """
    @property
    def suggested_values(self) -> None:
        """
        Sets the list of Suggested values. Contains values that are the optimal settings for the corresponding Property value. These values, however, are not enforced when setting a new Property value.

        :type: None
        """
    @suggested_values.setter
    def suggested_values(self, arg1: IList) -> None:
        """
        Sets the list of Suggested values. Contains values that are the optimal settings for the corresponding Property value. These values, however, are not enforced when setting a new Property value.
        """
    @property
    def unit(self) -> None:
        """
        Sets the Unit of the Property.

        :type: None
        """
    @unit.setter
    def unit(self, arg1: IUnit) -> None:
        """
        Sets the Unit of the Property.
        """
    @property
    def validator(self) -> None:
        """
        Sets the validator of the Property.

        :type: None
        """
    @validator.setter
    def validator(self, arg1: IValidator) -> None:
        """
        Sets the validator of the Property.
        """
    @property
    def value_type(self) -> None:
        """
        Sets the Value type of the Property. Values written to the corresponding Property value must be of the same type.

        :type: None
        """
    @value_type.setter
    def value_type(self, arg1: CoreType) -> None:
        """
        Sets the Value type of the Property. Values written to the corresponding Property value must be of the same type.
        """
    @property
    def visible(self) -> None:
        """
        Used to determine whether the property is visible or not.

        :type: None
        """
    @visible.setter
    def visible(self, arg1: IBoolean) -> None:
        """
        Used to determine whether the property is visible or not.
        """
    pass
class IInstance(IDevice, IFolder, IComponent, IPropertyObject, IBaseObject):
    """
    The top-level openDAQ object. It acts as container for the openDAQ context and the base module manager.
    """
    def add_server(self, server_type_id: str, server_config: IPropertyObject) -> IServer: 
        """
        Creates and adds a server with the provided serverType and configuration.
        """
    def add_standard_servers(self) -> IList: 
        """
        Creates and adds servers of types "openDAQ WebsocketTcp" and "openDAQ OpcUa" with default configurations.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IInstance: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IInstance: ...
    def find_component(self, component: IComponent, id: str) -> IComponent: 
        """
        Finds the component (signal/device/function block) with the specified (global) id.
        """
    def remove_server(self, server: IServer) -> None: 
        """
        Removes the server provided as argument.
        """
    @property
    def available_servers(self) -> IDict:
        """
        Get a dictionary of available servers as <IString, IServerType> pairs

        :type: IDict
        """
    @property
    def context(self) -> IContext:
        """
        Gets the Context.

        :type: IContext
        """
    @property
    def module_manager(self) -> IModuleManager:
        """
        Gets the Module manager.

        :type: IModuleManager
        """
    @property
    def root_device(self) -> IDevice:
        """
        Gets the current root device. / Sets the current root device.

        :type: IDevice
        """
    @root_device.setter
    def root_device(self, arg1: IDevice) -> None:
        """
        Gets the current root device. / Sets the current root device.
        """
    @property
    def servers(self) -> IList:
        """
        Get list of added servers.

        :type: IList
        """
    pass
class IPropertyObjectClass(IBaseObject):
    """
    Container of properties that can be used as a base class when instantiating a Property object.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyObjectClass: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyObjectClass: ...
    def get_properties(self, include_inherited: bool) -> IList: 
        """
        Gets the list of properties added to the class.
        """
    def get_property(self, property_name: str) -> IProperty: 
        """
        Gets the class's property with the given name.
        """
    def has_property(self, property_name: str) -> int: 
        """
        Checks if the property is registered.
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the property class.

        :type: str
        """
    @property
    def parent_name(self) -> str:
        """
        Gets the name of the parent of the property class.

        :type: str
        """
    pass
class IPropertyObjectClassConfig(IPropertyObjectClass, IBaseObject):
    """
    The configuration interface of Property object classes. Allows for their modification until the class is frozen.
    """
    def add_property(self, property: IProperty) -> None: 
        """
        Adds a property to the class.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyObjectClassConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyObjectClassConfig: ...
    def remove_property(self, property_name: str) -> None: 
        """
        Removes a property with the given name from the class.
        """
    @property
    def name(self) -> None:
        """
        Sets the name of the property class.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the name of the property class.
        """
    @property
    def parent_name(self) -> None:
        """
        Gets the name of the parent of the property class.

        :type: None
        """
    @parent_name.setter
    def parent_name(self, arg1: str) -> None:
        """
        Gets the name of the parent of the property class.
        """
    @property
    def property_order(self) -> None:
        """
        Sets a custom order of properties as defined in the list of property names.

        :type: None
        """
    @property_order.setter
    def property_order(self, arg1: IList) -> None:
        """
        Sets a custom order of properties as defined in the list of property names.
        """
    pass
class IPropertyObjectClassManager(IBaseObject):
    """
    Container for Property object classes. For a Property object class to be used in the creation of a Property object, it must be added to the Property object class manager.
    """
    def add_class(self, property_object_class: IPropertyObjectClass) -> None: 
        """
        Adds a property class to the manager.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyObjectClassManager: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyObjectClassManager: ...
    def get_class(self, name: str) -> IPropertyObjectClass: 
        """
        Gets an added class by name.
        """
    def remove_class(self, name: str) -> None: 
        """
        Removes the property class from property manager.
        """
    @property
    def classes(self) -> IList:
        """
        Gets a list of all added classes.

        :type: IList
        """
    pass
class IPropertyObjectProtected(IBaseObject):
    """
    Provides protected access that allows changing read-only property values of a Property object.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyObjectProtected: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyObjectProtected: ...
    def set_protected_property_value(self, property_name: str, value: object) -> None: 
        """
        Sets a property value. Does not fail if the property is read-only.
        """
    pass
class IPropertyValueEventArgs(IEventArgs, IBaseObject):
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IPropertyValueEventArgs: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IPropertyValueEventArgs: ...
    @property
    def property(self) -> IProperty:
        """
        :type: IProperty
        """
    @property
    def property_event_type(self) -> PropertyEventType:
        """
        :type: PropertyEventType
        """
    @property
    def value(self) -> object:
        """
        :type: object
        """
    @value.setter
    def value(self, arg1: object) -> None:
        pass
    pass
class IRange(IBaseObject):
    """
    Describes a range of values between the `lowValue` and `highValue` boundaries
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IRange: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IRange: ...
    @property
    def high_value(self) -> daq::INumber:
        """
        Gets the upper boundary value of the range.

        :type: daq::INumber
        """
    @property
    def low_value(self) -> daq::INumber:
        """
        Gets the lower boundary value of the range.

        :type: daq::INumber
        """
    pass
class IRatio(IBaseObject):
    """
    Represents rational number as `IRatio` interface. Use this interface to wrap rational number when you need to add the number to lists, dictionaries and other containers which accept `IBaseObject` and derived interfaces. Rational numbers are defined as numerator / denominator.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IRatio: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IRatio: ...
    def simplify(self) -> None: 
        """
        Simplifies rational number if possible.
        """
    @property
    def denominator(self) -> int:
        """
        Gets denominator part.

        :type: int
        """
    @property
    def numerator(self) -> int:
        """
        Gets numerator part.

        :type: int
        """
    pass
class ISampleReader(IReader, IBaseObject):
    """
    A basic signal reader that simplifies reading the signals's samples.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ISampleReader: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ISampleReader: ...
    @property
    def domain_read_type(self) -> daq::SampleType:
        """
        Gets the sample-type the signal domain samples will be converted to when read or @c SampleType::Invalid if read-type has not been determined yet.

        :type: daq::SampleType
        """
    @property
    def domain_transform_function(self) -> None:
        """
        Sets the transform function that will be called with the read domain-data and currently valid Signal-Descriptor giving the user the chance add a custom post-processing step. The function should have a signature compatible with:

        :type: None
        """
    @domain_transform_function.setter
    def domain_transform_function(self, arg1: daq::IFunction) -> None:
        """
        Sets the transform function that will be called with the read domain-data and currently valid Signal-Descriptor giving the user the chance add a custom post-processing step. The function should have a signature compatible with:
        """
    @property
    def value_read_type(self) -> daq::SampleType:
        """
        Gets the sample-type the signal value samples will be converted to when read or @c SampleType::Invalid if read-type has not been determined yet.

        :type: daq::SampleType
        """
    @property
    def value_transform_function(self) -> None:
        """
        Sets the transform function that will be called with the read value-data and currently valid Signal-Descriptor giving the user the chance add a custom post-processing step. The function should have a signature compatible with:

        :type: None
        """
    @value_transform_function.setter
    def value_transform_function(self, arg1: daq::IFunction) -> None:
        """
        Sets the transform function that will be called with the read value-data and currently valid Signal-Descriptor giving the user the chance add a custom post-processing step. The function should have a signature compatible with:
        """
    pass
class IRemovable(IBaseObject):
    """
    Allows the component to be notified when it is removed.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IRemovable: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IRemovable: ...
    def remove(self) -> None: 
        """
        Notifies the component that it is being removed.
        """
    @property
    def removed(self) -> int:
        """
        Returns True if component was removed.

        :type: int
        """
    pass
class IBlockReader(ISampleReader, IReader, IBaseObject):
    """
    A signal data reader that abstracts away reading of signal packets by keeping an internal read-position and automatically advances it on subsequent reads. The difference to a StreamReader is that instead of reading on per sample basis it always returns only a full block of samples. This means that even if more samples are available they will not be read until there is enough of them to fill at least one block.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IBlockReader: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IBlockReader: ...
    pass
class IScaling(IBaseObject):
    """
    Signal descriptor field that defines a scaling transformation, which should be applied to data carried by the signal's packets when read.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IScaling: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IScaling: ...
    @property
    def input_sample_type(self) -> daq::SampleType:
        """
        Gets the scaling's input data type.

        :type: daq::SampleType
        """
    @property
    def output_sample_type(self) -> daq::ScaledSampleType:
        """
        Gets the scaling's output data type.

        :type: daq::ScaledSampleType
        """
    @property
    def parameters(self) -> IDict:
        """
        Gets the dictionary of parameters that are used to calculate the scaling in conjunction with the input data.

        :type: IDict
        """
    @property
    def type(self) -> ScalingType:
        """
        Gets the type of the scaling that determines how the scaling parameters should be interpreted and how the scaling should be calculated.

        :type: ScalingType
        """
    pass
class IScalingConfig(IScaling, IBaseObject):
    """
    Configuration component of Scaling objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IScalingConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IScalingConfig: ...
    @property
    def input_data_type(self) -> None:
        """
        Sets the scaling's input data type.

        :type: None
        """
    @input_data_type.setter
    def input_data_type(self, arg1: daq::SampleType) -> None:
        """
        Sets the scaling's input data type.
        """
    @property
    def output_data_type(self) -> None:
        """
        Sets the scaling's output data type.

        :type: None
        """
    @output_data_type.setter
    def output_data_type(self, arg1: daq::ScaledSampleType) -> None:
        """
        Sets the scaling's output data type.
        """
    @property
    def parameters(self) -> None:
        """
        Gets the list of parameters that are used to calculate the scaling in conjunction with the input data.

        :type: None
        """
    @parameters.setter
    def parameters(self, arg1: IDict) -> None:
        """
        Gets the list of parameters that are used to calculate the scaling in conjunction with the input data.
        """
    @property
    def scaling_type(self) -> None:
        """
        Sets the type of the scaling that determines how the scaling parameters should be interpreted and how the scaling should be calculated.

        :type: None
        """
    @scaling_type.setter
    def scaling_type(self, arg1: ScalingType) -> None:
        """
        Sets the type of the scaling that determines how the scaling parameters should be interpreted and how the scaling should be calculated.
        """
    pass
class IScheduler(IBaseObject):
    """
    A thread-pool scheduler that supports scheduling one-off functions as well as dependency graphs.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IScheduler: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IScheduler: ...
    def schedule_graph(self, graph: ITaskGraph) -> IAwaitable: 
        """
        Schedules the specified dependency @p graph to run on the thread-pool. The call does not block but immediately returns an @p awaitable that represents the asynchronous execution. It can be waited upon and queried for status and result. <b>Any exceptions that occur during the graph execution are silently ignored.</b>
        """
    @staticmethod
    def schedule_work(*args, **kwargs) -> typing.Any: 
        """
        Schedules the specified @p work function to run on the thread-pool. The call does not block but immediately returns an @p awaitable that represents the asynchronous execution. It can be waited upon and queried for status and result.
        """
    def stop(self) -> None: 
        """
        Cancels all outstanding work and waits for the remaining to complete. After this point the scheduler does not allow any new work or graphs for scheduling.
        """
    def wait_all(self) -> None: 
        """
        Waits fo all current scheduled work and tasks to complete.
        """
    @property
    def multi_threaded(self) -> int:
        """
        Returns whether more than one worker thread is used.

        :type: int
        """
    pass
class IServer(IBaseObject):
    """
    Represents a server. The server provides access to the openDAQ device. Depend of the implementation, it can support configuring the device, reading configuration, and data streaming.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IServer: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IServer: ...
    def stop(self) -> None: 
        """
        Stops the server. This is called when we remove the server from the Instance or Instance is closing.
        """
    def update_root_device(self, root_device: IDevice) -> None: 
        """
        A function is called when root device on Instance is changed (Instance::setRootDevice). In that case, server needs to rebuild the structure.
        """
    pass
class IServerType(IBaseObject):
    """
    Provides information about the server.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IServerType: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IServerType: ...
    def create_default_config(self) -> IPropertyObject: 
        """
        The function creates and returns default configuration. On each call, we need to create new object, because we want that each instance of the server has its own configuration object.
        """
    @property
    def description(self) -> str:
        """
        Gets the description of a server.

        :type: str
        """
    @property
    def id(self) -> str:
        """
        Gets the unique server type id.

        :type: str
        """
    @property
    def name(self) -> str:
        """
        Gets the user-friendly name of a server.

        :type: str
        """
    pass
class IServerTypeConfig(IServerType, IBaseObject):
    """
    Configuration component of Server info objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IServerTypeConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IServerTypeConfig: ...
    @property
    def create_default_config_callback(self) -> None:
        """
        Sets the callback, which is called, when user want to create new default configuration object. Callback needs to create and return property object.

        :type: None
        """
    @create_default_config_callback.setter
    def create_default_config_callback(self, arg1: daq::IFunction) -> None:
        """
        Sets the callback, which is called, when user want to create new default configuration object. Callback needs to create and return property object.
        """
    @property
    def description(self) -> None:
        """
        Sets the description of a server.

        :type: None
        """
    @description.setter
    def description(self, arg1: str) -> None:
        """
        Sets the description of a server.
        """
    @property
    def id(self) -> None:
        """
        Sets the server type id. For example 'OpcUA-TMS'

        :type: None
        """
    @id.setter
    def id(self, arg1: str) -> None:
        """
        Sets the server type id. For example 'OpcUA-TMS'
        """
    @property
    def name(self) -> None:
        """
        Sets the user-friendly name of a server.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the user-friendly name of a server.
        """
    pass
class ISignal(IComponent, IPropertyObject, IBaseObject):
    """
    A signal with an unique ID that sends event/data packets through connections to input ports the signal is connected to.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ISignal: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ISignal: ...
    @property
    def connections(self) -> IList:
        """
        Gets the list of connections to input ports formed by the signal.

        :type: IList
        """
    @property
    def descriptor(self) -> ISignalDescriptor:
        """
        Gets the signal's descriptor.

        :type: ISignalDescriptor
        """
    @property
    def domain_signal(self) -> ISignal:
        """
        Gets the signal that carries its domain data.

        :type: ISignal
        """
    @property
    def public(self) -> int:
        """
        Returns true if the signal is public; false otherwise. / Sets the signal to be either public or private.

        :type: int
        """
    @public.setter
    def public(self, arg1: bool) -> None:
        """
        Returns true if the signal is public; false otherwise. / Sets the signal to be either public or private.
        """
    @property
    def related_signals(self) -> IList:
        """
        Gets a list of related signals.

        :type: IList
        """
    pass
class ISignalConfig(ISignal, IComponent, IPropertyObject, IBaseObject):
    """
    The configuration component of a Signal. Allows for configuration of its properties and sending packets through its connections.
    """
    def add_related_signal(self, signal: ISignal) -> None: 
        """
        Adds a related signal to the list of related signals.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ISignalConfig: ...
    def clear_related_signals(self) -> None: 
        """
        Clears the list of related signals.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ISignalConfig: ...
    def remove_related_signal(self, signal: ISignal) -> None: 
        """
        Removes a signal from the list of related signal.
        """
    def send_packet(self, packet: IPacket) -> None: 
        """
        Sends a packet through all connections of the signal.
        """
    @property
    def descriptor(self) -> None:
        """
        Sets the signal descriptor.

        :type: None
        """
    @descriptor.setter
    def descriptor(self, arg1: ISignalDescriptor) -> None:
        """
        Sets the signal descriptor.
        """
    @property
    def domain_signal(self) -> None:
        """
        Sets the domain signal reference.

        :type: None
        """
    @domain_signal.setter
    def domain_signal(self, arg1: ISignal) -> None:
        """
        Sets the domain signal reference.
        """
    @property
    def related_signals(self) -> None:
        """
        Sets the list of related signals.

        :type: None
        """
    @related_signals.setter
    def related_signals(self, arg1: IList) -> None:
        """
        Sets the list of related signals.
        """
    pass
class ISignalDescriptor(IBaseObject):
    """
    Object containing information about the data of a signal component (either value or domain).
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ISignalDescriptor: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ISignalDescriptor: ...
    @property
    def data_descriptor(self) -> IDataDescriptor:
        """
        Gets the Data descriptor.

        :type: IDataDescriptor
        """
    @property
    def description(self) -> str:
        """
        Gets a short description of the signal.

        :type: str
        """
    @property
    def metadata(self) -> IDict:
        """
        Gets any extra metadata defined by the signal descriptor.

        :type: IDict
        """
    @property
    def name(self) -> str:
        """
        Gets the name of the signal.

        :type: str
        """
    @property
    def tags(self) -> ITags:
        """
        Gets the `Tags` object that contains a list of string tags of the signal. The object allows for inspection and querying of tags.

        :type: ITags
        """
    pass
class ISignalDescriptorConfig(ISignalDescriptor, IBaseObject):
    """
    Configuration component of Signal descriptor objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ISignalDescriptorConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ISignalDescriptorConfig: ...
    @property
    def data_descriptor(self) -> None:
        """
        Sets the Data descriptor.

        :type: None
        """
    @data_descriptor.setter
    def data_descriptor(self, arg1: IDataDescriptor) -> None:
        """
        Sets the Data descriptor.
        """
    @property
    def description(self) -> None:
        """
        Gets a short description of the signal.

        :type: None
        """
    @description.setter
    def description(self, arg1: str) -> None:
        """
        Gets a short description of the signal.
        """
    @property
    def metadata(self) -> None:
        """
        Sets any extra metadata defined by the signal descriptor.

        :type: None
        """
    @metadata.setter
    def metadata(self, arg1: IDict) -> None:
        """
        Sets any extra metadata defined by the signal descriptor.
        """
    @property
    def name(self) -> None:
        """
        Gets the name of the signal.

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Gets the name of the signal.
        """
    @property
    def tags(self) -> None:
        """
        Gets the `Tags` object that contains a list of string tags of the signal. The object allows for inspection and querying of tags.

        :type: None
        """
    @tags.setter
    def tags(self, arg1: ITags) -> None:
        """
        Gets the `Tags` object that contains a list of string tags of the signal. The object allows for inspection and querying of tags.
        """
    pass
class ISignalEvents(IBaseObject):
    """
    Internal functions of a signal containing event methods that are called on certain events. Eg. when a signal is connected to an input port, or when a signal is used as a domain signal of another.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ISignalEvents: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ISignalEvents: ...
    def domain_signal_reference_removed(self, signal: ISignal) -> None: 
        """
        Notifies the signal that it is no longer being used as a domain signal by the signal passed as the function argument.
        """
    def domain_signal_reference_set(self, signal: ISignal) -> None: 
        """
        Notifies the signal that it is being used as a domain signal by the signal passed as the function argument.
        """
    def listener_connected(self, connection: IConnection) -> None: 
        """
        Notifies the signal that it has been connected to an input port forming a new connection.
        """
    def listener_disconnected(self, connection: IConnection) -> None: 
        """
        Notifies the signal that it has been disconnected from an input port with the given connection.
        """
    pass
class IStreamReader(ISampleReader, IReader, IBaseObject):
    """
    A signal data reader that abstracts away reading of signal packets by keeping an internal read-position and automatically advances it on subsequent reads.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IStreamReader: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IStreamReader: ...
    def read(self, count: int, timeout_ms: int = 0) -> numpy.ndarray[numpy.float64]: 
        """
        Copies at maximum the next `count` unread samples to the values buffer. The amount actually read is returned through the `count` parameter.
        """
    def read_with_domain(self, count: int, timeout_ms: int = 0) -> tuple: 
        """
        Copies at maximum the next `count` unread samples and clock-stamps to the `values` and `stamps` buffers. The amount actually read is returned through the `count` parameter.
        """
    def read_with_timestamps(self, count: int, timeout_ms: int = 0) -> tuple: 
        """
        Copies at maximum the next `count` unread samples and clock-stamps to the `values` and `stamps` buffers. The amount actually read is returned through the `count` parameter. The domain data is returned in timestamp format.
        """
    pass
class IString(IBaseObject):
    """
    Represents string variable as `IString` interface. Use this interface to wrap string variable when you need to add the variable to lists, dictionaries and other containers which accept `IBaseObject` and derived interfaces.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IString: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IString: ...
    @property
    def length(self) -> int:
        """
        Gets length of string.

        :type: int
        """
    pass
class ITags(IBaseObject):
    """
    List of string tags. Provides helpers to get and search the list of tags.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ITags: ...
    def contains(self, name: str) -> int: 
        """
        Checks whether a tag is present in the list of tags.
        """
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ITags: ...
    def query(self, query: str) -> int: 
        """
        Queries the list of tags, creating an EvalValue expression from the `query` string. Returns true if the list of tags matches the query, false otherwise.
        """
    @property
    def list(self) -> IList:
        """
        Gets the list of all tags in the list.

        :type: IList
        """
    pass
class ITagsConfig(ITags, IBaseObject):
    def add(self, name: str) -> None: 
        """
        Adds a new tag to the list.
        """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ITagsConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ITagsConfig: ...
    def remove(self, name: str) -> None: 
        """
        Removes a new tag from the list.
        """
    pass
class ITailReader(ISampleReader, IReader, IBaseObject):
    """
    A reader that only ever reads the last N samples, subsequent calls may result in overlapping data.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ITailReader: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ITailReader: ...
    def read(self, count: int) -> numpy.ndarray[numpy.float64]: 
        """
        Copies at maximum the next `count` unread samples to the values buffer. The amount actually read is returned through the `count` parameter.
        """
    def read_with_domain(self, count: int) -> tuple: 
        """
        Copies at maximum the next `count` unread samples and clock-stamps to the `values` and `stamps` buffers. The amount actually read is returned through the `count` parameter.
        """
    @property
    def history_size(self) -> int:
        """
        The maximum amount of samples in history to keep.

        :type: int
        """
    pass
class ITask(IBaseObject):
    """
    A packaged callback with possible continuations and dependencies that can be arranged in a dependency graph (directed acyclic graph). The task is not executed directly but only when the graph is scheduled for execution and all dependencies have been satisfied.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ITask: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ITask: ...
    def then(self, continuation: ITask) -> None: 
        """
        Sets the continuation to only execute after this task completes. Be careful of forming cycles as tasks whose dependencies cannot be satisfied will never execute.
        """
    @property
    def name(self) -> str:
        """
        Gets the task name. / Sets the task name that is used in diagnostics.

        :type: str
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Gets the task name. / Sets the task name that is used in diagnostics.
        """
    pass
class ITaskGraph(ITask, IBaseObject):
    """
    A dependency graph (directed acyclic graph) of tasks that can be scheduled for execution on a Scheduler.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> ITaskGraph: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> ITaskGraph: ...
    pass
class IUnit(IBaseObject):
    """
    Describes a measurement unit with IDs as defined in <a href="https://unece.org/trade/cefact/UNLOCODE-Download">Codes for Units of Measurement used in International Trade</a>.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IUnit: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IUnit: ...
    @property
    def id(self) -> int:
        """
        Gets the unit ID as defined in <a href="https://unece.org/trade/cefact/UNLOCODE-Download">Codes for Units of Measurement used in International Trade</a>.

        :type: int
        """
    @property
    def name(self) -> str:
        """
        Gets the full name of the unit, i.e. "meters per second".

        :type: str
        """
    @property
    def quantity(self) -> str:
        """
        Gets the quantity represented by the unit, i.e. "Velocity"

        :type: str
        """
    @property
    def symbol(self) -> str:
        """
        Gets the symbol of the unit, i.e. "m/s".

        :type: str
        """
    pass
class IUnitConfig(IUnit, IBaseObject):
    """
    Configuration component of Unit objects. Contains setter methods that are available until the object is frozen.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IUnitConfig: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IUnitConfig: ...
    @property
    def id(self) -> None:
        """
        Sets the unit ID as defined in <a href="https://unece.org/trade/cefact/UNLOCODE-Download">Codes for Units of Measurement used in International Trade</a>.

        :type: None
        """
    @id.setter
    def id(self, arg1: int) -> None:
        """
        Sets the unit ID as defined in <a href="https://unece.org/trade/cefact/UNLOCODE-Download">Codes for Units of Measurement used in International Trade</a>.
        """
    @property
    def name(self) -> None:
        """
        Sets the full name of the unit, i.e. "meters per second".

        :type: None
        """
    @name.setter
    def name(self, arg1: str) -> None:
        """
        Sets the full name of the unit, i.e. "meters per second".
        """
    @property
    def quantity(self) -> None:
        """
        Sets the quantity represented by the unit, i.e. "Velocity"

        :type: None
        """
    @quantity.setter
    def quantity(self, arg1: str) -> None:
        """
        Sets the quantity represented by the unit, i.e. "Velocity"
        """
    @property
    def symbol(self) -> None:
        """
        Sets the symbol of the unit, i.e. "m/s".

        :type: None
        """
    @symbol.setter
    def symbol(self, arg1: str) -> None:
        """
        Sets the symbol of the unit, i.e. "m/s".
        """
    pass
class IValidator(IBaseObject):
    """
    Used by openDAQ properties to validate whether a value fits the value restrictions of the Property.
    """
    @staticmethod
    def can_cast_from(arg0: IBaseObject) -> bool: ...
    @staticmethod
    def cast_from(arg0: IBaseObject) -> IValidator: ...
    @staticmethod
    def convert_from(arg0: IBaseObject) -> IValidator: ...
    def validate(self, prop_obj: object, value: object) -> None: 
        """
        Checks whether `value` adheres to the validity conditions of the validator.
        """
    @property
    def eval(self) -> str:
        """
        Gets the string expression used when creating the validator.

        :type: str
        """
    pass
class LogLevel():
    """
    Members:

      Trace

      Debug

      Info

      Warn

      Error

      Critical

      Off

      Default
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Critical: opendaq._opendaq.LogLevel # value = <LogLevel.Critical: 5>
    Debug: opendaq._opendaq.LogLevel # value = <LogLevel.Debug: 1>
    Default: opendaq._opendaq.LogLevel # value = <LogLevel.Default: 7>
    Error: opendaq._opendaq.LogLevel # value = <LogLevel.Error: 4>
    Info: opendaq._opendaq.LogLevel # value = <LogLevel.Info: 2>
    Off: opendaq._opendaq.LogLevel # value = <LogLevel.Off: 6>
    Trace: opendaq._opendaq.LogLevel # value = <LogLevel.Trace: 0>
    Warn: opendaq._opendaq.LogLevel # value = <LogLevel.Warn: 3>
    __members__: dict # value = {'Trace': <LogLevel.Trace: 0>, 'Debug': <LogLevel.Debug: 1>, 'Info': <LogLevel.Info: 2>, 'Warn': <LogLevel.Warn: 3>, 'Error': <LogLevel.Error: 4>, 'Critical': <LogLevel.Critical: 5>, 'Off': <LogLevel.Off: 6>, 'Default': <LogLevel.Default: 7>}
    pass
class PacketReadyNotification():
    """
    Members:

      None

      SameThread

      Scheduler
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    None: opendaq._opendaq.PacketReadyNotification # value = <PacketReadyNotification.None: 0>
    SameThread: opendaq._opendaq.PacketReadyNotification # value = <PacketReadyNotification.SameThread: 1>
    Scheduler: opendaq._opendaq.PacketReadyNotification # value = <PacketReadyNotification.Scheduler: 2>
    __members__: dict # value = {'None': <PacketReadyNotification.None: 0>, 'SameThread': <PacketReadyNotification.SameThread: 1>, 'Scheduler': <PacketReadyNotification.Scheduler: 2>}
    pass
class PacketType():
    """
    Members:

      None

      Data

      Event
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Data: opendaq._opendaq.PacketType # value = <PacketType.Data: 1>
    Event: opendaq._opendaq.PacketType # value = <PacketType.Event: 2>
    None: opendaq._opendaq.PacketType # value = <PacketType.None: 0>
    __members__: dict # value = {'None': <PacketType.None: 0>, 'Data': <PacketType.Data: 1>, 'Event': <PacketType.Event: 2>}
    pass
class PropertyEventType():
    """
    Members:

      Update

      Clear

      Read
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Clear: opendaq._opendaq.PropertyEventType # value = <PropertyEventType.Clear: 1>
    Read: opendaq._opendaq.PropertyEventType # value = <PropertyEventType.Read: 2>
    Update: opendaq._opendaq.PropertyEventType # value = <PropertyEventType.Update: 0>
    __members__: dict # value = {'Update': <PropertyEventType.Update: 0>, 'Clear': <PropertyEventType.Clear: 1>, 'Read': <PropertyEventType.Read: 2>}
    pass
class ReadTimeoutType():
    """
    Members:

      Any

      All
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    All: opendaq._opendaq.ReadTimeoutType # value = <ReadTimeoutType.All: 1>
    Any: opendaq._opendaq.ReadTimeoutType # value = <ReadTimeoutType.Any: 0>
    __members__: dict # value = {'Any': <ReadTimeoutType.Any: 0>, 'All': <ReadTimeoutType.All: 1>}
    pass
class ScalingType():
    """
    Members:

      Other

      Linear
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Linear: opendaq._opendaq.ScalingType # value = <ScalingType.Linear: 1>
    Other: opendaq._opendaq.ScalingType # value = <ScalingType.Other: 0>
    __members__: dict # value = {'Other': <ScalingType.Other: 0>, 'Linear': <ScalingType.Linear: 1>}
    pass
def ArgumentInfo(arg0: IString, arg1: CoreType) -> IArgumentInfo:
    pass
def BaseObject() -> IBaseObject:
    pass
def BasicFileLoggerSink(arg0: IString) -> ILoggerSink:
    pass
def BlockReader(*args, **kwargs) -> typing.Any:
    pass
def BlockReaderFromExisting(*args, **kwargs) -> typing.Any:
    pass
def BoolProperty(arg0: IString, arg1: IBoolean, arg2: IBoolean) -> IProperty:
    pass
def Boolean(value: bool) -> IBoolean:
    """
    Creates a new Boolean.
    """
def CallableInfo(arg0: IList, arg1: CoreType) -> ICallableInfo:
    pass
def Client(arg0: IContext, arg1: IModuleManager, arg2: IString) -> IDevice:
    pass
def Coercer(arg0: IString) -> ICoercer:
    pass
@typing.overload
def ComplexNumber(real: float, imaginary: float) -> IComplexNumber:
    """
    Creates a new ComplexNumber object.

    Creates a new ComplexNumber object.
    """
@typing.overload
def ComplexNumber(value: complex) -> IComplexNumber:
    pass
def Component(arg0: IContext, arg1: IComponent, arg2: IString, arg3: IString) -> IComponent:
    pass
def Connection(arg0: IInputPort, arg1: ISignal, arg2: IContext) -> IConnection:
    pass
def ConstantDataRule(*args, **kwargs) -> typing.Any:
    pass
def Context(arg0: IScheduler, arg1: ILogger, arg2: IPropertyObjectClassManager) -> IContext:
    pass
def DataDescriptor() -> IDataDescriptorConfig:
    pass
def DataDescriptorFromExisting(arg0: IDataDescriptor) -> IDataDescriptorConfig:
    pass
def DataPacket(*args, **kwargs) -> typing.Any:
    pass
def DataPacketWithDomain(*args, **kwargs) -> typing.Any:
    pass
def DataRule() -> IDataRuleConfig:
    pass
def DataRuleFromExisting(arg0: IDataRule) -> IDataRuleConfig:
    pass
def DeviceInfoConfig(arg0: IString, arg1: IString) -> IDeviceInfoConfig:
    pass
def Dict() -> IDict:
    pass
def DictProperty(arg0: IString, arg1: IDict, arg2: IBoolean) -> IProperty:
    pass
def Dimension() -> IDimensionConfig:
    pass
def DimensionFromExisting(arg0: IDimension) -> IDimensionConfig:
    pass
def DimensionFromRule(arg0: IDimensionRule, arg1: IUnit, arg2: IString) -> IDimension:
    pass
def DimensionRule() -> IDimensionRuleConfig:
    pass
def DimensionRuleFromExisting(arg0: IDimensionRule) -> IDimensionRuleConfig:
    pass
def EvalValue(arg0: IString) -> IEvalValue:
    pass
def EvalValueArgs(arg0: IString, arg1: IList) -> IEvalValue:
    pass
def EvalValueFunc(*args, **kwargs) -> typing.Any:
    pass
def EventArgs(arg0: int, arg1: IString) -> IEventArgs:
    pass
def EventPacket(arg0: IString, arg1: IDict) -> IEventPacket:
    pass
def ExplicitDataRule() -> IDataRule:
    pass
def ExternalAllocator(*args, **kwargs) -> typing.Any:
    pass
def Float(arg0: float) -> IFloat:
    pass
def FloatProperty(arg0: IString, arg1: IFloat, arg2: IBoolean) -> IProperty:
    pass
def Folder(arg0: IContext, arg1: IComponent, arg2: IString) -> IFolderConfig:
    pass
def FolderWithItemType(*args, **kwargs) -> typing.Any:
    pass
def FunctionBlockType(arg0: IString, arg1: IString, arg2: IString) -> IFunctionBlockType:
    pass
def FunctionProperty(arg0: IString, arg1: ICallableInfo, arg2: IBoolean) -> IProperty:
    pass
def InputPort(arg0: IContext, arg1: IComponent, arg2: IString) -> IInputPortConfig:
    pass
@typing.overload
def Instance(arg0: IContext, arg1: IModuleManager, arg2: IString) -> IInstance:
    """
    Creates a new Instance, using the default logger and module manager. The module manager searches for module shared libraries at the given module path, using the executable directory if left empty.
    """
@typing.overload
def Instance(module_path: str = '', local_id: str = '') -> IInstance:
    pass
def IntProperty(arg0: IString, arg1: IInteger, arg2: IBoolean) -> IProperty:
    pass
def Integer(arg0: int) -> IInteger:
    pass
def IoFolder(arg0: IContext, arg1: IComponent, arg2: IString) -> IFolderConfig:
    pass
def LinearDataRule(*args, **kwargs) -> typing.Any:
    pass
def LinearDimensionRule(*args, **kwargs) -> typing.Any:
    pass
def LinearScaling(*args, **kwargs) -> typing.Any:
    pass
def List() -> IList:
    pass
def ListDimensionRule(arg0: IList) -> IDimensionRule:
    pass
def ListProperty(arg0: IString, arg1: IList, arg2: IBoolean) -> IProperty:
    pass
def LogarithmicDimensionRule(*args, **kwargs) -> typing.Any:
    pass
def Logger(*args, **kwargs) -> typing.Any:
    pass
def LoggerComponent(*args, **kwargs) -> typing.Any:
    pass
def LoggerThreadPool() -> ILoggerThreadPool:
    pass
def MallocAllocator() -> IAllocator:
    pass
def ModuleManager(arg0: IString, arg1: IContext) -> IModuleManager:
    pass
def ObjectProperty(arg0: IString, arg1: IPropertyObject) -> IProperty:
    pass
def PacketReader(arg0: ISignal) -> IPacketReader:
    pass
def Procedure(arg0: object) -> IProcObject:
    pass
def Property() -> IPropertyConfig:
    pass
def PropertyObject() -> IPropertyObject:
    pass
def PropertyObjectClass(arg0: IString) -> IPropertyObjectClassConfig:
    pass
def PropertyObjectClassManager() -> IPropertyObjectClassManager:
    pass
def PropertyObjectClassWithManager(arg0: IPropertyObjectClassManager, arg1: IString) -> IPropertyObjectClassConfig:
    pass
def PropertyObjectWithClassAndManager(arg0: IPropertyObjectClassManager, arg1: IString) -> IPropertyObject:
    pass
def PropertyValueEventArgs(*args, **kwargs) -> typing.Any:
    pass
def PropertyWithName(arg0: IString) -> IProperty:
    pass
def Range(*args, **kwargs) -> typing.Any:
    pass
def Ratio(numerator: int, denominator: int) -> IRatio:
    """
    Creates a new Ratio object.
    """
def RatioProperty(arg0: IString, arg1: IRatio, arg2: IBoolean) -> IProperty:
    pass
def ReferenceProperty(arg0: IString, arg1: IEvalValue) -> IProperty:
    pass
def RotatingFileLoggerSink(arg0: IString, arg1: int, arg2: int) -> ILoggerSink:
    pass
def Scaling() -> IScalingConfig:
    pass
def ScalingFromExisting(arg0: IScaling) -> IScalingConfig:
    pass
def Scheduler(arg0: ILogger, arg1: int) -> IScheduler:
    pass
def SelectionProperty(arg0: IString, arg1: IList, arg2: IInteger, arg3: IBoolean) -> IProperty:
    pass
def ServerTypeConfig(*args, **kwargs) -> typing.Any:
    pass
def Signal(arg0: IContext, arg1: IComponent, arg2: IString, arg3: IString) -> ISignalConfig:
    pass
def SignalDescriptor() -> ISignalDescriptorConfig:
    pass
def SignalDescriptorChangedEventPacket(arg0: ISignalDescriptor, arg1: ISignalDescriptor) -> IEventPacket:
    pass
def SignalDescriptorFromExisting(arg0: ISignalDescriptor) -> ISignalDescriptorConfig:
    pass
def SignalWithDescriptor(arg0: IContext, arg1: ISignalDescriptor, arg2: IComponent, arg3: IString, arg4: IString) -> ISignalConfig:
    pass
def SparseSelectionProperty(arg0: IString, arg1: IDict, arg2: IInteger, arg3: IBoolean) -> IProperty:
    pass
def StdErrLoggerSink() -> ILoggerSink:
    pass
def StdOutLoggerSink() -> ILoggerSink:
    pass
def StreamReader(signal: ISignal, timeout_type: ReadTimeoutType = ReadTimeoutType.All) -> IStreamReader:
    pass
def StreamReaderFromExisting(*args, **kwargs) -> typing.Any:
    pass
def String(arg0: str) -> IString:
    pass
def StringProperty(arg0: IString, arg1: IString, arg2: IBoolean) -> IProperty:
    pass
def Tags() -> ITagsConfig:
    pass
def TagsFromExisting(arg0: ITags) -> ITagsConfig:
    pass
def TailReader(signal: ISignal, history_size: int) -> ITailReader:
    """
    A reader that only ever reads the last N samples, subsequent calls may result in overlapping data.
    """
def TailReaderFromExisting(*args, **kwargs) -> typing.Any:
    pass
def Task(arg0: IProcObject, arg1: IString) -> ITask:
    pass
def TaskGraph(arg0: IProcObject, arg1: IString) -> ITaskGraph:
    pass
def Unit(arg0: int, arg1: IString, arg2: IString, arg3: IString) -> IUnit:
    pass
def UnitEmpty() -> IUnitConfig:
    pass
def UnitFromExisting(arg0: IUnit) -> IUnitConfig:
    pass
def Validator(arg0: IString) -> IValidator:
    pass
def WinDebugLoggerSink() -> ILoggerSink:
    pass
def clear_error_info() -> None:
    pass
def get_tracked_object_count() -> int:
    pass
def print_tracked_objects() -> None:
    pass
