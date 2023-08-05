"""
Type annotations for timestream-write service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_write/type_defs/)

Usage::

    ```python
    from mypy_boto3_timestream_write.type_defs import BatchLoadProgressReportTypeDef

    data: BatchLoadProgressReportTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    BatchLoadStatusType,
    MeasureValueTypeType,
    PartitionKeyEnforcementLevelType,
    PartitionKeyTypeType,
    S3EncryptionOptionType,
    ScalarMeasureValueTypeType,
    TableStatusType,
    TimeUnitType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BatchLoadProgressReportTypeDef",
    "BatchLoadTaskTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "DatabaseTypeDef",
    "RetentionPropertiesTypeDef",
    "CsvConfigurationTypeDef",
    "DataModelS3ConfigurationTypeDef",
    "DimensionMappingTypeDef",
    "DataSourceS3ConfigurationTypeDef",
    "DeleteDatabaseRequestRequestTypeDef",
    "DeleteTableRequestRequestTypeDef",
    "DescribeBatchLoadTaskRequestRequestTypeDef",
    "DescribeDatabaseRequestRequestTypeDef",
    "EndpointTypeDef",
    "DescribeTableRequestRequestTypeDef",
    "DimensionTypeDef",
    "ListBatchLoadTasksRequestRequestTypeDef",
    "ListDatabasesRequestRequestTypeDef",
    "ListTablesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "S3ConfigurationTypeDef",
    "MeasureValueTypeDef",
    "MultiMeasureAttributeMappingTypeDef",
    "PartitionKeyTypeDef",
    "RecordsIngestedTypeDef",
    "ReportS3ConfigurationTypeDef",
    "ResumeBatchLoadTaskRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatabaseRequestRequestTypeDef",
    "CreateBatchLoadTaskResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListBatchLoadTasksResponseTypeDef",
    "CreateDatabaseRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateDatabaseResponseTypeDef",
    "DescribeDatabaseResponseTypeDef",
    "ListDatabasesResponseTypeDef",
    "UpdateDatabaseResponseTypeDef",
    "DataSourceConfigurationTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "MagneticStoreRejectedDataLocationTypeDef",
    "RecordTypeDef",
    "MixedMeasureMappingTypeDef",
    "MultiMeasureMappingsTypeDef",
    "SchemaTypeDef",
    "WriteRecordsResponseTypeDef",
    "ReportConfigurationTypeDef",
    "MagneticStoreWritePropertiesTypeDef",
    "WriteRecordsRequestRequestTypeDef",
    "DataModelTypeDef",
    "CreateTableRequestRequestTypeDef",
    "TableTypeDef",
    "UpdateTableRequestRequestTypeDef",
    "DataModelConfigurationTypeDef",
    "CreateTableResponseTypeDef",
    "DescribeTableResponseTypeDef",
    "ListTablesResponseTypeDef",
    "UpdateTableResponseTypeDef",
    "BatchLoadTaskDescriptionTypeDef",
    "CreateBatchLoadTaskRequestRequestTypeDef",
    "DescribeBatchLoadTaskResponseTypeDef",
)

BatchLoadProgressReportTypeDef = TypedDict(
    "BatchLoadProgressReportTypeDef",
    {
        "RecordsProcessed": int,
        "RecordsIngested": int,
        "ParseFailures": int,
        "RecordIngestionFailures": int,
        "FileFailures": int,
        "BytesMetered": int,
    },
    total=False,
)

BatchLoadTaskTypeDef = TypedDict(
    "BatchLoadTaskTypeDef",
    {
        "TaskId": str,
        "TaskStatus": BatchLoadStatusType,
        "DatabaseName": str,
        "TableName": str,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
        "ResumableUntil": datetime,
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DatabaseTypeDef = TypedDict(
    "DatabaseTypeDef",
    {
        "Arn": str,
        "DatabaseName": str,
        "TableCount": int,
        "KmsKeyId": str,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
    },
    total=False,
)

RetentionPropertiesTypeDef = TypedDict(
    "RetentionPropertiesTypeDef",
    {
        "MemoryStoreRetentionPeriodInHours": int,
        "MagneticStoreRetentionPeriodInDays": int,
    },
)

CsvConfigurationTypeDef = TypedDict(
    "CsvConfigurationTypeDef",
    {
        "ColumnSeparator": str,
        "EscapeChar": str,
        "QuoteChar": str,
        "NullValue": str,
        "TrimWhiteSpace": bool,
    },
    total=False,
)

DataModelS3ConfigurationTypeDef = TypedDict(
    "DataModelS3ConfigurationTypeDef",
    {
        "BucketName": str,
        "ObjectKey": str,
    },
    total=False,
)

DimensionMappingTypeDef = TypedDict(
    "DimensionMappingTypeDef",
    {
        "SourceColumn": str,
        "DestinationColumn": str,
    },
    total=False,
)

_RequiredDataSourceS3ConfigurationTypeDef = TypedDict(
    "_RequiredDataSourceS3ConfigurationTypeDef",
    {
        "BucketName": str,
    },
)
_OptionalDataSourceS3ConfigurationTypeDef = TypedDict(
    "_OptionalDataSourceS3ConfigurationTypeDef",
    {
        "ObjectKeyPrefix": str,
    },
    total=False,
)

class DataSourceS3ConfigurationTypeDef(
    _RequiredDataSourceS3ConfigurationTypeDef, _OptionalDataSourceS3ConfigurationTypeDef
):
    pass

DeleteDatabaseRequestRequestTypeDef = TypedDict(
    "DeleteDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)

DeleteTableRequestRequestTypeDef = TypedDict(
    "DeleteTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)

DescribeBatchLoadTaskRequestRequestTypeDef = TypedDict(
    "DescribeBatchLoadTaskRequestRequestTypeDef",
    {
        "TaskId": str,
    },
)

DescribeDatabaseRequestRequestTypeDef = TypedDict(
    "DescribeDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)

EndpointTypeDef = TypedDict(
    "EndpointTypeDef",
    {
        "Address": str,
        "CachePeriodInMinutes": int,
    },
)

DescribeTableRequestRequestTypeDef = TypedDict(
    "DescribeTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)

_RequiredDimensionTypeDef = TypedDict(
    "_RequiredDimensionTypeDef",
    {
        "Name": str,
        "Value": str,
    },
)
_OptionalDimensionTypeDef = TypedDict(
    "_OptionalDimensionTypeDef",
    {
        "DimensionValueType": Literal["VARCHAR"],
    },
    total=False,
)

class DimensionTypeDef(_RequiredDimensionTypeDef, _OptionalDimensionTypeDef):
    pass

ListBatchLoadTasksRequestRequestTypeDef = TypedDict(
    "ListBatchLoadTasksRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "TaskStatus": BatchLoadStatusType,
    },
    total=False,
)

ListDatabasesRequestRequestTypeDef = TypedDict(
    "ListDatabasesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTablesRequestRequestTypeDef = TypedDict(
    "ListTablesRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
    },
)

S3ConfigurationTypeDef = TypedDict(
    "S3ConfigurationTypeDef",
    {
        "BucketName": str,
        "ObjectKeyPrefix": str,
        "EncryptionOption": S3EncryptionOptionType,
        "KmsKeyId": str,
    },
    total=False,
)

MeasureValueTypeDef = TypedDict(
    "MeasureValueTypeDef",
    {
        "Name": str,
        "Value": str,
        "Type": MeasureValueTypeType,
    },
)

_RequiredMultiMeasureAttributeMappingTypeDef = TypedDict(
    "_RequiredMultiMeasureAttributeMappingTypeDef",
    {
        "SourceColumn": str,
    },
)
_OptionalMultiMeasureAttributeMappingTypeDef = TypedDict(
    "_OptionalMultiMeasureAttributeMappingTypeDef",
    {
        "TargetMultiMeasureAttributeName": str,
        "MeasureValueType": ScalarMeasureValueTypeType,
    },
    total=False,
)

class MultiMeasureAttributeMappingTypeDef(
    _RequiredMultiMeasureAttributeMappingTypeDef, _OptionalMultiMeasureAttributeMappingTypeDef
):
    pass

_RequiredPartitionKeyTypeDef = TypedDict(
    "_RequiredPartitionKeyTypeDef",
    {
        "Type": PartitionKeyTypeType,
    },
)
_OptionalPartitionKeyTypeDef = TypedDict(
    "_OptionalPartitionKeyTypeDef",
    {
        "Name": str,
        "EnforcementInRecord": PartitionKeyEnforcementLevelType,
    },
    total=False,
)

class PartitionKeyTypeDef(_RequiredPartitionKeyTypeDef, _OptionalPartitionKeyTypeDef):
    pass

RecordsIngestedTypeDef = TypedDict(
    "RecordsIngestedTypeDef",
    {
        "Total": int,
        "MemoryStore": int,
        "MagneticStore": int,
    },
    total=False,
)

_RequiredReportS3ConfigurationTypeDef = TypedDict(
    "_RequiredReportS3ConfigurationTypeDef",
    {
        "BucketName": str,
    },
)
_OptionalReportS3ConfigurationTypeDef = TypedDict(
    "_OptionalReportS3ConfigurationTypeDef",
    {
        "ObjectKeyPrefix": str,
        "EncryptionOption": S3EncryptionOptionType,
        "KmsKeyId": str,
    },
    total=False,
)

class ReportS3ConfigurationTypeDef(
    _RequiredReportS3ConfigurationTypeDef, _OptionalReportS3ConfigurationTypeDef
):
    pass

ResumeBatchLoadTaskRequestRequestTypeDef = TypedDict(
    "ResumeBatchLoadTaskRequestRequestTypeDef",
    {
        "TaskId": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateDatabaseRequestRequestTypeDef = TypedDict(
    "UpdateDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "KmsKeyId": str,
    },
)

CreateBatchLoadTaskResponseTypeDef = TypedDict(
    "CreateBatchLoadTaskResponseTypeDef",
    {
        "TaskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBatchLoadTasksResponseTypeDef = TypedDict(
    "ListBatchLoadTasksResponseTypeDef",
    {
        "NextToken": str,
        "BatchLoadTasks": List[BatchLoadTaskTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredCreateDatabaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatabaseRequestRequestTypeDef",
    {
        "DatabaseName": str,
    },
)
_OptionalCreateDatabaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatabaseRequestRequestTypeDef",
    {
        "KmsKeyId": str,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)

class CreateDatabaseRequestRequestTypeDef(
    _RequiredCreateDatabaseRequestRequestTypeDef, _OptionalCreateDatabaseRequestRequestTypeDef
):
    pass

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateDatabaseResponseTypeDef = TypedDict(
    "CreateDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDatabaseResponseTypeDef = TypedDict(
    "DescribeDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatabasesResponseTypeDef = TypedDict(
    "ListDatabasesResponseTypeDef",
    {
        "Databases": List[DatabaseTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDatabaseResponseTypeDef = TypedDict(
    "UpdateDatabaseResponseTypeDef",
    {
        "Database": DatabaseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredDataSourceConfigurationTypeDef = TypedDict(
    "_RequiredDataSourceConfigurationTypeDef",
    {
        "DataSourceS3Configuration": DataSourceS3ConfigurationTypeDef,
        "DataFormat": Literal["CSV"],
    },
)
_OptionalDataSourceConfigurationTypeDef = TypedDict(
    "_OptionalDataSourceConfigurationTypeDef",
    {
        "CsvConfiguration": CsvConfigurationTypeDef,
    },
    total=False,
)

class DataSourceConfigurationTypeDef(
    _RequiredDataSourceConfigurationTypeDef, _OptionalDataSourceConfigurationTypeDef
):
    pass

DescribeEndpointsResponseTypeDef = TypedDict(
    "DescribeEndpointsResponseTypeDef",
    {
        "Endpoints": List[EndpointTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MagneticStoreRejectedDataLocationTypeDef = TypedDict(
    "MagneticStoreRejectedDataLocationTypeDef",
    {
        "S3Configuration": S3ConfigurationTypeDef,
    },
    total=False,
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "Dimensions": Sequence[DimensionTypeDef],
        "MeasureName": str,
        "MeasureValue": str,
        "MeasureValueType": MeasureValueTypeType,
        "Time": str,
        "TimeUnit": TimeUnitType,
        "Version": int,
        "MeasureValues": Sequence[MeasureValueTypeDef],
    },
    total=False,
)

_RequiredMixedMeasureMappingTypeDef = TypedDict(
    "_RequiredMixedMeasureMappingTypeDef",
    {
        "MeasureValueType": MeasureValueTypeType,
    },
)
_OptionalMixedMeasureMappingTypeDef = TypedDict(
    "_OptionalMixedMeasureMappingTypeDef",
    {
        "MeasureName": str,
        "SourceColumn": str,
        "TargetMeasureName": str,
        "MultiMeasureAttributeMappings": Sequence[MultiMeasureAttributeMappingTypeDef],
    },
    total=False,
)

class MixedMeasureMappingTypeDef(
    _RequiredMixedMeasureMappingTypeDef, _OptionalMixedMeasureMappingTypeDef
):
    pass

_RequiredMultiMeasureMappingsTypeDef = TypedDict(
    "_RequiredMultiMeasureMappingsTypeDef",
    {
        "MultiMeasureAttributeMappings": Sequence[MultiMeasureAttributeMappingTypeDef],
    },
)
_OptionalMultiMeasureMappingsTypeDef = TypedDict(
    "_OptionalMultiMeasureMappingsTypeDef",
    {
        "TargetMultiMeasureName": str,
    },
    total=False,
)

class MultiMeasureMappingsTypeDef(
    _RequiredMultiMeasureMappingsTypeDef, _OptionalMultiMeasureMappingsTypeDef
):
    pass

SchemaTypeDef = TypedDict(
    "SchemaTypeDef",
    {
        "CompositePartitionKey": Sequence[PartitionKeyTypeDef],
    },
    total=False,
)

WriteRecordsResponseTypeDef = TypedDict(
    "WriteRecordsResponseTypeDef",
    {
        "RecordsIngested": RecordsIngestedTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReportConfigurationTypeDef = TypedDict(
    "ReportConfigurationTypeDef",
    {
        "ReportS3Configuration": ReportS3ConfigurationTypeDef,
    },
    total=False,
)

_RequiredMagneticStoreWritePropertiesTypeDef = TypedDict(
    "_RequiredMagneticStoreWritePropertiesTypeDef",
    {
        "EnableMagneticStoreWrites": bool,
    },
)
_OptionalMagneticStoreWritePropertiesTypeDef = TypedDict(
    "_OptionalMagneticStoreWritePropertiesTypeDef",
    {
        "MagneticStoreRejectedDataLocation": MagneticStoreRejectedDataLocationTypeDef,
    },
    total=False,
)

class MagneticStoreWritePropertiesTypeDef(
    _RequiredMagneticStoreWritePropertiesTypeDef, _OptionalMagneticStoreWritePropertiesTypeDef
):
    pass

_RequiredWriteRecordsRequestRequestTypeDef = TypedDict(
    "_RequiredWriteRecordsRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
        "Records": Sequence[RecordTypeDef],
    },
)
_OptionalWriteRecordsRequestRequestTypeDef = TypedDict(
    "_OptionalWriteRecordsRequestRequestTypeDef",
    {
        "CommonAttributes": RecordTypeDef,
    },
    total=False,
)

class WriteRecordsRequestRequestTypeDef(
    _RequiredWriteRecordsRequestRequestTypeDef, _OptionalWriteRecordsRequestRequestTypeDef
):
    pass

_RequiredDataModelTypeDef = TypedDict(
    "_RequiredDataModelTypeDef",
    {
        "DimensionMappings": Sequence[DimensionMappingTypeDef],
    },
)
_OptionalDataModelTypeDef = TypedDict(
    "_OptionalDataModelTypeDef",
    {
        "TimeColumn": str,
        "TimeUnit": TimeUnitType,
        "MultiMeasureMappings": MultiMeasureMappingsTypeDef,
        "MixedMeasureMappings": Sequence[MixedMeasureMappingTypeDef],
        "MeasureNameColumn": str,
    },
    total=False,
)

class DataModelTypeDef(_RequiredDataModelTypeDef, _OptionalDataModelTypeDef):
    pass

_RequiredCreateTableRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalCreateTableRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTableRequestRequestTypeDef",
    {
        "RetentionProperties": RetentionPropertiesTypeDef,
        "Tags": Sequence[TagTypeDef],
        "MagneticStoreWriteProperties": MagneticStoreWritePropertiesTypeDef,
        "Schema": SchemaTypeDef,
    },
    total=False,
)

class CreateTableRequestRequestTypeDef(
    _RequiredCreateTableRequestRequestTypeDef, _OptionalCreateTableRequestRequestTypeDef
):
    pass

TableTypeDef = TypedDict(
    "TableTypeDef",
    {
        "Arn": str,
        "TableName": str,
        "DatabaseName": str,
        "TableStatus": TableStatusType,
        "RetentionProperties": RetentionPropertiesTypeDef,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
        "MagneticStoreWriteProperties": MagneticStoreWritePropertiesTypeDef,
        "Schema": SchemaTypeDef,
    },
    total=False,
)

_RequiredUpdateTableRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTableRequestRequestTypeDef",
    {
        "DatabaseName": str,
        "TableName": str,
    },
)
_OptionalUpdateTableRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTableRequestRequestTypeDef",
    {
        "RetentionProperties": RetentionPropertiesTypeDef,
        "MagneticStoreWriteProperties": MagneticStoreWritePropertiesTypeDef,
        "Schema": SchemaTypeDef,
    },
    total=False,
)

class UpdateTableRequestRequestTypeDef(
    _RequiredUpdateTableRequestRequestTypeDef, _OptionalUpdateTableRequestRequestTypeDef
):
    pass

DataModelConfigurationTypeDef = TypedDict(
    "DataModelConfigurationTypeDef",
    {
        "DataModel": DataModelTypeDef,
        "DataModelS3Configuration": DataModelS3ConfigurationTypeDef,
    },
    total=False,
)

CreateTableResponseTypeDef = TypedDict(
    "CreateTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTableResponseTypeDef = TypedDict(
    "DescribeTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTablesResponseTypeDef = TypedDict(
    "ListTablesResponseTypeDef",
    {
        "Tables": List[TableTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateTableResponseTypeDef = TypedDict(
    "UpdateTableResponseTypeDef",
    {
        "Table": TableTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchLoadTaskDescriptionTypeDef = TypedDict(
    "BatchLoadTaskDescriptionTypeDef",
    {
        "TaskId": str,
        "ErrorMessage": str,
        "DataSourceConfiguration": DataSourceConfigurationTypeDef,
        "ProgressReport": BatchLoadProgressReportTypeDef,
        "ReportConfiguration": ReportConfigurationTypeDef,
        "DataModelConfiguration": DataModelConfigurationTypeDef,
        "TargetDatabaseName": str,
        "TargetTableName": str,
        "TaskStatus": BatchLoadStatusType,
        "RecordVersion": int,
        "CreationTime": datetime,
        "LastUpdatedTime": datetime,
        "ResumableUntil": datetime,
    },
    total=False,
)

_RequiredCreateBatchLoadTaskRequestRequestTypeDef = TypedDict(
    "_RequiredCreateBatchLoadTaskRequestRequestTypeDef",
    {
        "DataSourceConfiguration": DataSourceConfigurationTypeDef,
        "ReportConfiguration": ReportConfigurationTypeDef,
        "TargetDatabaseName": str,
        "TargetTableName": str,
    },
)
_OptionalCreateBatchLoadTaskRequestRequestTypeDef = TypedDict(
    "_OptionalCreateBatchLoadTaskRequestRequestTypeDef",
    {
        "ClientToken": str,
        "DataModelConfiguration": DataModelConfigurationTypeDef,
        "RecordVersion": int,
    },
    total=False,
)

class CreateBatchLoadTaskRequestRequestTypeDef(
    _RequiredCreateBatchLoadTaskRequestRequestTypeDef,
    _OptionalCreateBatchLoadTaskRequestRequestTypeDef,
):
    pass

DescribeBatchLoadTaskResponseTypeDef = TypedDict(
    "DescribeBatchLoadTaskResponseTypeDef",
    {
        "BatchLoadTaskDescription": BatchLoadTaskDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
