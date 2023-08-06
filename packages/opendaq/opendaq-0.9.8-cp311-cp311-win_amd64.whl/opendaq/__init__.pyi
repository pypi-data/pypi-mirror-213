from __future__ import annotations
import opendaq
import typing
from opendaq._opendaq import CoreType
from opendaq._opendaq import DataRuleType
from opendaq._opendaq import DimensionRuleType
from opendaq._opendaq import IAllocator
from opendaq._opendaq import IArgumentInfo
from opendaq._opendaq import IAwaitable
from opendaq._opendaq import IBaseObject
from opendaq._opendaq import IBlockReader
from opendaq._opendaq import IBoolean
from opendaq._opendaq import ICallableInfo
from opendaq._opendaq import IChannel
from opendaq._opendaq import ICoercer
from opendaq._opendaq import IComplexNumber
from opendaq._opendaq import IComponent
from opendaq._opendaq import IConnection
from opendaq._opendaq import IContext
from opendaq._opendaq import IDataDescriptor
from opendaq._opendaq import IDataDescriptorConfig
from opendaq._opendaq import IDataPacket
from opendaq._opendaq import IDataRule
from opendaq._opendaq import IDataRuleConfig
from opendaq._opendaq import IDevice
from opendaq._opendaq import IDeviceDomain
from opendaq._opendaq import IDeviceInfo
from opendaq._opendaq import IDeviceInfoConfig
from opendaq._opendaq import IDict
from opendaq._opendaq import IDimension
from opendaq._opendaq import IDimensionConfig
from opendaq._opendaq import IDimensionRule
from opendaq._opendaq import IDimensionRuleConfig
from opendaq._opendaq import IEvalValue
from opendaq._opendaq import IEventArgs
from opendaq._opendaq import IEventPacket
from opendaq._opendaq import IFloat
from opendaq._opendaq import IFolder
from opendaq._opendaq import IFolderConfig
from opendaq._opendaq import IFunctionBlock
from opendaq._opendaq import IFunctionBlockType
from opendaq._opendaq import IGraphVisualization
from opendaq._opendaq import IInputPort
from opendaq._opendaq import IInputPortConfig
from opendaq._opendaq import IInputPortNotifications
from opendaq._opendaq import IInstance
from opendaq._opendaq import IInteger
from opendaq._opendaq import IIterable
from opendaq._opendaq import IIterator
from opendaq._opendaq import IList
from opendaq._opendaq import ILogger
from opendaq._opendaq import ILoggerComponent
from opendaq._opendaq import ILoggerSink
from opendaq._opendaq import ILoggerThreadPool
from opendaq._opendaq import IModule
from opendaq._opendaq import IModuleManager
from opendaq._opendaq import IOwnable
from opendaq._opendaq import IPacket
from opendaq._opendaq import IPacketReader
from opendaq._opendaq import IProcObject
from opendaq._opendaq import IProperty
from opendaq._opendaq import IPropertyConfig
from opendaq._opendaq import IPropertyObject
from opendaq._opendaq import IPropertyObjectClass
from opendaq._opendaq import IPropertyObjectClassConfig
from opendaq._opendaq import IPropertyObjectClassManager
from opendaq._opendaq import IPropertyObjectProtected
from opendaq._opendaq import IPropertyValueEventArgs
from opendaq._opendaq import IRange
from opendaq._opendaq import IRatio
from opendaq._opendaq import IReader
from opendaq._opendaq import IRemovable
from opendaq._opendaq import ISampleReader
from opendaq._opendaq import IScaling
from opendaq._opendaq import IScalingConfig
from opendaq._opendaq import IScheduler
from opendaq._opendaq import IServer
from opendaq._opendaq import IServerType
from opendaq._opendaq import IServerTypeConfig
from opendaq._opendaq import ISignal
from opendaq._opendaq import ISignalConfig
from opendaq._opendaq import ISignalDescriptor
from opendaq._opendaq import ISignalDescriptorConfig
from opendaq._opendaq import ISignalEvents
from opendaq._opendaq import IStreamReader
from opendaq._opendaq import IString
from opendaq._opendaq import ITags
from opendaq._opendaq import ITagsConfig
from opendaq._opendaq import ITailReader
from opendaq._opendaq import ITask
from opendaq._opendaq import ITaskGraph
from opendaq._opendaq import IUnit
from opendaq._opendaq import IUnitConfig
from opendaq._opendaq import IValidator
from opendaq._opendaq import LogLevel
from opendaq._opendaq import PacketReadyNotification
from opendaq._opendaq import PacketType
from opendaq._opendaq import PropertyEventType
from opendaq._opendaq import ReadTimeoutType
from opendaq._opendaq import ScalingType
import os

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
    "OPENDAQ_MODULES_DIR",
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
    "os",
    "print_tracked_objects"
]


def ArgumentInfo(arg0: _opendaq.IString, arg1: _opendaq.CoreType) -> _opendaq.IArgumentInfo:
    pass
def BaseObject() -> _opendaq.IBaseObject:
    pass
def BasicFileLoggerSink(arg0: _opendaq.IString) -> _opendaq.ILoggerSink:
    pass
def BlockReader(*args, **kwargs) -> typing.Any:
    pass
def BlockReaderFromExisting(*args, **kwargs) -> typing.Any:
    pass
def BoolProperty(arg0: _opendaq.IString, arg1: _opendaq.IBoolean, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def Boolean(value: bool) -> _opendaq.IBoolean:
    """
    Creates a new Boolean.
    """
def CallableInfo(arg0: _opendaq.IList, arg1: _opendaq.CoreType) -> _opendaq.ICallableInfo:
    pass
def Client(arg0: _opendaq.IContext, arg1: _opendaq.IModuleManager, arg2: _opendaq.IString) -> _opendaq.IDevice:
    pass
def Coercer(arg0: _opendaq.IString) -> _opendaq.ICoercer:
    pass
@typing.overload
def ComplexNumber(real: float, imaginary: float) -> _opendaq.IComplexNumber:
    """
    Creates a new ComplexNumber object.

    Creates a new ComplexNumber object.
    """
@typing.overload
def ComplexNumber(value: complex) -> _opendaq.IComplexNumber:
    pass
def Component(arg0: _opendaq.IContext, arg1: _opendaq.IComponent, arg2: _opendaq.IString, arg3: _opendaq.IString) -> _opendaq.IComponent:
    pass
def Connection(arg0: _opendaq.IInputPort, arg1: _opendaq.ISignal, arg2: _opendaq.IContext) -> _opendaq.IConnection:
    pass
def ConstantDataRule(*args, **kwargs) -> typing.Any:
    pass
def Context(arg0: _opendaq.IScheduler, arg1: _opendaq.ILogger, arg2: _opendaq.IPropertyObjectClassManager) -> _opendaq.IContext:
    pass
def DataDescriptor() -> _opendaq.IDataDescriptorConfig:
    pass
def DataDescriptorFromExisting(arg0: _opendaq.IDataDescriptor) -> _opendaq.IDataDescriptorConfig:
    pass
def DataPacket(*args, **kwargs) -> typing.Any:
    pass
def DataPacketWithDomain(*args, **kwargs) -> typing.Any:
    pass
def DataRule() -> _opendaq.IDataRuleConfig:
    pass
def DataRuleFromExisting(arg0: _opendaq.IDataRule) -> _opendaq.IDataRuleConfig:
    pass
def DeviceInfoConfig(arg0: _opendaq.IString, arg1: _opendaq.IString) -> _opendaq.IDeviceInfoConfig:
    pass
def Dict() -> _opendaq.IDict:
    pass
def DictProperty(arg0: _opendaq.IString, arg1: _opendaq.IDict, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def Dimension() -> _opendaq.IDimensionConfig:
    pass
def DimensionFromExisting(arg0: _opendaq.IDimension) -> _opendaq.IDimensionConfig:
    pass
def DimensionFromRule(arg0: _opendaq.IDimensionRule, arg1: _opendaq.IUnit, arg2: _opendaq.IString) -> _opendaq.IDimension:
    pass
def DimensionRule() -> _opendaq.IDimensionRuleConfig:
    pass
def DimensionRuleFromExisting(arg0: _opendaq.IDimensionRule) -> _opendaq.IDimensionRuleConfig:
    pass
def EvalValue(arg0: _opendaq.IString) -> _opendaq.IEvalValue:
    pass
def EvalValueArgs(arg0: _opendaq.IString, arg1: _opendaq.IList) -> _opendaq.IEvalValue:
    pass
def EvalValueFunc(*args, **kwargs) -> typing.Any:
    pass
def EventArgs(arg0: int, arg1: _opendaq.IString) -> _opendaq.IEventArgs:
    pass
def EventPacket(arg0: _opendaq.IString, arg1: _opendaq.IDict) -> _opendaq.IEventPacket:
    pass
def ExplicitDataRule() -> _opendaq.IDataRule:
    pass
def ExternalAllocator(*args, **kwargs) -> typing.Any:
    pass
def Float(arg0: float) -> _opendaq.IFloat:
    pass
def FloatProperty(arg0: _opendaq.IString, arg1: _opendaq.IFloat, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def Folder(arg0: _opendaq.IContext, arg1: _opendaq.IComponent, arg2: _opendaq.IString) -> _opendaq.IFolderConfig:
    pass
def FolderWithItemType(*args, **kwargs) -> typing.Any:
    pass
def FunctionBlockType(arg0: _opendaq.IString, arg1: _opendaq.IString, arg2: _opendaq.IString) -> _opendaq.IFunctionBlockType:
    pass
def FunctionProperty(arg0: _opendaq.IString, arg1: _opendaq.ICallableInfo, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def InputPort(arg0: _opendaq.IContext, arg1: _opendaq.IComponent, arg2: _opendaq.IString) -> _opendaq.IInputPortConfig:
    pass
def IntProperty(arg0: _opendaq.IString, arg1: _opendaq.IInteger, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def Integer(arg0: int) -> _opendaq.IInteger:
    pass
def IoFolder(arg0: _opendaq.IContext, arg1: _opendaq.IComponent, arg2: _opendaq.IString) -> _opendaq.IFolderConfig:
    pass
def LinearDataRule(*args, **kwargs) -> typing.Any:
    pass
def LinearDimensionRule(*args, **kwargs) -> typing.Any:
    pass
def LinearScaling(*args, **kwargs) -> typing.Any:
    pass
def List() -> _opendaq.IList:
    pass
def ListDimensionRule(arg0: _opendaq.IList) -> _opendaq.IDimensionRule:
    pass
def ListProperty(arg0: _opendaq.IString, arg1: _opendaq.IList, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def LogarithmicDimensionRule(*args, **kwargs) -> typing.Any:
    pass
def Logger(*args, **kwargs) -> typing.Any:
    pass
def LoggerComponent(*args, **kwargs) -> typing.Any:
    pass
def LoggerThreadPool() -> _opendaq.ILoggerThreadPool:
    pass
def MallocAllocator() -> _opendaq.IAllocator:
    pass
def ModuleManager(arg0: _opendaq.IString, arg1: _opendaq.IContext) -> _opendaq.IModuleManager:
    pass
def ObjectProperty(arg0: _opendaq.IString, arg1: _opendaq.IPropertyObject) -> _opendaq.IProperty:
    pass
def PacketReader(arg0: _opendaq.ISignal) -> _opendaq.IPacketReader:
    pass
def Procedure(arg0: object) -> _opendaq.IProcObject:
    pass
def Property() -> _opendaq.IPropertyConfig:
    pass
def PropertyObject() -> _opendaq.IPropertyObject:
    pass
def PropertyObjectClass(arg0: _opendaq.IString) -> _opendaq.IPropertyObjectClassConfig:
    pass
def PropertyObjectClassManager() -> _opendaq.IPropertyObjectClassManager:
    pass
def PropertyObjectClassWithManager(arg0: _opendaq.IPropertyObjectClassManager, arg1: _opendaq.IString) -> _opendaq.IPropertyObjectClassConfig:
    pass
def PropertyObjectWithClassAndManager(arg0: _opendaq.IPropertyObjectClassManager, arg1: _opendaq.IString) -> _opendaq.IPropertyObject:
    pass
def PropertyValueEventArgs(*args, **kwargs) -> typing.Any:
    pass
def PropertyWithName(arg0: _opendaq.IString) -> _opendaq.IProperty:
    pass
def Range(*args, **kwargs) -> typing.Any:
    pass
def Ratio(numerator: int, denominator: int) -> _opendaq.IRatio:
    """
    Creates a new Ratio object.
    """
def RatioProperty(arg0: _opendaq.IString, arg1: _opendaq.IRatio, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def ReferenceProperty(arg0: _opendaq.IString, arg1: _opendaq.IEvalValue) -> _opendaq.IProperty:
    pass
def RotatingFileLoggerSink(arg0: _opendaq.IString, arg1: int, arg2: int) -> _opendaq.ILoggerSink:
    pass
def Scaling() -> _opendaq.IScalingConfig:
    pass
def ScalingFromExisting(arg0: _opendaq.IScaling) -> _opendaq.IScalingConfig:
    pass
def Scheduler(arg0: _opendaq.ILogger, arg1: int) -> _opendaq.IScheduler:
    pass
def SelectionProperty(arg0: _opendaq.IString, arg1: _opendaq.IList, arg2: _opendaq.IInteger, arg3: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def ServerTypeConfig(*args, **kwargs) -> typing.Any:
    pass
def Signal(arg0: _opendaq.IContext, arg1: _opendaq.IComponent, arg2: _opendaq.IString, arg3: _opendaq.IString) -> _opendaq.ISignalConfig:
    pass
def SignalDescriptor() -> _opendaq.ISignalDescriptorConfig:
    pass
def SignalDescriptorChangedEventPacket(arg0: _opendaq.ISignalDescriptor, arg1: _opendaq.ISignalDescriptor) -> _opendaq.IEventPacket:
    pass
def SignalDescriptorFromExisting(arg0: _opendaq.ISignalDescriptor) -> _opendaq.ISignalDescriptorConfig:
    pass
def SignalWithDescriptor(arg0: _opendaq.IContext, arg1: _opendaq.ISignalDescriptor, arg2: _opendaq.IComponent, arg3: _opendaq.IString, arg4: _opendaq.IString) -> _opendaq.ISignalConfig:
    pass
def SparseSelectionProperty(arg0: _opendaq.IString, arg1: _opendaq.IDict, arg2: _opendaq.IInteger, arg3: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def StdErrLoggerSink() -> _opendaq.ILoggerSink:
    pass
def StdOutLoggerSink() -> _opendaq.ILoggerSink:
    pass
def StreamReader(signal: _opendaq.ISignal, timeout_type: _opendaq.ReadTimeoutType = ReadTimeoutType.All) -> _opendaq.IStreamReader:
    pass
def StreamReaderFromExisting(*args, **kwargs) -> typing.Any:
    pass
def String(arg0: str) -> _opendaq.IString:
    pass
def StringProperty(arg0: _opendaq.IString, arg1: _opendaq.IString, arg2: _opendaq.IBoolean) -> _opendaq.IProperty:
    pass
def Tags() -> _opendaq.ITagsConfig:
    pass
def TagsFromExisting(arg0: _opendaq.ITags) -> _opendaq.ITagsConfig:
    pass
def TailReader(signal: _opendaq.ISignal, history_size: int) -> _opendaq.ITailReader:
    """
    A reader that only ever reads the last N samples, subsequent calls may result in overlapping data.
    """
def TailReaderFromExisting(*args, **kwargs) -> typing.Any:
    pass
def Task(arg0: _opendaq.IProcObject, arg1: _opendaq.IString) -> _opendaq.ITask:
    pass
def TaskGraph(arg0: _opendaq.IProcObject, arg1: _opendaq.IString) -> _opendaq.ITaskGraph:
    pass
def Unit(arg0: int, arg1: _opendaq.IString, arg2: _opendaq.IString, arg3: _opendaq.IString) -> _opendaq.IUnit:
    pass
def UnitEmpty() -> _opendaq.IUnitConfig:
    pass
def UnitFromExisting(arg0: _opendaq.IUnit) -> _opendaq.IUnitConfig:
    pass
def Validator(arg0: _opendaq.IString) -> _opendaq.IValidator:
    pass
def WinDebugLoggerSink() -> _opendaq.ILoggerSink:
    pass
def clear_error_info() -> None:
    pass
def get_tracked_object_count() -> int:
    pass
def print_tracked_objects() -> None:
    pass

OPENDAQ_MODULES_DIR = os.path.dirname(os.path.abspath(__file__))

def Instance(*args) -> IInstance: ...
