"""
Type annotations for simspaceweaver service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_simspaceweaver/type_defs/)

Usage::

    ```python
    from mypy_boto3_simspaceweaver.type_defs import CloudWatchLogsLogGroupTypeDef

    data: CloudWatchLogsLogGroupTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    ClockStatusType,
    ClockTargetStatusType,
    LifecycleManagementStrategyType,
    SimulationAppStatusType,
    SimulationAppTargetStatusType,
    SimulationStatusType,
    SimulationTargetStatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CloudWatchLogsLogGroupTypeDef",
    "S3DestinationTypeDef",
    "DeleteAppInputRequestTypeDef",
    "DeleteSimulationInputRequestTypeDef",
    "DescribeAppInputRequestTypeDef",
    "LaunchOverridesTypeDef",
    "ResponseMetadataTypeDef",
    "DescribeSimulationInputRequestTypeDef",
    "S3LocationTypeDef",
    "DomainTypeDef",
    "ListAppsInputRequestTypeDef",
    "SimulationAppMetadataTypeDef",
    "ListSimulationsInputRequestTypeDef",
    "SimulationMetadataTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "SimulationClockTypeDef",
    "SimulationAppPortMappingTypeDef",
    "StartClockInputRequestTypeDef",
    "StopAppInputRequestTypeDef",
    "StopClockInputRequestTypeDef",
    "StopSimulationInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "LogDestinationTypeDef",
    "CreateSnapshotInputRequestTypeDef",
    "StartAppInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "StartAppOutputTypeDef",
    "StartSimulationOutputTypeDef",
    "StartSimulationInputRequestTypeDef",
    "ListAppsOutputTypeDef",
    "ListSimulationsOutputTypeDef",
    "LiveSimulationStateTypeDef",
    "SimulationAppEndpointInfoTypeDef",
    "LoggingConfigurationTypeDef",
    "DescribeAppOutputTypeDef",
    "DescribeSimulationOutputTypeDef",
)

CloudWatchLogsLogGroupTypeDef = TypedDict(
    "CloudWatchLogsLogGroupTypeDef",
    {
        "LogGroupArn": str,
    },
    total=False,
)

S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef",
    {
        "BucketName": str,
        "ObjectKeyPrefix": str,
    },
    total=False,
)

DeleteAppInputRequestTypeDef = TypedDict(
    "DeleteAppInputRequestTypeDef",
    {
        "App": str,
        "Domain": str,
        "Simulation": str,
    },
)

DeleteSimulationInputRequestTypeDef = TypedDict(
    "DeleteSimulationInputRequestTypeDef",
    {
        "Simulation": str,
    },
)

DescribeAppInputRequestTypeDef = TypedDict(
    "DescribeAppInputRequestTypeDef",
    {
        "App": str,
        "Domain": str,
        "Simulation": str,
    },
)

LaunchOverridesTypeDef = TypedDict(
    "LaunchOverridesTypeDef",
    {
        "LaunchCommands": List[str],
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DescribeSimulationInputRequestTypeDef = TypedDict(
    "DescribeSimulationInputRequestTypeDef",
    {
        "Simulation": str,
    },
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "BucketName": str,
        "ObjectKey": str,
    },
    total=False,
)

DomainTypeDef = TypedDict(
    "DomainTypeDef",
    {
        "Lifecycle": LifecycleManagementStrategyType,
        "Name": str,
    },
    total=False,
)

_RequiredListAppsInputRequestTypeDef = TypedDict(
    "_RequiredListAppsInputRequestTypeDef",
    {
        "Simulation": str,
    },
)
_OptionalListAppsInputRequestTypeDef = TypedDict(
    "_OptionalListAppsInputRequestTypeDef",
    {
        "Domain": str,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListAppsInputRequestTypeDef(
    _RequiredListAppsInputRequestTypeDef, _OptionalListAppsInputRequestTypeDef
):
    pass


SimulationAppMetadataTypeDef = TypedDict(
    "SimulationAppMetadataTypeDef",
    {
        "Domain": str,
        "Name": str,
        "Simulation": str,
        "Status": SimulationAppStatusType,
        "TargetStatus": SimulationAppTargetStatusType,
    },
    total=False,
)

ListSimulationsInputRequestTypeDef = TypedDict(
    "ListSimulationsInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

SimulationMetadataTypeDef = TypedDict(
    "SimulationMetadataTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "Name": str,
        "Status": SimulationStatusType,
        "TargetStatus": SimulationTargetStatusType,
    },
    total=False,
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

SimulationClockTypeDef = TypedDict(
    "SimulationClockTypeDef",
    {
        "Status": ClockStatusType,
        "TargetStatus": ClockTargetStatusType,
    },
    total=False,
)

SimulationAppPortMappingTypeDef = TypedDict(
    "SimulationAppPortMappingTypeDef",
    {
        "Actual": int,
        "Declared": int,
    },
    total=False,
)

StartClockInputRequestTypeDef = TypedDict(
    "StartClockInputRequestTypeDef",
    {
        "Simulation": str,
    },
)

StopAppInputRequestTypeDef = TypedDict(
    "StopAppInputRequestTypeDef",
    {
        "App": str,
        "Domain": str,
        "Simulation": str,
    },
)

StopClockInputRequestTypeDef = TypedDict(
    "StopClockInputRequestTypeDef",
    {
        "Simulation": str,
    },
)

StopSimulationInputRequestTypeDef = TypedDict(
    "StopSimulationInputRequestTypeDef",
    {
        "Simulation": str,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

LogDestinationTypeDef = TypedDict(
    "LogDestinationTypeDef",
    {
        "CloudWatchLogsLogGroup": CloudWatchLogsLogGroupTypeDef,
    },
    total=False,
)

CreateSnapshotInputRequestTypeDef = TypedDict(
    "CreateSnapshotInputRequestTypeDef",
    {
        "Destination": S3DestinationTypeDef,
        "Simulation": str,
    },
)

_RequiredStartAppInputRequestTypeDef = TypedDict(
    "_RequiredStartAppInputRequestTypeDef",
    {
        "Domain": str,
        "Name": str,
        "Simulation": str,
    },
)
_OptionalStartAppInputRequestTypeDef = TypedDict(
    "_OptionalStartAppInputRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "LaunchOverrides": LaunchOverridesTypeDef,
    },
    total=False,
)


class StartAppInputRequestTypeDef(
    _RequiredStartAppInputRequestTypeDef, _OptionalStartAppInputRequestTypeDef
):
    pass


ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartAppOutputTypeDef = TypedDict(
    "StartAppOutputTypeDef",
    {
        "Domain": str,
        "Name": str,
        "Simulation": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartSimulationOutputTypeDef = TypedDict(
    "StartSimulationOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "ExecutionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredStartSimulationInputRequestTypeDef = TypedDict(
    "_RequiredStartSimulationInputRequestTypeDef",
    {
        "Name": str,
        "RoleArn": str,
    },
)
_OptionalStartSimulationInputRequestTypeDef = TypedDict(
    "_OptionalStartSimulationInputRequestTypeDef",
    {
        "ClientToken": str,
        "Description": str,
        "MaximumDuration": str,
        "SchemaS3Location": S3LocationTypeDef,
        "SnapshotS3Location": S3LocationTypeDef,
        "Tags": Mapping[str, str],
    },
    total=False,
)


class StartSimulationInputRequestTypeDef(
    _RequiredStartSimulationInputRequestTypeDef, _OptionalStartSimulationInputRequestTypeDef
):
    pass


ListAppsOutputTypeDef = TypedDict(
    "ListAppsOutputTypeDef",
    {
        "Apps": List[SimulationAppMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSimulationsOutputTypeDef = TypedDict(
    "ListSimulationsOutputTypeDef",
    {
        "NextToken": str,
        "Simulations": List[SimulationMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LiveSimulationStateTypeDef = TypedDict(
    "LiveSimulationStateTypeDef",
    {
        "Clocks": List[SimulationClockTypeDef],
        "Domains": List[DomainTypeDef],
    },
    total=False,
)

SimulationAppEndpointInfoTypeDef = TypedDict(
    "SimulationAppEndpointInfoTypeDef",
    {
        "Address": str,
        "IngressPortMappings": List[SimulationAppPortMappingTypeDef],
    },
    total=False,
)

LoggingConfigurationTypeDef = TypedDict(
    "LoggingConfigurationTypeDef",
    {
        "Destinations": List[LogDestinationTypeDef],
    },
    total=False,
)

DescribeAppOutputTypeDef = TypedDict(
    "DescribeAppOutputTypeDef",
    {
        "Description": str,
        "Domain": str,
        "EndpointInfo": SimulationAppEndpointInfoTypeDef,
        "LaunchOverrides": LaunchOverridesTypeDef,
        "Name": str,
        "Simulation": str,
        "Status": SimulationAppStatusType,
        "TargetStatus": SimulationAppTargetStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSimulationOutputTypeDef = TypedDict(
    "DescribeSimulationOutputTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "Description": str,
        "ExecutionId": str,
        "LiveSimulationState": LiveSimulationStateTypeDef,
        "LoggingConfiguration": LoggingConfigurationTypeDef,
        "MaximumDuration": str,
        "Name": str,
        "RoleArn": str,
        "SchemaError": str,
        "SchemaS3Location": S3LocationTypeDef,
        "SnapshotS3Location": S3LocationTypeDef,
        "StartError": str,
        "Status": SimulationStatusType,
        "TargetStatus": SimulationTargetStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
