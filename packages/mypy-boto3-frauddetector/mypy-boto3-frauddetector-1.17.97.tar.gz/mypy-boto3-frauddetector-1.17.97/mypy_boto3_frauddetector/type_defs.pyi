"""
Type annotations for frauddetector service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_frauddetector/type_defs.html)

Usage::

    ```python
    from mypy_boto3_frauddetector.type_defs import BatchCreateVariableErrorTypeDef

    data: BatchCreateVariableErrorTypeDef = {...}
    ```
"""
import sys
from typing import IO, Dict, List, Union

from .literals import (
    AsyncJobStatusType,
    DataSourceType,
    DataTypeType,
    DetectorVersionStatusType,
    ModelEndpointStatusType,
    ModelInputDataFormatType,
    ModelOutputDataFormatType,
    RuleExecutionModeType,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BatchCreateVariableErrorTypeDef",
    "BatchCreateVariableResultTypeDef",
    "BatchGetVariableErrorTypeDef",
    "BatchGetVariableResultTypeDef",
    "BatchPredictionTypeDef",
    "CreateDetectorVersionResultTypeDef",
    "CreateModelVersionResultTypeDef",
    "CreateRuleResultTypeDef",
    "DataValidationMetricsTypeDef",
    "DescribeDetectorResultTypeDef",
    "DescribeModelVersionsResultTypeDef",
    "DetectorTypeDef",
    "DetectorVersionSummaryTypeDef",
    "EntityTypeDef",
    "EntityTypeTypeDef",
    "EventTypeTypeDef",
    "ExternalEventsDetailTypeDef",
    "ExternalModelTypeDef",
    "FieldValidationMessageTypeDef",
    "FileValidationMessageTypeDef",
    "GetBatchPredictionJobsResultTypeDef",
    "GetDetectorVersionResultTypeDef",
    "GetDetectorsResultTypeDef",
    "GetEntityTypesResultTypeDef",
    "GetEventPredictionResultTypeDef",
    "GetEventTypesResultTypeDef",
    "GetExternalModelsResultTypeDef",
    "GetKMSEncryptionKeyResultTypeDef",
    "GetLabelsResultTypeDef",
    "GetModelVersionResultTypeDef",
    "GetModelsResultTypeDef",
    "GetOutcomesResultTypeDef",
    "GetRulesResultTypeDef",
    "GetVariablesResultTypeDef",
    "KMSKeyTypeDef",
    "LabelSchemaTypeDef",
    "LabelTypeDef",
    "ListTagsForResourceResultTypeDef",
    "MetricDataPointTypeDef",
    "ModelEndpointDataBlobTypeDef",
    "ModelInputConfigurationTypeDef",
    "ModelOutputConfigurationTypeDef",
    "ModelScoresTypeDef",
    "ModelTypeDef",
    "ModelVersionDetailTypeDef",
    "ModelVersionTypeDef",
    "OutcomeTypeDef",
    "RuleDetailTypeDef",
    "RuleResultTypeDef",
    "RuleTypeDef",
    "TagTypeDef",
    "TrainingDataSchemaTypeDef",
    "TrainingMetricsTypeDef",
    "TrainingResultTypeDef",
    "UpdateModelVersionResultTypeDef",
    "UpdateRuleVersionResultTypeDef",
    "VariableEntryTypeDef",
    "VariableTypeDef",
)

BatchCreateVariableErrorTypeDef = TypedDict(
    "BatchCreateVariableErrorTypeDef",
    {
        "name": str,
        "code": int,
        "message": str,
    },
    total=False,
)

BatchCreateVariableResultTypeDef = TypedDict(
    "BatchCreateVariableResultTypeDef",
    {
        "errors": List["BatchCreateVariableErrorTypeDef"],
    },
    total=False,
)

BatchGetVariableErrorTypeDef = TypedDict(
    "BatchGetVariableErrorTypeDef",
    {
        "name": str,
        "code": int,
        "message": str,
    },
    total=False,
)

BatchGetVariableResultTypeDef = TypedDict(
    "BatchGetVariableResultTypeDef",
    {
        "variables": List["VariableTypeDef"],
        "errors": List["BatchGetVariableErrorTypeDef"],
    },
    total=False,
)

BatchPredictionTypeDef = TypedDict(
    "BatchPredictionTypeDef",
    {
        "jobId": str,
        "status": AsyncJobStatusType,
        "failureReason": str,
        "startTime": str,
        "completionTime": str,
        "lastHeartbeatTime": str,
        "inputPath": str,
        "outputPath": str,
        "eventTypeName": str,
        "detectorName": str,
        "detectorVersion": str,
        "iamRoleArn": str,
        "arn": str,
        "processedRecordsCount": int,
        "totalRecordsCount": int,
    },
    total=False,
)

CreateDetectorVersionResultTypeDef = TypedDict(
    "CreateDetectorVersionResultTypeDef",
    {
        "detectorId": str,
        "detectorVersionId": str,
        "status": DetectorVersionStatusType,
    },
    total=False,
)

CreateModelVersionResultTypeDef = TypedDict(
    "CreateModelVersionResultTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "status": str,
    },
    total=False,
)

CreateRuleResultTypeDef = TypedDict(
    "CreateRuleResultTypeDef",
    {
        "rule": "RuleTypeDef",
    },
    total=False,
)

DataValidationMetricsTypeDef = TypedDict(
    "DataValidationMetricsTypeDef",
    {
        "fileLevelMessages": List["FileValidationMessageTypeDef"],
        "fieldLevelMessages": List["FieldValidationMessageTypeDef"],
    },
    total=False,
)

DescribeDetectorResultTypeDef = TypedDict(
    "DescribeDetectorResultTypeDef",
    {
        "detectorId": str,
        "detectorVersionSummaries": List["DetectorVersionSummaryTypeDef"],
        "nextToken": str,
        "arn": str,
    },
    total=False,
)

DescribeModelVersionsResultTypeDef = TypedDict(
    "DescribeModelVersionsResultTypeDef",
    {
        "modelVersionDetails": List["ModelVersionDetailTypeDef"],
        "nextToken": str,
    },
    total=False,
)

DetectorTypeDef = TypedDict(
    "DetectorTypeDef",
    {
        "detectorId": str,
        "description": str,
        "eventTypeName": str,
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

DetectorVersionSummaryTypeDef = TypedDict(
    "DetectorVersionSummaryTypeDef",
    {
        "detectorVersionId": str,
        "status": DetectorVersionStatusType,
        "description": str,
        "lastUpdatedTime": str,
    },
    total=False,
)

EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "entityType": str,
        "entityId": str,
    },
)

EntityTypeTypeDef = TypedDict(
    "EntityTypeTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

EventTypeTypeDef = TypedDict(
    "EventTypeTypeDef",
    {
        "name": str,
        "description": str,
        "eventVariables": List[str],
        "labels": List[str],
        "entityTypes": List[str],
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

ExternalEventsDetailTypeDef = TypedDict(
    "ExternalEventsDetailTypeDef",
    {
        "dataLocation": str,
        "dataAccessRoleArn": str,
    },
)

ExternalModelTypeDef = TypedDict(
    "ExternalModelTypeDef",
    {
        "modelEndpoint": str,
        "modelSource": Literal["SAGEMAKER"],
        "invokeModelEndpointRoleArn": str,
        "inputConfiguration": "ModelInputConfigurationTypeDef",
        "outputConfiguration": "ModelOutputConfigurationTypeDef",
        "modelEndpointStatus": ModelEndpointStatusType,
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

FieldValidationMessageTypeDef = TypedDict(
    "FieldValidationMessageTypeDef",
    {
        "fieldName": str,
        "identifier": str,
        "title": str,
        "content": str,
        "type": str,
    },
    total=False,
)

FileValidationMessageTypeDef = TypedDict(
    "FileValidationMessageTypeDef",
    {
        "title": str,
        "content": str,
        "type": str,
    },
    total=False,
)

GetBatchPredictionJobsResultTypeDef = TypedDict(
    "GetBatchPredictionJobsResultTypeDef",
    {
        "batchPredictions": List["BatchPredictionTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetDetectorVersionResultTypeDef = TypedDict(
    "GetDetectorVersionResultTypeDef",
    {
        "detectorId": str,
        "detectorVersionId": str,
        "description": str,
        "externalModelEndpoints": List[str],
        "modelVersions": List["ModelVersionTypeDef"],
        "rules": List["RuleTypeDef"],
        "status": DetectorVersionStatusType,
        "lastUpdatedTime": str,
        "createdTime": str,
        "ruleExecutionMode": RuleExecutionModeType,
        "arn": str,
    },
    total=False,
)

GetDetectorsResultTypeDef = TypedDict(
    "GetDetectorsResultTypeDef",
    {
        "detectors": List["DetectorTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetEntityTypesResultTypeDef = TypedDict(
    "GetEntityTypesResultTypeDef",
    {
        "entityTypes": List["EntityTypeTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetEventPredictionResultTypeDef = TypedDict(
    "GetEventPredictionResultTypeDef",
    {
        "modelScores": List["ModelScoresTypeDef"],
        "ruleResults": List["RuleResultTypeDef"],
    },
    total=False,
)

GetEventTypesResultTypeDef = TypedDict(
    "GetEventTypesResultTypeDef",
    {
        "eventTypes": List["EventTypeTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetExternalModelsResultTypeDef = TypedDict(
    "GetExternalModelsResultTypeDef",
    {
        "externalModels": List["ExternalModelTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetKMSEncryptionKeyResultTypeDef = TypedDict(
    "GetKMSEncryptionKeyResultTypeDef",
    {
        "kmsKey": "KMSKeyTypeDef",
    },
    total=False,
)

GetLabelsResultTypeDef = TypedDict(
    "GetLabelsResultTypeDef",
    {
        "labels": List["LabelTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetModelVersionResultTypeDef = TypedDict(
    "GetModelVersionResultTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "trainingDataSource": Literal["EXTERNAL_EVENTS"],
        "trainingDataSchema": "TrainingDataSchemaTypeDef",
        "externalEventsDetail": "ExternalEventsDetailTypeDef",
        "status": str,
        "arn": str,
    },
    total=False,
)

GetModelsResultTypeDef = TypedDict(
    "GetModelsResultTypeDef",
    {
        "nextToken": str,
        "models": List["ModelTypeDef"],
    },
    total=False,
)

GetOutcomesResultTypeDef = TypedDict(
    "GetOutcomesResultTypeDef",
    {
        "outcomes": List["OutcomeTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetRulesResultTypeDef = TypedDict(
    "GetRulesResultTypeDef",
    {
        "ruleDetails": List["RuleDetailTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetVariablesResultTypeDef = TypedDict(
    "GetVariablesResultTypeDef",
    {
        "variables": List["VariableTypeDef"],
        "nextToken": str,
    },
    total=False,
)

KMSKeyTypeDef = TypedDict(
    "KMSKeyTypeDef",
    {
        "kmsEncryptionKeyArn": str,
    },
    total=False,
)

LabelSchemaTypeDef = TypedDict(
    "LabelSchemaTypeDef",
    {
        "labelMapper": Dict[str, List[str]],
    },
)

LabelTypeDef = TypedDict(
    "LabelTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "tags": List["TagTypeDef"],
        "nextToken": str,
    },
    total=False,
)

MetricDataPointTypeDef = TypedDict(
    "MetricDataPointTypeDef",
    {
        "fpr": float,
        "precision": float,
        "tpr": float,
        "threshold": float,
    },
    total=False,
)

ModelEndpointDataBlobTypeDef = TypedDict(
    "ModelEndpointDataBlobTypeDef",
    {
        "byteBuffer": Union[bytes, IO[bytes]],
        "contentType": str,
    },
    total=False,
)

_RequiredModelInputConfigurationTypeDef = TypedDict(
    "_RequiredModelInputConfigurationTypeDef",
    {
        "useEventVariables": bool,
    },
)
_OptionalModelInputConfigurationTypeDef = TypedDict(
    "_OptionalModelInputConfigurationTypeDef",
    {
        "eventTypeName": str,
        "format": ModelInputDataFormatType,
        "jsonInputTemplate": str,
        "csvInputTemplate": str,
    },
    total=False,
)

class ModelInputConfigurationTypeDef(
    _RequiredModelInputConfigurationTypeDef, _OptionalModelInputConfigurationTypeDef
):
    pass

_RequiredModelOutputConfigurationTypeDef = TypedDict(
    "_RequiredModelOutputConfigurationTypeDef",
    {
        "format": ModelOutputDataFormatType,
    },
)
_OptionalModelOutputConfigurationTypeDef = TypedDict(
    "_OptionalModelOutputConfigurationTypeDef",
    {
        "jsonKeyToVariableMap": Dict[str, str],
        "csvIndexToVariableMap": Dict[str, str],
    },
    total=False,
)

class ModelOutputConfigurationTypeDef(
    _RequiredModelOutputConfigurationTypeDef, _OptionalModelOutputConfigurationTypeDef
):
    pass

ModelScoresTypeDef = TypedDict(
    "ModelScoresTypeDef",
    {
        "modelVersion": "ModelVersionTypeDef",
        "scores": Dict[str, float],
    },
    total=False,
)

ModelTypeDef = TypedDict(
    "ModelTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "description": str,
        "eventTypeName": str,
        "createdTime": str,
        "lastUpdatedTime": str,
        "arn": str,
    },
    total=False,
)

ModelVersionDetailTypeDef = TypedDict(
    "ModelVersionDetailTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "status": str,
        "trainingDataSource": Literal["EXTERNAL_EVENTS"],
        "trainingDataSchema": "TrainingDataSchemaTypeDef",
        "externalEventsDetail": "ExternalEventsDetailTypeDef",
        "trainingResult": "TrainingResultTypeDef",
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

_RequiredModelVersionTypeDef = TypedDict(
    "_RequiredModelVersionTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
    },
)
_OptionalModelVersionTypeDef = TypedDict(
    "_OptionalModelVersionTypeDef",
    {
        "arn": str,
    },
    total=False,
)

class ModelVersionTypeDef(_RequiredModelVersionTypeDef, _OptionalModelVersionTypeDef):
    pass

OutcomeTypeDef = TypedDict(
    "OutcomeTypeDef",
    {
        "name": str,
        "description": str,
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

RuleDetailTypeDef = TypedDict(
    "RuleDetailTypeDef",
    {
        "ruleId": str,
        "description": str,
        "detectorId": str,
        "ruleVersion": str,
        "expression": str,
        "language": Literal["DETECTORPL"],
        "outcomes": List[str],
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)

RuleResultTypeDef = TypedDict(
    "RuleResultTypeDef",
    {
        "ruleId": str,
        "outcomes": List[str],
    },
    total=False,
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "detectorId": str,
        "ruleId": str,
        "ruleVersion": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

TrainingDataSchemaTypeDef = TypedDict(
    "TrainingDataSchemaTypeDef",
    {
        "modelVariables": List[str],
        "labelSchema": "LabelSchemaTypeDef",
    },
)

TrainingMetricsTypeDef = TypedDict(
    "TrainingMetricsTypeDef",
    {
        "auc": float,
        "metricDataPoints": List["MetricDataPointTypeDef"],
    },
    total=False,
)

TrainingResultTypeDef = TypedDict(
    "TrainingResultTypeDef",
    {
        "dataValidationMetrics": "DataValidationMetricsTypeDef",
        "trainingMetrics": "TrainingMetricsTypeDef",
    },
    total=False,
)

UpdateModelVersionResultTypeDef = TypedDict(
    "UpdateModelVersionResultTypeDef",
    {
        "modelId": str,
        "modelType": Literal["ONLINE_FRAUD_INSIGHTS"],
        "modelVersionNumber": str,
        "status": str,
    },
    total=False,
)

UpdateRuleVersionResultTypeDef = TypedDict(
    "UpdateRuleVersionResultTypeDef",
    {
        "rule": "RuleTypeDef",
    },
    total=False,
)

VariableEntryTypeDef = TypedDict(
    "VariableEntryTypeDef",
    {
        "name": str,
        "dataType": str,
        "dataSource": str,
        "defaultValue": str,
        "description": str,
        "variableType": str,
    },
    total=False,
)

VariableTypeDef = TypedDict(
    "VariableTypeDef",
    {
        "name": str,
        "dataType": DataTypeType,
        "dataSource": DataSourceType,
        "defaultValue": str,
        "description": str,
        "variableType": str,
        "lastUpdatedTime": str,
        "createdTime": str,
        "arn": str,
    },
    total=False,
)
