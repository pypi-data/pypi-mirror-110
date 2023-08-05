"""
Type annotations for iot service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_iot/type_defs.html)

Usage::

    ```python
    from mypy_boto3_iot.type_defs import AbortConfigTypeDef

    data: AbortConfigTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Dict, List, Union

from .literals import (
    ActionTypeType,
    AuditCheckRunStatusType,
    AuditFindingSeverityType,
    AuditFrequencyType,
    AuditMitigationActionsExecutionStatusType,
    AuditMitigationActionsTaskStatusType,
    AuditTaskStatusType,
    AuditTaskTypeType,
    AuthDecisionType,
    AuthorizerStatusType,
    AutoRegistrationStatusType,
    AwsJobAbortCriteriaFailureTypeType,
    CACertificateStatusType,
    CannedAccessControlListType,
    CertificateModeType,
    CertificateStatusType,
    ComparisonOperatorType,
    ConfidenceLevelType,
    CustomMetricTypeType,
    DayOfWeekType,
    DetectMitigationActionExecutionStatusType,
    DetectMitigationActionsTaskStatusType,
    DimensionValueOperatorType,
    DomainConfigurationStatusType,
    DomainTypeType,
    DynamicGroupStatusType,
    DynamoKeyTypeType,
    EventTypeType,
    FieldTypeType,
    IndexStatusType,
    JobExecutionFailureTypeType,
    JobExecutionStatusType,
    JobStatusType,
    LogLevelType,
    LogTargetTypeType,
    MessageFormatType,
    MitigationActionTypeType,
    ModelStatusType,
    OTAUpdateStatusType,
    ProtocolType,
    ReportTypeType,
    ResourceTypeType,
    ServerCertificateStatusType,
    ServiceTypeType,
    StatusType,
    TargetSelectionType,
    ThingConnectivityIndexingModeType,
    ThingGroupIndexingModeType,
    ThingIndexingModeType,
    TopicRuleDestinationStatusType,
    ViolationEventTypeType,
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
    "AbortConfigTypeDef",
    "AbortCriteriaTypeDef",
    "ActionTypeDef",
    "ActiveViolationTypeDef",
    "AddThingsToThingGroupParamsTypeDef",
    "AlertTargetTypeDef",
    "AllowedTypeDef",
    "AssetPropertyTimestampTypeDef",
    "AssetPropertyValueTypeDef",
    "AssetPropertyVariantTypeDef",
    "AssociateTargetsWithJobResponseTypeDef",
    "AttributePayloadTypeDef",
    "AuditCheckConfigurationTypeDef",
    "AuditCheckDetailsTypeDef",
    "AuditFindingTypeDef",
    "AuditMitigationActionExecutionMetadataTypeDef",
    "AuditMitigationActionsTaskMetadataTypeDef",
    "AuditMitigationActionsTaskTargetTypeDef",
    "AuditNotificationTargetTypeDef",
    "AuditSuppressionTypeDef",
    "AuditTaskMetadataTypeDef",
    "AuthInfoTypeDef",
    "AuthResultTypeDef",
    "AuthorizerConfigTypeDef",
    "AuthorizerDescriptionTypeDef",
    "AuthorizerSummaryTypeDef",
    "AwsJobAbortConfigTypeDef",
    "AwsJobAbortCriteriaTypeDef",
    "AwsJobExecutionsRolloutConfigTypeDef",
    "AwsJobExponentialRolloutRateTypeDef",
    "AwsJobPresignedUrlConfigTypeDef",
    "AwsJobRateIncreaseCriteriaTypeDef",
    "AwsJobTimeoutConfigTypeDef",
    "BehaviorCriteriaTypeDef",
    "BehaviorModelTrainingSummaryTypeDef",
    "BehaviorTypeDef",
    "BillingGroupMetadataTypeDef",
    "BillingGroupPropertiesTypeDef",
    "CACertificateDescriptionTypeDef",
    "CACertificateTypeDef",
    "CancelJobResponseTypeDef",
    "CertificateDescriptionTypeDef",
    "CertificateTypeDef",
    "CertificateValidityTypeDef",
    "CloudwatchAlarmActionTypeDef",
    "CloudwatchLogsActionTypeDef",
    "CloudwatchMetricActionTypeDef",
    "CodeSigningCertificateChainTypeDef",
    "CodeSigningSignatureTypeDef",
    "CodeSigningTypeDef",
    "ConfigurationTypeDef",
    "CreateAuthorizerResponseTypeDef",
    "CreateBillingGroupResponseTypeDef",
    "CreateCertificateFromCsrResponseTypeDef",
    "CreateCustomMetricResponseTypeDef",
    "CreateDimensionResponseTypeDef",
    "CreateDomainConfigurationResponseTypeDef",
    "CreateDynamicThingGroupResponseTypeDef",
    "CreateJobResponseTypeDef",
    "CreateJobTemplateResponseTypeDef",
    "CreateKeysAndCertificateResponseTypeDef",
    "CreateMitigationActionResponseTypeDef",
    "CreateOTAUpdateResponseTypeDef",
    "CreatePolicyResponseTypeDef",
    "CreatePolicyVersionResponseTypeDef",
    "CreateProvisioningClaimResponseTypeDef",
    "CreateProvisioningTemplateResponseTypeDef",
    "CreateProvisioningTemplateVersionResponseTypeDef",
    "CreateRoleAliasResponseTypeDef",
    "CreateScheduledAuditResponseTypeDef",
    "CreateSecurityProfileResponseTypeDef",
    "CreateStreamResponseTypeDef",
    "CreateThingGroupResponseTypeDef",
    "CreateThingResponseTypeDef",
    "CreateThingTypeResponseTypeDef",
    "CreateTopicRuleDestinationResponseTypeDef",
    "CustomCodeSigningTypeDef",
    "DeniedTypeDef",
    "DescribeAccountAuditConfigurationResponseTypeDef",
    "DescribeAuditFindingResponseTypeDef",
    "DescribeAuditMitigationActionsTaskResponseTypeDef",
    "DescribeAuditSuppressionResponseTypeDef",
    "DescribeAuditTaskResponseTypeDef",
    "DescribeAuthorizerResponseTypeDef",
    "DescribeBillingGroupResponseTypeDef",
    "DescribeCACertificateResponseTypeDef",
    "DescribeCertificateResponseTypeDef",
    "DescribeCustomMetricResponseTypeDef",
    "DescribeDefaultAuthorizerResponseTypeDef",
    "DescribeDetectMitigationActionsTaskResponseTypeDef",
    "DescribeDimensionResponseTypeDef",
    "DescribeDomainConfigurationResponseTypeDef",
    "DescribeEndpointResponseTypeDef",
    "DescribeEventConfigurationsResponseTypeDef",
    "DescribeIndexResponseTypeDef",
    "DescribeJobExecutionResponseTypeDef",
    "DescribeJobResponseTypeDef",
    "DescribeJobTemplateResponseTypeDef",
    "DescribeMitigationActionResponseTypeDef",
    "DescribeProvisioningTemplateResponseTypeDef",
    "DescribeProvisioningTemplateVersionResponseTypeDef",
    "DescribeRoleAliasResponseTypeDef",
    "DescribeScheduledAuditResponseTypeDef",
    "DescribeSecurityProfileResponseTypeDef",
    "DescribeStreamResponseTypeDef",
    "DescribeThingGroupResponseTypeDef",
    "DescribeThingRegistrationTaskResponseTypeDef",
    "DescribeThingResponseTypeDef",
    "DescribeThingTypeResponseTypeDef",
    "DestinationTypeDef",
    "DetectMitigationActionExecutionTypeDef",
    "DetectMitigationActionsTaskStatisticsTypeDef",
    "DetectMitigationActionsTaskSummaryTypeDef",
    "DetectMitigationActionsTaskTargetTypeDef",
    "DomainConfigurationSummaryTypeDef",
    "DynamoDBActionTypeDef",
    "DynamoDBv2ActionTypeDef",
    "EffectivePolicyTypeDef",
    "ElasticsearchActionTypeDef",
    "EnableIoTLoggingParamsTypeDef",
    "ErrorInfoTypeDef",
    "ExplicitDenyTypeDef",
    "ExponentialRolloutRateTypeDef",
    "FieldTypeDef",
    "FileLocationTypeDef",
    "FirehoseActionTypeDef",
    "GetBehaviorModelTrainingSummariesResponseTypeDef",
    "GetCardinalityResponseTypeDef",
    "GetEffectivePoliciesResponseTypeDef",
    "GetIndexingConfigurationResponseTypeDef",
    "GetJobDocumentResponseTypeDef",
    "GetLoggingOptionsResponseTypeDef",
    "GetOTAUpdateResponseTypeDef",
    "GetPercentilesResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "GetPolicyVersionResponseTypeDef",
    "GetRegistrationCodeResponseTypeDef",
    "GetStatisticsResponseTypeDef",
    "GetTopicRuleDestinationResponseTypeDef",
    "GetTopicRuleResponseTypeDef",
    "GetV2LoggingOptionsResponseTypeDef",
    "GroupNameAndArnTypeDef",
    "HttpActionHeaderTypeDef",
    "HttpActionTypeDef",
    "HttpAuthorizationTypeDef",
    "HttpContextTypeDef",
    "HttpUrlDestinationConfigurationTypeDef",
    "HttpUrlDestinationPropertiesTypeDef",
    "HttpUrlDestinationSummaryTypeDef",
    "ImplicitDenyTypeDef",
    "IotAnalyticsActionTypeDef",
    "IotEventsActionTypeDef",
    "IotSiteWiseActionTypeDef",
    "JobExecutionStatusDetailsTypeDef",
    "JobExecutionSummaryForJobTypeDef",
    "JobExecutionSummaryForThingTypeDef",
    "JobExecutionSummaryTypeDef",
    "JobExecutionTypeDef",
    "JobExecutionsRolloutConfigTypeDef",
    "JobProcessDetailsTypeDef",
    "JobSummaryTypeDef",
    "JobTemplateSummaryTypeDef",
    "JobTypeDef",
    "KafkaActionTypeDef",
    "KeyPairTypeDef",
    "KinesisActionTypeDef",
    "LambdaActionTypeDef",
    "ListActiveViolationsResponseTypeDef",
    "ListAttachedPoliciesResponseTypeDef",
    "ListAuditFindingsResponseTypeDef",
    "ListAuditMitigationActionsExecutionsResponseTypeDef",
    "ListAuditMitigationActionsTasksResponseTypeDef",
    "ListAuditSuppressionsResponseTypeDef",
    "ListAuditTasksResponseTypeDef",
    "ListAuthorizersResponseTypeDef",
    "ListBillingGroupsResponseTypeDef",
    "ListCACertificatesResponseTypeDef",
    "ListCertificatesByCAResponseTypeDef",
    "ListCertificatesResponseTypeDef",
    "ListCustomMetricsResponseTypeDef",
    "ListDetectMitigationActionsExecutionsResponseTypeDef",
    "ListDetectMitigationActionsTasksResponseTypeDef",
    "ListDimensionsResponseTypeDef",
    "ListDomainConfigurationsResponseTypeDef",
    "ListIndicesResponseTypeDef",
    "ListJobExecutionsForJobResponseTypeDef",
    "ListJobExecutionsForThingResponseTypeDef",
    "ListJobTemplatesResponseTypeDef",
    "ListJobsResponseTypeDef",
    "ListMitigationActionsResponseTypeDef",
    "ListOTAUpdatesResponseTypeDef",
    "ListOutgoingCertificatesResponseTypeDef",
    "ListPoliciesResponseTypeDef",
    "ListPolicyPrincipalsResponseTypeDef",
    "ListPolicyVersionsResponseTypeDef",
    "ListPrincipalPoliciesResponseTypeDef",
    "ListPrincipalThingsResponseTypeDef",
    "ListProvisioningTemplateVersionsResponseTypeDef",
    "ListProvisioningTemplatesResponseTypeDef",
    "ListRoleAliasesResponseTypeDef",
    "ListScheduledAuditsResponseTypeDef",
    "ListSecurityProfilesForTargetResponseTypeDef",
    "ListSecurityProfilesResponseTypeDef",
    "ListStreamsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetsForPolicyResponseTypeDef",
    "ListTargetsForSecurityProfileResponseTypeDef",
    "ListThingGroupsForThingResponseTypeDef",
    "ListThingGroupsResponseTypeDef",
    "ListThingPrincipalsResponseTypeDef",
    "ListThingRegistrationTaskReportsResponseTypeDef",
    "ListThingRegistrationTasksResponseTypeDef",
    "ListThingTypesResponseTypeDef",
    "ListThingsInBillingGroupResponseTypeDef",
    "ListThingsInThingGroupResponseTypeDef",
    "ListThingsResponseTypeDef",
    "ListTopicRuleDestinationsResponseTypeDef",
    "ListTopicRulesResponseTypeDef",
    "ListV2LoggingLevelsResponseTypeDef",
    "ListViolationEventsResponseTypeDef",
    "LogTargetConfigurationTypeDef",
    "LogTargetTypeDef",
    "LoggingOptionsPayloadTypeDef",
    "MachineLearningDetectionConfigTypeDef",
    "MetricDimensionTypeDef",
    "MetricToRetainTypeDef",
    "MetricValueTypeDef",
    "MitigationActionIdentifierTypeDef",
    "MitigationActionParamsTypeDef",
    "MitigationActionTypeDef",
    "MqttContextTypeDef",
    "NonCompliantResourceTypeDef",
    "OTAUpdateFileTypeDef",
    "OTAUpdateInfoTypeDef",
    "OTAUpdateSummaryTypeDef",
    "OutgoingCertificateTypeDef",
    "PaginatorConfigTypeDef",
    "PercentPairTypeDef",
    "PolicyTypeDef",
    "PolicyVersionIdentifierTypeDef",
    "PolicyVersionTypeDef",
    "PresignedUrlConfigTypeDef",
    "ProvisioningHookTypeDef",
    "ProvisioningTemplateSummaryTypeDef",
    "ProvisioningTemplateVersionSummaryTypeDef",
    "PublishFindingToSnsParamsTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "PutItemInputTypeDef",
    "RateIncreaseCriteriaTypeDef",
    "RegisterCACertificateResponseTypeDef",
    "RegisterCertificateResponseTypeDef",
    "RegisterCertificateWithoutCAResponseTypeDef",
    "RegisterThingResponseTypeDef",
    "RegistrationConfigTypeDef",
    "RelatedResourceTypeDef",
    "ReplaceDefaultPolicyVersionParamsTypeDef",
    "RepublishActionTypeDef",
    "ResourceIdentifierTypeDef",
    "RoleAliasDescriptionTypeDef",
    "S3ActionTypeDef",
    "S3DestinationTypeDef",
    "S3LocationTypeDef",
    "SalesforceActionTypeDef",
    "ScheduledAuditMetadataTypeDef",
    "SearchIndexResponseTypeDef",
    "SecurityProfileIdentifierTypeDef",
    "SecurityProfileTargetMappingTypeDef",
    "SecurityProfileTargetTypeDef",
    "ServerCertificateSummaryTypeDef",
    "SetDefaultAuthorizerResponseTypeDef",
    "SigV4AuthorizationTypeDef",
    "SigningProfileParameterTypeDef",
    "SnsActionTypeDef",
    "SqsActionTypeDef",
    "StartAuditMitigationActionsTaskResponseTypeDef",
    "StartDetectMitigationActionsTaskResponseTypeDef",
    "StartOnDemandAuditTaskResponseTypeDef",
    "StartSigningJobParameterTypeDef",
    "StartThingRegistrationTaskResponseTypeDef",
    "StatisticalThresholdTypeDef",
    "StatisticsTypeDef",
    "StepFunctionsActionTypeDef",
    "StreamFileTypeDef",
    "StreamInfoTypeDef",
    "StreamSummaryTypeDef",
    "StreamTypeDef",
    "TagTypeDef",
    "TaskStatisticsForAuditCheckTypeDef",
    "TaskStatisticsTypeDef",
    "TestAuthorizationResponseTypeDef",
    "TestInvokeAuthorizerResponseTypeDef",
    "ThingAttributeTypeDef",
    "ThingConnectivityTypeDef",
    "ThingDocumentTypeDef",
    "ThingGroupDocumentTypeDef",
    "ThingGroupIndexingConfigurationTypeDef",
    "ThingGroupMetadataTypeDef",
    "ThingGroupPropertiesTypeDef",
    "ThingIndexingConfigurationTypeDef",
    "ThingTypeDefinitionTypeDef",
    "ThingTypeMetadataTypeDef",
    "ThingTypePropertiesTypeDef",
    "TimeoutConfigTypeDef",
    "TimestreamActionTypeDef",
    "TimestreamDimensionTypeDef",
    "TimestreamTimestampTypeDef",
    "TlsContextTypeDef",
    "TopicRuleDestinationConfigurationTypeDef",
    "TopicRuleDestinationSummaryTypeDef",
    "TopicRuleDestinationTypeDef",
    "TopicRuleListItemTypeDef",
    "TopicRulePayloadTypeDef",
    "TopicRuleTypeDef",
    "TransferCertificateResponseTypeDef",
    "TransferDataTypeDef",
    "UpdateAuthorizerResponseTypeDef",
    "UpdateBillingGroupResponseTypeDef",
    "UpdateCACertificateParamsTypeDef",
    "UpdateCustomMetricResponseTypeDef",
    "UpdateDeviceCertificateParamsTypeDef",
    "UpdateDimensionResponseTypeDef",
    "UpdateDomainConfigurationResponseTypeDef",
    "UpdateDynamicThingGroupResponseTypeDef",
    "UpdateMitigationActionResponseTypeDef",
    "UpdateRoleAliasResponseTypeDef",
    "UpdateScheduledAuditResponseTypeDef",
    "UpdateSecurityProfileResponseTypeDef",
    "UpdateStreamResponseTypeDef",
    "UpdateThingGroupResponseTypeDef",
    "ValidateSecurityProfileBehaviorsResponseTypeDef",
    "ValidationErrorTypeDef",
    "ViolationEventAdditionalInfoTypeDef",
    "ViolationEventOccurrenceRangeTypeDef",
    "ViolationEventTypeDef",
    "VpcDestinationConfigurationTypeDef",
    "VpcDestinationPropertiesTypeDef",
    "VpcDestinationSummaryTypeDef",
)

AbortConfigTypeDef = TypedDict(
    "AbortConfigTypeDef",
    {
        "criteriaList": List["AbortCriteriaTypeDef"],
    },
)

AbortCriteriaTypeDef = TypedDict(
    "AbortCriteriaTypeDef",
    {
        "failureType": JobExecutionFailureTypeType,
        "action": Literal["CANCEL"],
        "thresholdPercentage": float,
        "minNumberOfExecutedThings": int,
    },
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "dynamoDB": "DynamoDBActionTypeDef",
        "dynamoDBv2": "DynamoDBv2ActionTypeDef",
        "lambda": "LambdaActionTypeDef",
        "sns": "SnsActionTypeDef",
        "sqs": "SqsActionTypeDef",
        "kinesis": "KinesisActionTypeDef",
        "republish": "RepublishActionTypeDef",
        "s3": "S3ActionTypeDef",
        "firehose": "FirehoseActionTypeDef",
        "cloudwatchMetric": "CloudwatchMetricActionTypeDef",
        "cloudwatchAlarm": "CloudwatchAlarmActionTypeDef",
        "cloudwatchLogs": "CloudwatchLogsActionTypeDef",
        "elasticsearch": "ElasticsearchActionTypeDef",
        "salesforce": "SalesforceActionTypeDef",
        "iotAnalytics": "IotAnalyticsActionTypeDef",
        "iotEvents": "IotEventsActionTypeDef",
        "iotSiteWise": "IotSiteWiseActionTypeDef",
        "stepFunctions": "StepFunctionsActionTypeDef",
        "timestream": "TimestreamActionTypeDef",
        "http": "HttpActionTypeDef",
        "kafka": "KafkaActionTypeDef",
    },
    total=False,
)

ActiveViolationTypeDef = TypedDict(
    "ActiveViolationTypeDef",
    {
        "violationId": str,
        "thingName": str,
        "securityProfileName": str,
        "behavior": "BehaviorTypeDef",
        "lastViolationValue": "MetricValueTypeDef",
        "violationEventAdditionalInfo": "ViolationEventAdditionalInfoTypeDef",
        "lastViolationTime": datetime,
        "violationStartTime": datetime,
    },
    total=False,
)

_RequiredAddThingsToThingGroupParamsTypeDef = TypedDict(
    "_RequiredAddThingsToThingGroupParamsTypeDef",
    {
        "thingGroupNames": List[str],
    },
)
_OptionalAddThingsToThingGroupParamsTypeDef = TypedDict(
    "_OptionalAddThingsToThingGroupParamsTypeDef",
    {
        "overrideDynamicGroups": bool,
    },
    total=False,
)


class AddThingsToThingGroupParamsTypeDef(
    _RequiredAddThingsToThingGroupParamsTypeDef, _OptionalAddThingsToThingGroupParamsTypeDef
):
    pass


AlertTargetTypeDef = TypedDict(
    "AlertTargetTypeDef",
    {
        "alertTargetArn": str,
        "roleArn": str,
    },
)

AllowedTypeDef = TypedDict(
    "AllowedTypeDef",
    {
        "policies": List["PolicyTypeDef"],
    },
    total=False,
)

_RequiredAssetPropertyTimestampTypeDef = TypedDict(
    "_RequiredAssetPropertyTimestampTypeDef",
    {
        "timeInSeconds": str,
    },
)
_OptionalAssetPropertyTimestampTypeDef = TypedDict(
    "_OptionalAssetPropertyTimestampTypeDef",
    {
        "offsetInNanos": str,
    },
    total=False,
)


class AssetPropertyTimestampTypeDef(
    _RequiredAssetPropertyTimestampTypeDef, _OptionalAssetPropertyTimestampTypeDef
):
    pass


_RequiredAssetPropertyValueTypeDef = TypedDict(
    "_RequiredAssetPropertyValueTypeDef",
    {
        "value": "AssetPropertyVariantTypeDef",
        "timestamp": "AssetPropertyTimestampTypeDef",
    },
)
_OptionalAssetPropertyValueTypeDef = TypedDict(
    "_OptionalAssetPropertyValueTypeDef",
    {
        "quality": str,
    },
    total=False,
)


class AssetPropertyValueTypeDef(
    _RequiredAssetPropertyValueTypeDef, _OptionalAssetPropertyValueTypeDef
):
    pass


AssetPropertyVariantTypeDef = TypedDict(
    "AssetPropertyVariantTypeDef",
    {
        "stringValue": str,
        "integerValue": str,
        "doubleValue": str,
        "booleanValue": str,
    },
    total=False,
)

AssociateTargetsWithJobResponseTypeDef = TypedDict(
    "AssociateTargetsWithJobResponseTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "description": str,
    },
    total=False,
)

AttributePayloadTypeDef = TypedDict(
    "AttributePayloadTypeDef",
    {
        "attributes": Dict[str, str],
        "merge": bool,
    },
    total=False,
)

AuditCheckConfigurationTypeDef = TypedDict(
    "AuditCheckConfigurationTypeDef",
    {
        "enabled": bool,
    },
    total=False,
)

AuditCheckDetailsTypeDef = TypedDict(
    "AuditCheckDetailsTypeDef",
    {
        "checkRunStatus": AuditCheckRunStatusType,
        "checkCompliant": bool,
        "totalResourcesCount": int,
        "nonCompliantResourcesCount": int,
        "suppressedNonCompliantResourcesCount": int,
        "errorCode": str,
        "message": str,
    },
    total=False,
)

AuditFindingTypeDef = TypedDict(
    "AuditFindingTypeDef",
    {
        "findingId": str,
        "taskId": str,
        "checkName": str,
        "taskStartTime": datetime,
        "findingTime": datetime,
        "severity": AuditFindingSeverityType,
        "nonCompliantResource": "NonCompliantResourceTypeDef",
        "relatedResources": List["RelatedResourceTypeDef"],
        "reasonForNonCompliance": str,
        "reasonForNonComplianceCode": str,
        "isSuppressed": bool,
    },
    total=False,
)

AuditMitigationActionExecutionMetadataTypeDef = TypedDict(
    "AuditMitigationActionExecutionMetadataTypeDef",
    {
        "taskId": str,
        "findingId": str,
        "actionName": str,
        "actionId": str,
        "status": AuditMitigationActionsExecutionStatusType,
        "startTime": datetime,
        "endTime": datetime,
        "errorCode": str,
        "message": str,
    },
    total=False,
)

AuditMitigationActionsTaskMetadataTypeDef = TypedDict(
    "AuditMitigationActionsTaskMetadataTypeDef",
    {
        "taskId": str,
        "startTime": datetime,
        "taskStatus": AuditMitigationActionsTaskStatusType,
    },
    total=False,
)

AuditMitigationActionsTaskTargetTypeDef = TypedDict(
    "AuditMitigationActionsTaskTargetTypeDef",
    {
        "auditTaskId": str,
        "findingIds": List[str],
        "auditCheckToReasonCodeFilter": Dict[str, List[str]],
    },
    total=False,
)

AuditNotificationTargetTypeDef = TypedDict(
    "AuditNotificationTargetTypeDef",
    {
        "targetArn": str,
        "roleArn": str,
        "enabled": bool,
    },
    total=False,
)

_RequiredAuditSuppressionTypeDef = TypedDict(
    "_RequiredAuditSuppressionTypeDef",
    {
        "checkName": str,
        "resourceIdentifier": "ResourceIdentifierTypeDef",
    },
)
_OptionalAuditSuppressionTypeDef = TypedDict(
    "_OptionalAuditSuppressionTypeDef",
    {
        "expirationDate": datetime,
        "suppressIndefinitely": bool,
        "description": str,
    },
    total=False,
)


class AuditSuppressionTypeDef(_RequiredAuditSuppressionTypeDef, _OptionalAuditSuppressionTypeDef):
    pass


AuditTaskMetadataTypeDef = TypedDict(
    "AuditTaskMetadataTypeDef",
    {
        "taskId": str,
        "taskStatus": AuditTaskStatusType,
        "taskType": AuditTaskTypeType,
    },
    total=False,
)

_RequiredAuthInfoTypeDef = TypedDict(
    "_RequiredAuthInfoTypeDef",
    {
        "resources": List[str],
    },
)
_OptionalAuthInfoTypeDef = TypedDict(
    "_OptionalAuthInfoTypeDef",
    {
        "actionType": ActionTypeType,
    },
    total=False,
)


class AuthInfoTypeDef(_RequiredAuthInfoTypeDef, _OptionalAuthInfoTypeDef):
    pass


AuthResultTypeDef = TypedDict(
    "AuthResultTypeDef",
    {
        "authInfo": "AuthInfoTypeDef",
        "allowed": "AllowedTypeDef",
        "denied": "DeniedTypeDef",
        "authDecision": AuthDecisionType,
        "missingContextValues": List[str],
    },
    total=False,
)

AuthorizerConfigTypeDef = TypedDict(
    "AuthorizerConfigTypeDef",
    {
        "defaultAuthorizerName": str,
        "allowAuthorizerOverride": bool,
    },
    total=False,
)

AuthorizerDescriptionTypeDef = TypedDict(
    "AuthorizerDescriptionTypeDef",
    {
        "authorizerName": str,
        "authorizerArn": str,
        "authorizerFunctionArn": str,
        "tokenKeyName": str,
        "tokenSigningPublicKeys": Dict[str, str],
        "status": AuthorizerStatusType,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "signingDisabled": bool,
    },
    total=False,
)

AuthorizerSummaryTypeDef = TypedDict(
    "AuthorizerSummaryTypeDef",
    {
        "authorizerName": str,
        "authorizerArn": str,
    },
    total=False,
)

AwsJobAbortConfigTypeDef = TypedDict(
    "AwsJobAbortConfigTypeDef",
    {
        "abortCriteriaList": List["AwsJobAbortCriteriaTypeDef"],
    },
)

AwsJobAbortCriteriaTypeDef = TypedDict(
    "AwsJobAbortCriteriaTypeDef",
    {
        "failureType": AwsJobAbortCriteriaFailureTypeType,
        "action": Literal["CANCEL"],
        "thresholdPercentage": float,
        "minNumberOfExecutedThings": int,
    },
)

AwsJobExecutionsRolloutConfigTypeDef = TypedDict(
    "AwsJobExecutionsRolloutConfigTypeDef",
    {
        "maximumPerMinute": int,
        "exponentialRate": "AwsJobExponentialRolloutRateTypeDef",
    },
    total=False,
)

AwsJobExponentialRolloutRateTypeDef = TypedDict(
    "AwsJobExponentialRolloutRateTypeDef",
    {
        "baseRatePerMinute": int,
        "incrementFactor": float,
        "rateIncreaseCriteria": "AwsJobRateIncreaseCriteriaTypeDef",
    },
)

AwsJobPresignedUrlConfigTypeDef = TypedDict(
    "AwsJobPresignedUrlConfigTypeDef",
    {
        "expiresInSec": int,
    },
    total=False,
)

AwsJobRateIncreaseCriteriaTypeDef = TypedDict(
    "AwsJobRateIncreaseCriteriaTypeDef",
    {
        "numberOfNotifiedThings": int,
        "numberOfSucceededThings": int,
    },
    total=False,
)

AwsJobTimeoutConfigTypeDef = TypedDict(
    "AwsJobTimeoutConfigTypeDef",
    {
        "inProgressTimeoutInMinutes": int,
    },
    total=False,
)

BehaviorCriteriaTypeDef = TypedDict(
    "BehaviorCriteriaTypeDef",
    {
        "comparisonOperator": ComparisonOperatorType,
        "value": "MetricValueTypeDef",
        "durationSeconds": int,
        "consecutiveDatapointsToAlarm": int,
        "consecutiveDatapointsToClear": int,
        "statisticalThreshold": "StatisticalThresholdTypeDef",
        "mlDetectionConfig": "MachineLearningDetectionConfigTypeDef",
    },
    total=False,
)

BehaviorModelTrainingSummaryTypeDef = TypedDict(
    "BehaviorModelTrainingSummaryTypeDef",
    {
        "securityProfileName": str,
        "behaviorName": str,
        "trainingDataCollectionStartDate": datetime,
        "modelStatus": ModelStatusType,
        "datapointsCollectionPercentage": float,
        "lastModelRefreshDate": datetime,
    },
    total=False,
)

_RequiredBehaviorTypeDef = TypedDict(
    "_RequiredBehaviorTypeDef",
    {
        "name": str,
    },
)
_OptionalBehaviorTypeDef = TypedDict(
    "_OptionalBehaviorTypeDef",
    {
        "metric": str,
        "metricDimension": "MetricDimensionTypeDef",
        "criteria": "BehaviorCriteriaTypeDef",
        "suppressAlerts": bool,
    },
    total=False,
)


class BehaviorTypeDef(_RequiredBehaviorTypeDef, _OptionalBehaviorTypeDef):
    pass


BillingGroupMetadataTypeDef = TypedDict(
    "BillingGroupMetadataTypeDef",
    {
        "creationDate": datetime,
    },
    total=False,
)

BillingGroupPropertiesTypeDef = TypedDict(
    "BillingGroupPropertiesTypeDef",
    {
        "billingGroupDescription": str,
    },
    total=False,
)

CACertificateDescriptionTypeDef = TypedDict(
    "CACertificateDescriptionTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "status": CACertificateStatusType,
        "certificatePem": str,
        "ownedBy": str,
        "creationDate": datetime,
        "autoRegistrationStatus": AutoRegistrationStatusType,
        "lastModifiedDate": datetime,
        "customerVersion": int,
        "generationId": str,
        "validity": "CertificateValidityTypeDef",
    },
    total=False,
)

CACertificateTypeDef = TypedDict(
    "CACertificateTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "status": CACertificateStatusType,
        "creationDate": datetime,
    },
    total=False,
)

CancelJobResponseTypeDef = TypedDict(
    "CancelJobResponseTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "description": str,
    },
    total=False,
)

CertificateDescriptionTypeDef = TypedDict(
    "CertificateDescriptionTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "caCertificateId": str,
        "status": CertificateStatusType,
        "certificatePem": str,
        "ownedBy": str,
        "previousOwnedBy": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "customerVersion": int,
        "transferData": "TransferDataTypeDef",
        "generationId": str,
        "validity": "CertificateValidityTypeDef",
        "certificateMode": CertificateModeType,
    },
    total=False,
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "status": CertificateStatusType,
        "certificateMode": CertificateModeType,
        "creationDate": datetime,
    },
    total=False,
)

CertificateValidityTypeDef = TypedDict(
    "CertificateValidityTypeDef",
    {
        "notBefore": datetime,
        "notAfter": datetime,
    },
    total=False,
)

CloudwatchAlarmActionTypeDef = TypedDict(
    "CloudwatchAlarmActionTypeDef",
    {
        "roleArn": str,
        "alarmName": str,
        "stateReason": str,
        "stateValue": str,
    },
)

CloudwatchLogsActionTypeDef = TypedDict(
    "CloudwatchLogsActionTypeDef",
    {
        "roleArn": str,
        "logGroupName": str,
    },
)

_RequiredCloudwatchMetricActionTypeDef = TypedDict(
    "_RequiredCloudwatchMetricActionTypeDef",
    {
        "roleArn": str,
        "metricNamespace": str,
        "metricName": str,
        "metricValue": str,
        "metricUnit": str,
    },
)
_OptionalCloudwatchMetricActionTypeDef = TypedDict(
    "_OptionalCloudwatchMetricActionTypeDef",
    {
        "metricTimestamp": str,
    },
    total=False,
)


class CloudwatchMetricActionTypeDef(
    _RequiredCloudwatchMetricActionTypeDef, _OptionalCloudwatchMetricActionTypeDef
):
    pass


CodeSigningCertificateChainTypeDef = TypedDict(
    "CodeSigningCertificateChainTypeDef",
    {
        "certificateName": str,
        "inlineDocument": str,
    },
    total=False,
)

CodeSigningSignatureTypeDef = TypedDict(
    "CodeSigningSignatureTypeDef",
    {
        "inlineDocument": Union[bytes, IO[bytes]],
    },
    total=False,
)

CodeSigningTypeDef = TypedDict(
    "CodeSigningTypeDef",
    {
        "awsSignerJobId": str,
        "startSigningJobParameter": "StartSigningJobParameterTypeDef",
        "customCodeSigning": "CustomCodeSigningTypeDef",
    },
    total=False,
)

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "Enabled": bool,
    },
    total=False,
)

CreateAuthorizerResponseTypeDef = TypedDict(
    "CreateAuthorizerResponseTypeDef",
    {
        "authorizerName": str,
        "authorizerArn": str,
    },
    total=False,
)

CreateBillingGroupResponseTypeDef = TypedDict(
    "CreateBillingGroupResponseTypeDef",
    {
        "billingGroupName": str,
        "billingGroupArn": str,
        "billingGroupId": str,
    },
    total=False,
)

CreateCertificateFromCsrResponseTypeDef = TypedDict(
    "CreateCertificateFromCsrResponseTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "certificatePem": str,
    },
    total=False,
)

CreateCustomMetricResponseTypeDef = TypedDict(
    "CreateCustomMetricResponseTypeDef",
    {
        "metricName": str,
        "metricArn": str,
    },
    total=False,
)

CreateDimensionResponseTypeDef = TypedDict(
    "CreateDimensionResponseTypeDef",
    {
        "name": str,
        "arn": str,
    },
    total=False,
)

CreateDomainConfigurationResponseTypeDef = TypedDict(
    "CreateDomainConfigurationResponseTypeDef",
    {
        "domainConfigurationName": str,
        "domainConfigurationArn": str,
    },
    total=False,
)

CreateDynamicThingGroupResponseTypeDef = TypedDict(
    "CreateDynamicThingGroupResponseTypeDef",
    {
        "thingGroupName": str,
        "thingGroupArn": str,
        "thingGroupId": str,
        "indexName": str,
        "queryString": str,
        "queryVersion": str,
    },
    total=False,
)

CreateJobResponseTypeDef = TypedDict(
    "CreateJobResponseTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "description": str,
    },
    total=False,
)

CreateJobTemplateResponseTypeDef = TypedDict(
    "CreateJobTemplateResponseTypeDef",
    {
        "jobTemplateArn": str,
        "jobTemplateId": str,
    },
    total=False,
)

CreateKeysAndCertificateResponseTypeDef = TypedDict(
    "CreateKeysAndCertificateResponseTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "certificatePem": str,
        "keyPair": "KeyPairTypeDef",
    },
    total=False,
)

CreateMitigationActionResponseTypeDef = TypedDict(
    "CreateMitigationActionResponseTypeDef",
    {
        "actionArn": str,
        "actionId": str,
    },
    total=False,
)

CreateOTAUpdateResponseTypeDef = TypedDict(
    "CreateOTAUpdateResponseTypeDef",
    {
        "otaUpdateId": str,
        "awsIotJobId": str,
        "otaUpdateArn": str,
        "awsIotJobArn": str,
        "otaUpdateStatus": OTAUpdateStatusType,
    },
    total=False,
)

CreatePolicyResponseTypeDef = TypedDict(
    "CreatePolicyResponseTypeDef",
    {
        "policyName": str,
        "policyArn": str,
        "policyDocument": str,
        "policyVersionId": str,
    },
    total=False,
)

CreatePolicyVersionResponseTypeDef = TypedDict(
    "CreatePolicyVersionResponseTypeDef",
    {
        "policyArn": str,
        "policyDocument": str,
        "policyVersionId": str,
        "isDefaultVersion": bool,
    },
    total=False,
)

CreateProvisioningClaimResponseTypeDef = TypedDict(
    "CreateProvisioningClaimResponseTypeDef",
    {
        "certificateId": str,
        "certificatePem": str,
        "keyPair": "KeyPairTypeDef",
        "expiration": datetime,
    },
    total=False,
)

CreateProvisioningTemplateResponseTypeDef = TypedDict(
    "CreateProvisioningTemplateResponseTypeDef",
    {
        "templateArn": str,
        "templateName": str,
        "defaultVersionId": int,
    },
    total=False,
)

CreateProvisioningTemplateVersionResponseTypeDef = TypedDict(
    "CreateProvisioningTemplateVersionResponseTypeDef",
    {
        "templateArn": str,
        "templateName": str,
        "versionId": int,
        "isDefaultVersion": bool,
    },
    total=False,
)

CreateRoleAliasResponseTypeDef = TypedDict(
    "CreateRoleAliasResponseTypeDef",
    {
        "roleAlias": str,
        "roleAliasArn": str,
    },
    total=False,
)

CreateScheduledAuditResponseTypeDef = TypedDict(
    "CreateScheduledAuditResponseTypeDef",
    {
        "scheduledAuditArn": str,
    },
    total=False,
)

CreateSecurityProfileResponseTypeDef = TypedDict(
    "CreateSecurityProfileResponseTypeDef",
    {
        "securityProfileName": str,
        "securityProfileArn": str,
    },
    total=False,
)

CreateStreamResponseTypeDef = TypedDict(
    "CreateStreamResponseTypeDef",
    {
        "streamId": str,
        "streamArn": str,
        "description": str,
        "streamVersion": int,
    },
    total=False,
)

CreateThingGroupResponseTypeDef = TypedDict(
    "CreateThingGroupResponseTypeDef",
    {
        "thingGroupName": str,
        "thingGroupArn": str,
        "thingGroupId": str,
    },
    total=False,
)

CreateThingResponseTypeDef = TypedDict(
    "CreateThingResponseTypeDef",
    {
        "thingName": str,
        "thingArn": str,
        "thingId": str,
    },
    total=False,
)

CreateThingTypeResponseTypeDef = TypedDict(
    "CreateThingTypeResponseTypeDef",
    {
        "thingTypeName": str,
        "thingTypeArn": str,
        "thingTypeId": str,
    },
    total=False,
)

CreateTopicRuleDestinationResponseTypeDef = TypedDict(
    "CreateTopicRuleDestinationResponseTypeDef",
    {
        "topicRuleDestination": "TopicRuleDestinationTypeDef",
    },
    total=False,
)

CustomCodeSigningTypeDef = TypedDict(
    "CustomCodeSigningTypeDef",
    {
        "signature": "CodeSigningSignatureTypeDef",
        "certificateChain": "CodeSigningCertificateChainTypeDef",
        "hashAlgorithm": str,
        "signatureAlgorithm": str,
    },
    total=False,
)

DeniedTypeDef = TypedDict(
    "DeniedTypeDef",
    {
        "implicitDeny": "ImplicitDenyTypeDef",
        "explicitDeny": "ExplicitDenyTypeDef",
    },
    total=False,
)

DescribeAccountAuditConfigurationResponseTypeDef = TypedDict(
    "DescribeAccountAuditConfigurationResponseTypeDef",
    {
        "roleArn": str,
        "auditNotificationTargetConfigurations": Dict[
            Literal["SNS"], "AuditNotificationTargetTypeDef"
        ],
        "auditCheckConfigurations": Dict[str, "AuditCheckConfigurationTypeDef"],
    },
    total=False,
)

DescribeAuditFindingResponseTypeDef = TypedDict(
    "DescribeAuditFindingResponseTypeDef",
    {
        "finding": "AuditFindingTypeDef",
    },
    total=False,
)

DescribeAuditMitigationActionsTaskResponseTypeDef = TypedDict(
    "DescribeAuditMitigationActionsTaskResponseTypeDef",
    {
        "taskStatus": AuditMitigationActionsTaskStatusType,
        "startTime": datetime,
        "endTime": datetime,
        "taskStatistics": Dict[str, "TaskStatisticsForAuditCheckTypeDef"],
        "target": "AuditMitigationActionsTaskTargetTypeDef",
        "auditCheckToActionsMapping": Dict[str, List[str]],
        "actionsDefinition": List["MitigationActionTypeDef"],
    },
    total=False,
)

DescribeAuditSuppressionResponseTypeDef = TypedDict(
    "DescribeAuditSuppressionResponseTypeDef",
    {
        "checkName": str,
        "resourceIdentifier": "ResourceIdentifierTypeDef",
        "expirationDate": datetime,
        "suppressIndefinitely": bool,
        "description": str,
    },
    total=False,
)

DescribeAuditTaskResponseTypeDef = TypedDict(
    "DescribeAuditTaskResponseTypeDef",
    {
        "taskStatus": AuditTaskStatusType,
        "taskType": AuditTaskTypeType,
        "taskStartTime": datetime,
        "taskStatistics": "TaskStatisticsTypeDef",
        "scheduledAuditName": str,
        "auditDetails": Dict[str, "AuditCheckDetailsTypeDef"],
    },
    total=False,
)

DescribeAuthorizerResponseTypeDef = TypedDict(
    "DescribeAuthorizerResponseTypeDef",
    {
        "authorizerDescription": "AuthorizerDescriptionTypeDef",
    },
    total=False,
)

DescribeBillingGroupResponseTypeDef = TypedDict(
    "DescribeBillingGroupResponseTypeDef",
    {
        "billingGroupName": str,
        "billingGroupId": str,
        "billingGroupArn": str,
        "version": int,
        "billingGroupProperties": "BillingGroupPropertiesTypeDef",
        "billingGroupMetadata": "BillingGroupMetadataTypeDef",
    },
    total=False,
)

DescribeCACertificateResponseTypeDef = TypedDict(
    "DescribeCACertificateResponseTypeDef",
    {
        "certificateDescription": "CACertificateDescriptionTypeDef",
        "registrationConfig": "RegistrationConfigTypeDef",
    },
    total=False,
)

DescribeCertificateResponseTypeDef = TypedDict(
    "DescribeCertificateResponseTypeDef",
    {
        "certificateDescription": "CertificateDescriptionTypeDef",
    },
    total=False,
)

DescribeCustomMetricResponseTypeDef = TypedDict(
    "DescribeCustomMetricResponseTypeDef",
    {
        "metricName": str,
        "metricArn": str,
        "metricType": CustomMetricTypeType,
        "displayName": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

DescribeDefaultAuthorizerResponseTypeDef = TypedDict(
    "DescribeDefaultAuthorizerResponseTypeDef",
    {
        "authorizerDescription": "AuthorizerDescriptionTypeDef",
    },
    total=False,
)

DescribeDetectMitigationActionsTaskResponseTypeDef = TypedDict(
    "DescribeDetectMitigationActionsTaskResponseTypeDef",
    {
        "taskSummary": "DetectMitigationActionsTaskSummaryTypeDef",
    },
    total=False,
)

DescribeDimensionResponseTypeDef = TypedDict(
    "DescribeDimensionResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "type": Literal["TOPIC_FILTER"],
        "stringValues": List[str],
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

DescribeDomainConfigurationResponseTypeDef = TypedDict(
    "DescribeDomainConfigurationResponseTypeDef",
    {
        "domainConfigurationName": str,
        "domainConfigurationArn": str,
        "domainName": str,
        "serverCertificates": List["ServerCertificateSummaryTypeDef"],
        "authorizerConfig": "AuthorizerConfigTypeDef",
        "domainConfigurationStatus": DomainConfigurationStatusType,
        "serviceType": ServiceTypeType,
        "domainType": DomainTypeType,
        "lastStatusChangeDate": datetime,
    },
    total=False,
)

DescribeEndpointResponseTypeDef = TypedDict(
    "DescribeEndpointResponseTypeDef",
    {
        "endpointAddress": str,
    },
    total=False,
)

DescribeEventConfigurationsResponseTypeDef = TypedDict(
    "DescribeEventConfigurationsResponseTypeDef",
    {
        "eventConfigurations": Dict[EventTypeType, "ConfigurationTypeDef"],
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

DescribeIndexResponseTypeDef = TypedDict(
    "DescribeIndexResponseTypeDef",
    {
        "indexName": str,
        "indexStatus": IndexStatusType,
        "schema": str,
    },
    total=False,
)

DescribeJobExecutionResponseTypeDef = TypedDict(
    "DescribeJobExecutionResponseTypeDef",
    {
        "execution": "JobExecutionTypeDef",
    },
    total=False,
)

DescribeJobResponseTypeDef = TypedDict(
    "DescribeJobResponseTypeDef",
    {
        "documentSource": str,
        "job": "JobTypeDef",
    },
    total=False,
)

DescribeJobTemplateResponseTypeDef = TypedDict(
    "DescribeJobTemplateResponseTypeDef",
    {
        "jobTemplateArn": str,
        "jobTemplateId": str,
        "description": str,
        "documentSource": str,
        "document": str,
        "createdAt": datetime,
        "presignedUrlConfig": "PresignedUrlConfigTypeDef",
        "jobExecutionsRolloutConfig": "JobExecutionsRolloutConfigTypeDef",
        "abortConfig": "AbortConfigTypeDef",
        "timeoutConfig": "TimeoutConfigTypeDef",
    },
    total=False,
)

DescribeMitigationActionResponseTypeDef = TypedDict(
    "DescribeMitigationActionResponseTypeDef",
    {
        "actionName": str,
        "actionType": MitigationActionTypeType,
        "actionArn": str,
        "actionId": str,
        "roleArn": str,
        "actionParams": "MitigationActionParamsTypeDef",
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

DescribeProvisioningTemplateResponseTypeDef = TypedDict(
    "DescribeProvisioningTemplateResponseTypeDef",
    {
        "templateArn": str,
        "templateName": str,
        "description": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "defaultVersionId": int,
        "templateBody": str,
        "enabled": bool,
        "provisioningRoleArn": str,
        "preProvisioningHook": "ProvisioningHookTypeDef",
    },
    total=False,
)

DescribeProvisioningTemplateVersionResponseTypeDef = TypedDict(
    "DescribeProvisioningTemplateVersionResponseTypeDef",
    {
        "versionId": int,
        "creationDate": datetime,
        "templateBody": str,
        "isDefaultVersion": bool,
    },
    total=False,
)

DescribeRoleAliasResponseTypeDef = TypedDict(
    "DescribeRoleAliasResponseTypeDef",
    {
        "roleAliasDescription": "RoleAliasDescriptionTypeDef",
    },
    total=False,
)

DescribeScheduledAuditResponseTypeDef = TypedDict(
    "DescribeScheduledAuditResponseTypeDef",
    {
        "frequency": AuditFrequencyType,
        "dayOfMonth": str,
        "dayOfWeek": DayOfWeekType,
        "targetCheckNames": List[str],
        "scheduledAuditName": str,
        "scheduledAuditArn": str,
    },
    total=False,
)

DescribeSecurityProfileResponseTypeDef = TypedDict(
    "DescribeSecurityProfileResponseTypeDef",
    {
        "securityProfileName": str,
        "securityProfileArn": str,
        "securityProfileDescription": str,
        "behaviors": List["BehaviorTypeDef"],
        "alertTargets": Dict[Literal["SNS"], "AlertTargetTypeDef"],
        "additionalMetricsToRetain": List[str],
        "additionalMetricsToRetainV2": List["MetricToRetainTypeDef"],
        "version": int,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

DescribeStreamResponseTypeDef = TypedDict(
    "DescribeStreamResponseTypeDef",
    {
        "streamInfo": "StreamInfoTypeDef",
    },
    total=False,
)

DescribeThingGroupResponseTypeDef = TypedDict(
    "DescribeThingGroupResponseTypeDef",
    {
        "thingGroupName": str,
        "thingGroupId": str,
        "thingGroupArn": str,
        "version": int,
        "thingGroupProperties": "ThingGroupPropertiesTypeDef",
        "thingGroupMetadata": "ThingGroupMetadataTypeDef",
        "indexName": str,
        "queryString": str,
        "queryVersion": str,
        "status": DynamicGroupStatusType,
    },
    total=False,
)

DescribeThingRegistrationTaskResponseTypeDef = TypedDict(
    "DescribeThingRegistrationTaskResponseTypeDef",
    {
        "taskId": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "templateBody": str,
        "inputFileBucket": str,
        "inputFileKey": str,
        "roleArn": str,
        "status": StatusType,
        "message": str,
        "successCount": int,
        "failureCount": int,
        "percentageProgress": int,
    },
    total=False,
)

DescribeThingResponseTypeDef = TypedDict(
    "DescribeThingResponseTypeDef",
    {
        "defaultClientId": str,
        "thingName": str,
        "thingId": str,
        "thingArn": str,
        "thingTypeName": str,
        "attributes": Dict[str, str],
        "version": int,
        "billingGroupName": str,
    },
    total=False,
)

DescribeThingTypeResponseTypeDef = TypedDict(
    "DescribeThingTypeResponseTypeDef",
    {
        "thingTypeName": str,
        "thingTypeId": str,
        "thingTypeArn": str,
        "thingTypeProperties": "ThingTypePropertiesTypeDef",
        "thingTypeMetadata": "ThingTypeMetadataTypeDef",
    },
    total=False,
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "s3Destination": "S3DestinationTypeDef",
    },
    total=False,
)

DetectMitigationActionExecutionTypeDef = TypedDict(
    "DetectMitigationActionExecutionTypeDef",
    {
        "taskId": str,
        "violationId": str,
        "actionName": str,
        "thingName": str,
        "executionStartDate": datetime,
        "executionEndDate": datetime,
        "status": DetectMitigationActionExecutionStatusType,
        "errorCode": str,
        "message": str,
    },
    total=False,
)

DetectMitigationActionsTaskStatisticsTypeDef = TypedDict(
    "DetectMitigationActionsTaskStatisticsTypeDef",
    {
        "actionsExecuted": int,
        "actionsSkipped": int,
        "actionsFailed": int,
    },
    total=False,
)

DetectMitigationActionsTaskSummaryTypeDef = TypedDict(
    "DetectMitigationActionsTaskSummaryTypeDef",
    {
        "taskId": str,
        "taskStatus": DetectMitigationActionsTaskStatusType,
        "taskStartTime": datetime,
        "taskEndTime": datetime,
        "target": "DetectMitigationActionsTaskTargetTypeDef",
        "violationEventOccurrenceRange": "ViolationEventOccurrenceRangeTypeDef",
        "onlyActiveViolationsIncluded": bool,
        "suppressedAlertsIncluded": bool,
        "actionsDefinition": List["MitigationActionTypeDef"],
        "taskStatistics": "DetectMitigationActionsTaskStatisticsTypeDef",
    },
    total=False,
)

DetectMitigationActionsTaskTargetTypeDef = TypedDict(
    "DetectMitigationActionsTaskTargetTypeDef",
    {
        "violationIds": List[str],
        "securityProfileName": str,
        "behaviorName": str,
    },
    total=False,
)

DomainConfigurationSummaryTypeDef = TypedDict(
    "DomainConfigurationSummaryTypeDef",
    {
        "domainConfigurationName": str,
        "domainConfigurationArn": str,
        "serviceType": ServiceTypeType,
    },
    total=False,
)

_RequiredDynamoDBActionTypeDef = TypedDict(
    "_RequiredDynamoDBActionTypeDef",
    {
        "tableName": str,
        "roleArn": str,
        "hashKeyField": str,
        "hashKeyValue": str,
    },
)
_OptionalDynamoDBActionTypeDef = TypedDict(
    "_OptionalDynamoDBActionTypeDef",
    {
        "operation": str,
        "hashKeyType": DynamoKeyTypeType,
        "rangeKeyField": str,
        "rangeKeyValue": str,
        "rangeKeyType": DynamoKeyTypeType,
        "payloadField": str,
    },
    total=False,
)


class DynamoDBActionTypeDef(_RequiredDynamoDBActionTypeDef, _OptionalDynamoDBActionTypeDef):
    pass


DynamoDBv2ActionTypeDef = TypedDict(
    "DynamoDBv2ActionTypeDef",
    {
        "roleArn": str,
        "putItem": "PutItemInputTypeDef",
    },
)

EffectivePolicyTypeDef = TypedDict(
    "EffectivePolicyTypeDef",
    {
        "policyName": str,
        "policyArn": str,
        "policyDocument": str,
    },
    total=False,
)

ElasticsearchActionTypeDef = TypedDict(
    "ElasticsearchActionTypeDef",
    {
        "roleArn": str,
        "endpoint": str,
        "index": str,
        "type": str,
        "id": str,
    },
)

EnableIoTLoggingParamsTypeDef = TypedDict(
    "EnableIoTLoggingParamsTypeDef",
    {
        "roleArnForLogging": str,
        "logLevel": LogLevelType,
    },
)

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "code": str,
        "message": str,
    },
    total=False,
)

ExplicitDenyTypeDef = TypedDict(
    "ExplicitDenyTypeDef",
    {
        "policies": List["PolicyTypeDef"],
    },
    total=False,
)

ExponentialRolloutRateTypeDef = TypedDict(
    "ExponentialRolloutRateTypeDef",
    {
        "baseRatePerMinute": int,
        "incrementFactor": float,
        "rateIncreaseCriteria": "RateIncreaseCriteriaTypeDef",
    },
)

FieldTypeDef = TypedDict(
    "FieldTypeDef",
    {
        "name": str,
        "type": FieldTypeType,
    },
    total=False,
)

FileLocationTypeDef = TypedDict(
    "FileLocationTypeDef",
    {
        "stream": "StreamTypeDef",
        "s3Location": "S3LocationTypeDef",
    },
    total=False,
)

_RequiredFirehoseActionTypeDef = TypedDict(
    "_RequiredFirehoseActionTypeDef",
    {
        "roleArn": str,
        "deliveryStreamName": str,
    },
)
_OptionalFirehoseActionTypeDef = TypedDict(
    "_OptionalFirehoseActionTypeDef",
    {
        "separator": str,
        "batchMode": bool,
    },
    total=False,
)


class FirehoseActionTypeDef(_RequiredFirehoseActionTypeDef, _OptionalFirehoseActionTypeDef):
    pass


GetBehaviorModelTrainingSummariesResponseTypeDef = TypedDict(
    "GetBehaviorModelTrainingSummariesResponseTypeDef",
    {
        "summaries": List["BehaviorModelTrainingSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

GetCardinalityResponseTypeDef = TypedDict(
    "GetCardinalityResponseTypeDef",
    {
        "cardinality": int,
    },
    total=False,
)

GetEffectivePoliciesResponseTypeDef = TypedDict(
    "GetEffectivePoliciesResponseTypeDef",
    {
        "effectivePolicies": List["EffectivePolicyTypeDef"],
    },
    total=False,
)

GetIndexingConfigurationResponseTypeDef = TypedDict(
    "GetIndexingConfigurationResponseTypeDef",
    {
        "thingIndexingConfiguration": "ThingIndexingConfigurationTypeDef",
        "thingGroupIndexingConfiguration": "ThingGroupIndexingConfigurationTypeDef",
    },
    total=False,
)

GetJobDocumentResponseTypeDef = TypedDict(
    "GetJobDocumentResponseTypeDef",
    {
        "document": str,
    },
    total=False,
)

GetLoggingOptionsResponseTypeDef = TypedDict(
    "GetLoggingOptionsResponseTypeDef",
    {
        "roleArn": str,
        "logLevel": LogLevelType,
    },
    total=False,
)

GetOTAUpdateResponseTypeDef = TypedDict(
    "GetOTAUpdateResponseTypeDef",
    {
        "otaUpdateInfo": "OTAUpdateInfoTypeDef",
    },
    total=False,
)

GetPercentilesResponseTypeDef = TypedDict(
    "GetPercentilesResponseTypeDef",
    {
        "percentiles": List["PercentPairTypeDef"],
    },
    total=False,
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef",
    {
        "policyName": str,
        "policyArn": str,
        "policyDocument": str,
        "defaultVersionId": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "generationId": str,
    },
    total=False,
)

GetPolicyVersionResponseTypeDef = TypedDict(
    "GetPolicyVersionResponseTypeDef",
    {
        "policyArn": str,
        "policyName": str,
        "policyDocument": str,
        "policyVersionId": str,
        "isDefaultVersion": bool,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "generationId": str,
    },
    total=False,
)

GetRegistrationCodeResponseTypeDef = TypedDict(
    "GetRegistrationCodeResponseTypeDef",
    {
        "registrationCode": str,
    },
    total=False,
)

GetStatisticsResponseTypeDef = TypedDict(
    "GetStatisticsResponseTypeDef",
    {
        "statistics": "StatisticsTypeDef",
    },
    total=False,
)

GetTopicRuleDestinationResponseTypeDef = TypedDict(
    "GetTopicRuleDestinationResponseTypeDef",
    {
        "topicRuleDestination": "TopicRuleDestinationTypeDef",
    },
    total=False,
)

GetTopicRuleResponseTypeDef = TypedDict(
    "GetTopicRuleResponseTypeDef",
    {
        "ruleArn": str,
        "rule": "TopicRuleTypeDef",
    },
    total=False,
)

GetV2LoggingOptionsResponseTypeDef = TypedDict(
    "GetV2LoggingOptionsResponseTypeDef",
    {
        "roleArn": str,
        "defaultLogLevel": LogLevelType,
        "disableAllLogs": bool,
    },
    total=False,
)

GroupNameAndArnTypeDef = TypedDict(
    "GroupNameAndArnTypeDef",
    {
        "groupName": str,
        "groupArn": str,
    },
    total=False,
)

HttpActionHeaderTypeDef = TypedDict(
    "HttpActionHeaderTypeDef",
    {
        "key": str,
        "value": str,
    },
)

_RequiredHttpActionTypeDef = TypedDict(
    "_RequiredHttpActionTypeDef",
    {
        "url": str,
    },
)
_OptionalHttpActionTypeDef = TypedDict(
    "_OptionalHttpActionTypeDef",
    {
        "confirmationUrl": str,
        "headers": List["HttpActionHeaderTypeDef"],
        "auth": "HttpAuthorizationTypeDef",
    },
    total=False,
)


class HttpActionTypeDef(_RequiredHttpActionTypeDef, _OptionalHttpActionTypeDef):
    pass


HttpAuthorizationTypeDef = TypedDict(
    "HttpAuthorizationTypeDef",
    {
        "sigv4": "SigV4AuthorizationTypeDef",
    },
    total=False,
)

HttpContextTypeDef = TypedDict(
    "HttpContextTypeDef",
    {
        "headers": Dict[str, str],
        "queryString": str,
    },
    total=False,
)

HttpUrlDestinationConfigurationTypeDef = TypedDict(
    "HttpUrlDestinationConfigurationTypeDef",
    {
        "confirmationUrl": str,
    },
)

HttpUrlDestinationPropertiesTypeDef = TypedDict(
    "HttpUrlDestinationPropertiesTypeDef",
    {
        "confirmationUrl": str,
    },
    total=False,
)

HttpUrlDestinationSummaryTypeDef = TypedDict(
    "HttpUrlDestinationSummaryTypeDef",
    {
        "confirmationUrl": str,
    },
    total=False,
)

ImplicitDenyTypeDef = TypedDict(
    "ImplicitDenyTypeDef",
    {
        "policies": List["PolicyTypeDef"],
    },
    total=False,
)

IotAnalyticsActionTypeDef = TypedDict(
    "IotAnalyticsActionTypeDef",
    {
        "channelArn": str,
        "channelName": str,
        "batchMode": bool,
        "roleArn": str,
    },
    total=False,
)

_RequiredIotEventsActionTypeDef = TypedDict(
    "_RequiredIotEventsActionTypeDef",
    {
        "inputName": str,
        "roleArn": str,
    },
)
_OptionalIotEventsActionTypeDef = TypedDict(
    "_OptionalIotEventsActionTypeDef",
    {
        "messageId": str,
        "batchMode": bool,
    },
    total=False,
)


class IotEventsActionTypeDef(_RequiredIotEventsActionTypeDef, _OptionalIotEventsActionTypeDef):
    pass


IotSiteWiseActionTypeDef = TypedDict(
    "IotSiteWiseActionTypeDef",
    {
        "putAssetPropertyValueEntries": List["PutAssetPropertyValueEntryTypeDef"],
        "roleArn": str,
    },
)

JobExecutionStatusDetailsTypeDef = TypedDict(
    "JobExecutionStatusDetailsTypeDef",
    {
        "detailsMap": Dict[str, str],
    },
    total=False,
)

JobExecutionSummaryForJobTypeDef = TypedDict(
    "JobExecutionSummaryForJobTypeDef",
    {
        "thingArn": str,
        "jobExecutionSummary": "JobExecutionSummaryTypeDef",
    },
    total=False,
)

JobExecutionSummaryForThingTypeDef = TypedDict(
    "JobExecutionSummaryForThingTypeDef",
    {
        "jobId": str,
        "jobExecutionSummary": "JobExecutionSummaryTypeDef",
    },
    total=False,
)

JobExecutionSummaryTypeDef = TypedDict(
    "JobExecutionSummaryTypeDef",
    {
        "status": JobExecutionStatusType,
        "queuedAt": datetime,
        "startedAt": datetime,
        "lastUpdatedAt": datetime,
        "executionNumber": int,
    },
    total=False,
)

JobExecutionTypeDef = TypedDict(
    "JobExecutionTypeDef",
    {
        "jobId": str,
        "status": JobExecutionStatusType,
        "forceCanceled": bool,
        "statusDetails": "JobExecutionStatusDetailsTypeDef",
        "thingArn": str,
        "queuedAt": datetime,
        "startedAt": datetime,
        "lastUpdatedAt": datetime,
        "executionNumber": int,
        "versionNumber": int,
        "approximateSecondsBeforeTimedOut": int,
    },
    total=False,
)

JobExecutionsRolloutConfigTypeDef = TypedDict(
    "JobExecutionsRolloutConfigTypeDef",
    {
        "maximumPerMinute": int,
        "exponentialRate": "ExponentialRolloutRateTypeDef",
    },
    total=False,
)

JobProcessDetailsTypeDef = TypedDict(
    "JobProcessDetailsTypeDef",
    {
        "processingTargets": List[str],
        "numberOfCanceledThings": int,
        "numberOfSucceededThings": int,
        "numberOfFailedThings": int,
        "numberOfRejectedThings": int,
        "numberOfQueuedThings": int,
        "numberOfInProgressThings": int,
        "numberOfRemovedThings": int,
        "numberOfTimedOutThings": int,
    },
    total=False,
)

JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "thingGroupId": str,
        "targetSelection": TargetSelectionType,
        "status": JobStatusType,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "completedAt": datetime,
    },
    total=False,
)

JobTemplateSummaryTypeDef = TypedDict(
    "JobTemplateSummaryTypeDef",
    {
        "jobTemplateArn": str,
        "jobTemplateId": str,
        "description": str,
        "createdAt": datetime,
    },
    total=False,
)

JobTypeDef = TypedDict(
    "JobTypeDef",
    {
        "jobArn": str,
        "jobId": str,
        "targetSelection": TargetSelectionType,
        "status": JobStatusType,
        "forceCanceled": bool,
        "reasonCode": str,
        "comment": str,
        "targets": List[str],
        "description": str,
        "presignedUrlConfig": "PresignedUrlConfigTypeDef",
        "jobExecutionsRolloutConfig": "JobExecutionsRolloutConfigTypeDef",
        "abortConfig": "AbortConfigTypeDef",
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "completedAt": datetime,
        "jobProcessDetails": "JobProcessDetailsTypeDef",
        "timeoutConfig": "TimeoutConfigTypeDef",
        "namespaceId": str,
        "jobTemplateArn": str,
    },
    total=False,
)

_RequiredKafkaActionTypeDef = TypedDict(
    "_RequiredKafkaActionTypeDef",
    {
        "destinationArn": str,
        "topic": str,
        "clientProperties": Dict[str, str],
    },
)
_OptionalKafkaActionTypeDef = TypedDict(
    "_OptionalKafkaActionTypeDef",
    {
        "key": str,
        "partition": str,
    },
    total=False,
)


class KafkaActionTypeDef(_RequiredKafkaActionTypeDef, _OptionalKafkaActionTypeDef):
    pass


KeyPairTypeDef = TypedDict(
    "KeyPairTypeDef",
    {
        "PublicKey": str,
        "PrivateKey": str,
    },
    total=False,
)

_RequiredKinesisActionTypeDef = TypedDict(
    "_RequiredKinesisActionTypeDef",
    {
        "roleArn": str,
        "streamName": str,
    },
)
_OptionalKinesisActionTypeDef = TypedDict(
    "_OptionalKinesisActionTypeDef",
    {
        "partitionKey": str,
    },
    total=False,
)


class KinesisActionTypeDef(_RequiredKinesisActionTypeDef, _OptionalKinesisActionTypeDef):
    pass


LambdaActionTypeDef = TypedDict(
    "LambdaActionTypeDef",
    {
        "functionArn": str,
    },
)

ListActiveViolationsResponseTypeDef = TypedDict(
    "ListActiveViolationsResponseTypeDef",
    {
        "activeViolations": List["ActiveViolationTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListAttachedPoliciesResponseTypeDef = TypedDict(
    "ListAttachedPoliciesResponseTypeDef",
    {
        "policies": List["PolicyTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListAuditFindingsResponseTypeDef = TypedDict(
    "ListAuditFindingsResponseTypeDef",
    {
        "findings": List["AuditFindingTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListAuditMitigationActionsExecutionsResponseTypeDef = TypedDict(
    "ListAuditMitigationActionsExecutionsResponseTypeDef",
    {
        "actionsExecutions": List["AuditMitigationActionExecutionMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListAuditMitigationActionsTasksResponseTypeDef = TypedDict(
    "ListAuditMitigationActionsTasksResponseTypeDef",
    {
        "tasks": List["AuditMitigationActionsTaskMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListAuditSuppressionsResponseTypeDef = TypedDict(
    "ListAuditSuppressionsResponseTypeDef",
    {
        "suppressions": List["AuditSuppressionTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListAuditTasksResponseTypeDef = TypedDict(
    "ListAuditTasksResponseTypeDef",
    {
        "tasks": List["AuditTaskMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListAuthorizersResponseTypeDef = TypedDict(
    "ListAuthorizersResponseTypeDef",
    {
        "authorizers": List["AuthorizerSummaryTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListBillingGroupsResponseTypeDef = TypedDict(
    "ListBillingGroupsResponseTypeDef",
    {
        "billingGroups": List["GroupNameAndArnTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListCACertificatesResponseTypeDef = TypedDict(
    "ListCACertificatesResponseTypeDef",
    {
        "certificates": List["CACertificateTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListCertificatesByCAResponseTypeDef = TypedDict(
    "ListCertificatesByCAResponseTypeDef",
    {
        "certificates": List["CertificateTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListCertificatesResponseTypeDef = TypedDict(
    "ListCertificatesResponseTypeDef",
    {
        "certificates": List["CertificateTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListCustomMetricsResponseTypeDef = TypedDict(
    "ListCustomMetricsResponseTypeDef",
    {
        "metricNames": List[str],
        "nextToken": str,
    },
    total=False,
)

ListDetectMitigationActionsExecutionsResponseTypeDef = TypedDict(
    "ListDetectMitigationActionsExecutionsResponseTypeDef",
    {
        "actionsExecutions": List["DetectMitigationActionExecutionTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListDetectMitigationActionsTasksResponseTypeDef = TypedDict(
    "ListDetectMitigationActionsTasksResponseTypeDef",
    {
        "tasks": List["DetectMitigationActionsTaskSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListDimensionsResponseTypeDef = TypedDict(
    "ListDimensionsResponseTypeDef",
    {
        "dimensionNames": List[str],
        "nextToken": str,
    },
    total=False,
)

ListDomainConfigurationsResponseTypeDef = TypedDict(
    "ListDomainConfigurationsResponseTypeDef",
    {
        "domainConfigurations": List["DomainConfigurationSummaryTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListIndicesResponseTypeDef = TypedDict(
    "ListIndicesResponseTypeDef",
    {
        "indexNames": List[str],
        "nextToken": str,
    },
    total=False,
)

ListJobExecutionsForJobResponseTypeDef = TypedDict(
    "ListJobExecutionsForJobResponseTypeDef",
    {
        "executionSummaries": List["JobExecutionSummaryForJobTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListJobExecutionsForThingResponseTypeDef = TypedDict(
    "ListJobExecutionsForThingResponseTypeDef",
    {
        "executionSummaries": List["JobExecutionSummaryForThingTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListJobTemplatesResponseTypeDef = TypedDict(
    "ListJobTemplatesResponseTypeDef",
    {
        "jobTemplates": List["JobTemplateSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListJobsResponseTypeDef = TypedDict(
    "ListJobsResponseTypeDef",
    {
        "jobs": List["JobSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListMitigationActionsResponseTypeDef = TypedDict(
    "ListMitigationActionsResponseTypeDef",
    {
        "actionIdentifiers": List["MitigationActionIdentifierTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListOTAUpdatesResponseTypeDef = TypedDict(
    "ListOTAUpdatesResponseTypeDef",
    {
        "otaUpdates": List["OTAUpdateSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListOutgoingCertificatesResponseTypeDef = TypedDict(
    "ListOutgoingCertificatesResponseTypeDef",
    {
        "outgoingCertificates": List["OutgoingCertificateTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListPoliciesResponseTypeDef = TypedDict(
    "ListPoliciesResponseTypeDef",
    {
        "policies": List["PolicyTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListPolicyPrincipalsResponseTypeDef = TypedDict(
    "ListPolicyPrincipalsResponseTypeDef",
    {
        "principals": List[str],
        "nextMarker": str,
    },
    total=False,
)

ListPolicyVersionsResponseTypeDef = TypedDict(
    "ListPolicyVersionsResponseTypeDef",
    {
        "policyVersions": List["PolicyVersionTypeDef"],
    },
    total=False,
)

ListPrincipalPoliciesResponseTypeDef = TypedDict(
    "ListPrincipalPoliciesResponseTypeDef",
    {
        "policies": List["PolicyTypeDef"],
        "nextMarker": str,
    },
    total=False,
)

ListPrincipalThingsResponseTypeDef = TypedDict(
    "ListPrincipalThingsResponseTypeDef",
    {
        "things": List[str],
        "nextToken": str,
    },
    total=False,
)

ListProvisioningTemplateVersionsResponseTypeDef = TypedDict(
    "ListProvisioningTemplateVersionsResponseTypeDef",
    {
        "versions": List["ProvisioningTemplateVersionSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListProvisioningTemplatesResponseTypeDef = TypedDict(
    "ListProvisioningTemplatesResponseTypeDef",
    {
        "templates": List["ProvisioningTemplateSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListRoleAliasesResponseTypeDef = TypedDict(
    "ListRoleAliasesResponseTypeDef",
    {
        "roleAliases": List[str],
        "nextMarker": str,
    },
    total=False,
)

ListScheduledAuditsResponseTypeDef = TypedDict(
    "ListScheduledAuditsResponseTypeDef",
    {
        "scheduledAudits": List["ScheduledAuditMetadataTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListSecurityProfilesForTargetResponseTypeDef = TypedDict(
    "ListSecurityProfilesForTargetResponseTypeDef",
    {
        "securityProfileTargetMappings": List["SecurityProfileTargetMappingTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListSecurityProfilesResponseTypeDef = TypedDict(
    "ListSecurityProfilesResponseTypeDef",
    {
        "securityProfileIdentifiers": List["SecurityProfileIdentifierTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListStreamsResponseTypeDef = TypedDict(
    "ListStreamsResponseTypeDef",
    {
        "streams": List["StreamSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List["TagTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListTargetsForPolicyResponseTypeDef = TypedDict(
    "ListTargetsForPolicyResponseTypeDef",
    {
        "targets": List[str],
        "nextMarker": str,
    },
    total=False,
)

ListTargetsForSecurityProfileResponseTypeDef = TypedDict(
    "ListTargetsForSecurityProfileResponseTypeDef",
    {
        "securityProfileTargets": List["SecurityProfileTargetTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListThingGroupsForThingResponseTypeDef = TypedDict(
    "ListThingGroupsForThingResponseTypeDef",
    {
        "thingGroups": List["GroupNameAndArnTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListThingGroupsResponseTypeDef = TypedDict(
    "ListThingGroupsResponseTypeDef",
    {
        "thingGroups": List["GroupNameAndArnTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListThingPrincipalsResponseTypeDef = TypedDict(
    "ListThingPrincipalsResponseTypeDef",
    {
        "principals": List[str],
        "nextToken": str,
    },
    total=False,
)

ListThingRegistrationTaskReportsResponseTypeDef = TypedDict(
    "ListThingRegistrationTaskReportsResponseTypeDef",
    {
        "resourceLinks": List[str],
        "reportType": ReportTypeType,
        "nextToken": str,
    },
    total=False,
)

ListThingRegistrationTasksResponseTypeDef = TypedDict(
    "ListThingRegistrationTasksResponseTypeDef",
    {
        "taskIds": List[str],
        "nextToken": str,
    },
    total=False,
)

ListThingTypesResponseTypeDef = TypedDict(
    "ListThingTypesResponseTypeDef",
    {
        "thingTypes": List["ThingTypeDefinitionTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListThingsInBillingGroupResponseTypeDef = TypedDict(
    "ListThingsInBillingGroupResponseTypeDef",
    {
        "things": List[str],
        "nextToken": str,
    },
    total=False,
)

ListThingsInThingGroupResponseTypeDef = TypedDict(
    "ListThingsInThingGroupResponseTypeDef",
    {
        "things": List[str],
        "nextToken": str,
    },
    total=False,
)

ListThingsResponseTypeDef = TypedDict(
    "ListThingsResponseTypeDef",
    {
        "things": List["ThingAttributeTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListTopicRuleDestinationsResponseTypeDef = TypedDict(
    "ListTopicRuleDestinationsResponseTypeDef",
    {
        "destinationSummaries": List["TopicRuleDestinationSummaryTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListTopicRulesResponseTypeDef = TypedDict(
    "ListTopicRulesResponseTypeDef",
    {
        "rules": List["TopicRuleListItemTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListV2LoggingLevelsResponseTypeDef = TypedDict(
    "ListV2LoggingLevelsResponseTypeDef",
    {
        "logTargetConfigurations": List["LogTargetConfigurationTypeDef"],
        "nextToken": str,
    },
    total=False,
)

ListViolationEventsResponseTypeDef = TypedDict(
    "ListViolationEventsResponseTypeDef",
    {
        "violationEvents": List["ViolationEventTypeDef"],
        "nextToken": str,
    },
    total=False,
)

LogTargetConfigurationTypeDef = TypedDict(
    "LogTargetConfigurationTypeDef",
    {
        "logTarget": "LogTargetTypeDef",
        "logLevel": LogLevelType,
    },
    total=False,
)

_RequiredLogTargetTypeDef = TypedDict(
    "_RequiredLogTargetTypeDef",
    {
        "targetType": LogTargetTypeType,
    },
)
_OptionalLogTargetTypeDef = TypedDict(
    "_OptionalLogTargetTypeDef",
    {
        "targetName": str,
    },
    total=False,
)


class LogTargetTypeDef(_RequiredLogTargetTypeDef, _OptionalLogTargetTypeDef):
    pass


_RequiredLoggingOptionsPayloadTypeDef = TypedDict(
    "_RequiredLoggingOptionsPayloadTypeDef",
    {
        "roleArn": str,
    },
)
_OptionalLoggingOptionsPayloadTypeDef = TypedDict(
    "_OptionalLoggingOptionsPayloadTypeDef",
    {
        "logLevel": LogLevelType,
    },
    total=False,
)


class LoggingOptionsPayloadTypeDef(
    _RequiredLoggingOptionsPayloadTypeDef, _OptionalLoggingOptionsPayloadTypeDef
):
    pass


MachineLearningDetectionConfigTypeDef = TypedDict(
    "MachineLearningDetectionConfigTypeDef",
    {
        "confidenceLevel": ConfidenceLevelType,
    },
)

_RequiredMetricDimensionTypeDef = TypedDict(
    "_RequiredMetricDimensionTypeDef",
    {
        "dimensionName": str,
    },
)
_OptionalMetricDimensionTypeDef = TypedDict(
    "_OptionalMetricDimensionTypeDef",
    {
        "operator": DimensionValueOperatorType,
    },
    total=False,
)


class MetricDimensionTypeDef(_RequiredMetricDimensionTypeDef, _OptionalMetricDimensionTypeDef):
    pass


_RequiredMetricToRetainTypeDef = TypedDict(
    "_RequiredMetricToRetainTypeDef",
    {
        "metric": str,
    },
)
_OptionalMetricToRetainTypeDef = TypedDict(
    "_OptionalMetricToRetainTypeDef",
    {
        "metricDimension": "MetricDimensionTypeDef",
    },
    total=False,
)


class MetricToRetainTypeDef(_RequiredMetricToRetainTypeDef, _OptionalMetricToRetainTypeDef):
    pass


MetricValueTypeDef = TypedDict(
    "MetricValueTypeDef",
    {
        "count": int,
        "cidrs": List[str],
        "ports": List[int],
        "number": float,
        "numbers": List[float],
        "strings": List[str],
    },
    total=False,
)

MitigationActionIdentifierTypeDef = TypedDict(
    "MitigationActionIdentifierTypeDef",
    {
        "actionName": str,
        "actionArn": str,
        "creationDate": datetime,
    },
    total=False,
)

MitigationActionParamsTypeDef = TypedDict(
    "MitigationActionParamsTypeDef",
    {
        "updateDeviceCertificateParams": "UpdateDeviceCertificateParamsTypeDef",
        "updateCACertificateParams": "UpdateCACertificateParamsTypeDef",
        "addThingsToThingGroupParams": "AddThingsToThingGroupParamsTypeDef",
        "replaceDefaultPolicyVersionParams": "ReplaceDefaultPolicyVersionParamsTypeDef",
        "enableIoTLoggingParams": "EnableIoTLoggingParamsTypeDef",
        "publishFindingToSnsParams": "PublishFindingToSnsParamsTypeDef",
    },
    total=False,
)

MitigationActionTypeDef = TypedDict(
    "MitigationActionTypeDef",
    {
        "name": str,
        "id": str,
        "roleArn": str,
        "actionParams": "MitigationActionParamsTypeDef",
    },
    total=False,
)

MqttContextTypeDef = TypedDict(
    "MqttContextTypeDef",
    {
        "username": str,
        "password": Union[bytes, IO[bytes]],
        "clientId": str,
    },
    total=False,
)

NonCompliantResourceTypeDef = TypedDict(
    "NonCompliantResourceTypeDef",
    {
        "resourceType": ResourceTypeType,
        "resourceIdentifier": "ResourceIdentifierTypeDef",
        "additionalInfo": Dict[str, str],
    },
    total=False,
)

OTAUpdateFileTypeDef = TypedDict(
    "OTAUpdateFileTypeDef",
    {
        "fileName": str,
        "fileType": int,
        "fileVersion": str,
        "fileLocation": "FileLocationTypeDef",
        "codeSigning": "CodeSigningTypeDef",
        "attributes": Dict[str, str],
    },
    total=False,
)

OTAUpdateInfoTypeDef = TypedDict(
    "OTAUpdateInfoTypeDef",
    {
        "otaUpdateId": str,
        "otaUpdateArn": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "description": str,
        "targets": List[str],
        "protocols": List[ProtocolType],
        "awsJobExecutionsRolloutConfig": "AwsJobExecutionsRolloutConfigTypeDef",
        "awsJobPresignedUrlConfig": "AwsJobPresignedUrlConfigTypeDef",
        "targetSelection": TargetSelectionType,
        "otaUpdateFiles": List["OTAUpdateFileTypeDef"],
        "otaUpdateStatus": OTAUpdateStatusType,
        "awsIotJobId": str,
        "awsIotJobArn": str,
        "errorInfo": "ErrorInfoTypeDef",
        "additionalParameters": Dict[str, str],
    },
    total=False,
)

OTAUpdateSummaryTypeDef = TypedDict(
    "OTAUpdateSummaryTypeDef",
    {
        "otaUpdateId": str,
        "otaUpdateArn": str,
        "creationDate": datetime,
    },
    total=False,
)

OutgoingCertificateTypeDef = TypedDict(
    "OutgoingCertificateTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
        "transferredTo": str,
        "transferDate": datetime,
        "transferMessage": str,
        "creationDate": datetime,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PercentPairTypeDef = TypedDict(
    "PercentPairTypeDef",
    {
        "percent": float,
        "value": float,
    },
    total=False,
)

PolicyTypeDef = TypedDict(
    "PolicyTypeDef",
    {
        "policyName": str,
        "policyArn": str,
    },
    total=False,
)

PolicyVersionIdentifierTypeDef = TypedDict(
    "PolicyVersionIdentifierTypeDef",
    {
        "policyName": str,
        "policyVersionId": str,
    },
    total=False,
)

PolicyVersionTypeDef = TypedDict(
    "PolicyVersionTypeDef",
    {
        "versionId": str,
        "isDefaultVersion": bool,
        "createDate": datetime,
    },
    total=False,
)

PresignedUrlConfigTypeDef = TypedDict(
    "PresignedUrlConfigTypeDef",
    {
        "roleArn": str,
        "expiresInSec": int,
    },
    total=False,
)

_RequiredProvisioningHookTypeDef = TypedDict(
    "_RequiredProvisioningHookTypeDef",
    {
        "targetArn": str,
    },
)
_OptionalProvisioningHookTypeDef = TypedDict(
    "_OptionalProvisioningHookTypeDef",
    {
        "payloadVersion": str,
    },
    total=False,
)


class ProvisioningHookTypeDef(_RequiredProvisioningHookTypeDef, _OptionalProvisioningHookTypeDef):
    pass


ProvisioningTemplateSummaryTypeDef = TypedDict(
    "ProvisioningTemplateSummaryTypeDef",
    {
        "templateArn": str,
        "templateName": str,
        "description": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
        "enabled": bool,
    },
    total=False,
)

ProvisioningTemplateVersionSummaryTypeDef = TypedDict(
    "ProvisioningTemplateVersionSummaryTypeDef",
    {
        "versionId": int,
        "creationDate": datetime,
        "isDefaultVersion": bool,
    },
    total=False,
)

PublishFindingToSnsParamsTypeDef = TypedDict(
    "PublishFindingToSnsParamsTypeDef",
    {
        "topicArn": str,
    },
)

_RequiredPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_RequiredPutAssetPropertyValueEntryTypeDef",
    {
        "propertyValues": List["AssetPropertyValueTypeDef"],
    },
)
_OptionalPutAssetPropertyValueEntryTypeDef = TypedDict(
    "_OptionalPutAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
        "assetId": str,
        "propertyId": str,
        "propertyAlias": str,
    },
    total=False,
)


class PutAssetPropertyValueEntryTypeDef(
    _RequiredPutAssetPropertyValueEntryTypeDef, _OptionalPutAssetPropertyValueEntryTypeDef
):
    pass


PutItemInputTypeDef = TypedDict(
    "PutItemInputTypeDef",
    {
        "tableName": str,
    },
)

RateIncreaseCriteriaTypeDef = TypedDict(
    "RateIncreaseCriteriaTypeDef",
    {
        "numberOfNotifiedThings": int,
        "numberOfSucceededThings": int,
    },
    total=False,
)

RegisterCACertificateResponseTypeDef = TypedDict(
    "RegisterCACertificateResponseTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
    },
    total=False,
)

RegisterCertificateResponseTypeDef = TypedDict(
    "RegisterCertificateResponseTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
    },
    total=False,
)

RegisterCertificateWithoutCAResponseTypeDef = TypedDict(
    "RegisterCertificateWithoutCAResponseTypeDef",
    {
        "certificateArn": str,
        "certificateId": str,
    },
    total=False,
)

RegisterThingResponseTypeDef = TypedDict(
    "RegisterThingResponseTypeDef",
    {
        "certificatePem": str,
        "resourceArns": Dict[str, str],
    },
    total=False,
)

RegistrationConfigTypeDef = TypedDict(
    "RegistrationConfigTypeDef",
    {
        "templateBody": str,
        "roleArn": str,
    },
    total=False,
)

RelatedResourceTypeDef = TypedDict(
    "RelatedResourceTypeDef",
    {
        "resourceType": ResourceTypeType,
        "resourceIdentifier": "ResourceIdentifierTypeDef",
        "additionalInfo": Dict[str, str],
    },
    total=False,
)

ReplaceDefaultPolicyVersionParamsTypeDef = TypedDict(
    "ReplaceDefaultPolicyVersionParamsTypeDef",
    {
        "templateName": Literal["BLANK_POLICY"],
    },
)

_RequiredRepublishActionTypeDef = TypedDict(
    "_RequiredRepublishActionTypeDef",
    {
        "roleArn": str,
        "topic": str,
    },
)
_OptionalRepublishActionTypeDef = TypedDict(
    "_OptionalRepublishActionTypeDef",
    {
        "qos": int,
    },
    total=False,
)


class RepublishActionTypeDef(_RequiredRepublishActionTypeDef, _OptionalRepublishActionTypeDef):
    pass


ResourceIdentifierTypeDef = TypedDict(
    "ResourceIdentifierTypeDef",
    {
        "deviceCertificateId": str,
        "caCertificateId": str,
        "cognitoIdentityPoolId": str,
        "clientId": str,
        "policyVersionIdentifier": "PolicyVersionIdentifierTypeDef",
        "account": str,
        "iamRoleArn": str,
        "roleAliasArn": str,
    },
    total=False,
)

RoleAliasDescriptionTypeDef = TypedDict(
    "RoleAliasDescriptionTypeDef",
    {
        "roleAlias": str,
        "roleAliasArn": str,
        "roleArn": str,
        "owner": str,
        "credentialDurationSeconds": int,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

_RequiredS3ActionTypeDef = TypedDict(
    "_RequiredS3ActionTypeDef",
    {
        "roleArn": str,
        "bucketName": str,
        "key": str,
    },
)
_OptionalS3ActionTypeDef = TypedDict(
    "_OptionalS3ActionTypeDef",
    {
        "cannedAcl": CannedAccessControlListType,
    },
    total=False,
)


class S3ActionTypeDef(_RequiredS3ActionTypeDef, _OptionalS3ActionTypeDef):
    pass


S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef",
    {
        "bucket": str,
        "prefix": str,
    },
    total=False,
)

S3LocationTypeDef = TypedDict(
    "S3LocationTypeDef",
    {
        "bucket": str,
        "key": str,
        "version": str,
    },
    total=False,
)

SalesforceActionTypeDef = TypedDict(
    "SalesforceActionTypeDef",
    {
        "token": str,
        "url": str,
    },
)

ScheduledAuditMetadataTypeDef = TypedDict(
    "ScheduledAuditMetadataTypeDef",
    {
        "scheduledAuditName": str,
        "scheduledAuditArn": str,
        "frequency": AuditFrequencyType,
        "dayOfMonth": str,
        "dayOfWeek": DayOfWeekType,
    },
    total=False,
)

SearchIndexResponseTypeDef = TypedDict(
    "SearchIndexResponseTypeDef",
    {
        "nextToken": str,
        "things": List["ThingDocumentTypeDef"],
        "thingGroups": List["ThingGroupDocumentTypeDef"],
    },
    total=False,
)

SecurityProfileIdentifierTypeDef = TypedDict(
    "SecurityProfileIdentifierTypeDef",
    {
        "name": str,
        "arn": str,
    },
)

SecurityProfileTargetMappingTypeDef = TypedDict(
    "SecurityProfileTargetMappingTypeDef",
    {
        "securityProfileIdentifier": "SecurityProfileIdentifierTypeDef",
        "target": "SecurityProfileTargetTypeDef",
    },
    total=False,
)

SecurityProfileTargetTypeDef = TypedDict(
    "SecurityProfileTargetTypeDef",
    {
        "arn": str,
    },
)

ServerCertificateSummaryTypeDef = TypedDict(
    "ServerCertificateSummaryTypeDef",
    {
        "serverCertificateArn": str,
        "serverCertificateStatus": ServerCertificateStatusType,
        "serverCertificateStatusDetail": str,
    },
    total=False,
)

SetDefaultAuthorizerResponseTypeDef = TypedDict(
    "SetDefaultAuthorizerResponseTypeDef",
    {
        "authorizerName": str,
        "authorizerArn": str,
    },
    total=False,
)

SigV4AuthorizationTypeDef = TypedDict(
    "SigV4AuthorizationTypeDef",
    {
        "signingRegion": str,
        "serviceName": str,
        "roleArn": str,
    },
)

SigningProfileParameterTypeDef = TypedDict(
    "SigningProfileParameterTypeDef",
    {
        "certificateArn": str,
        "platform": str,
        "certificatePathOnDevice": str,
    },
    total=False,
)

_RequiredSnsActionTypeDef = TypedDict(
    "_RequiredSnsActionTypeDef",
    {
        "targetArn": str,
        "roleArn": str,
    },
)
_OptionalSnsActionTypeDef = TypedDict(
    "_OptionalSnsActionTypeDef",
    {
        "messageFormat": MessageFormatType,
    },
    total=False,
)


class SnsActionTypeDef(_RequiredSnsActionTypeDef, _OptionalSnsActionTypeDef):
    pass


_RequiredSqsActionTypeDef = TypedDict(
    "_RequiredSqsActionTypeDef",
    {
        "roleArn": str,
        "queueUrl": str,
    },
)
_OptionalSqsActionTypeDef = TypedDict(
    "_OptionalSqsActionTypeDef",
    {
        "useBase64": bool,
    },
    total=False,
)


class SqsActionTypeDef(_RequiredSqsActionTypeDef, _OptionalSqsActionTypeDef):
    pass


StartAuditMitigationActionsTaskResponseTypeDef = TypedDict(
    "StartAuditMitigationActionsTaskResponseTypeDef",
    {
        "taskId": str,
    },
    total=False,
)

StartDetectMitigationActionsTaskResponseTypeDef = TypedDict(
    "StartDetectMitigationActionsTaskResponseTypeDef",
    {
        "taskId": str,
    },
    total=False,
)

StartOnDemandAuditTaskResponseTypeDef = TypedDict(
    "StartOnDemandAuditTaskResponseTypeDef",
    {
        "taskId": str,
    },
    total=False,
)

StartSigningJobParameterTypeDef = TypedDict(
    "StartSigningJobParameterTypeDef",
    {
        "signingProfileParameter": "SigningProfileParameterTypeDef",
        "signingProfileName": str,
        "destination": "DestinationTypeDef",
    },
    total=False,
)

StartThingRegistrationTaskResponseTypeDef = TypedDict(
    "StartThingRegistrationTaskResponseTypeDef",
    {
        "taskId": str,
    },
    total=False,
)

StatisticalThresholdTypeDef = TypedDict(
    "StatisticalThresholdTypeDef",
    {
        "statistic": str,
    },
    total=False,
)

StatisticsTypeDef = TypedDict(
    "StatisticsTypeDef",
    {
        "count": int,
        "average": float,
        "sum": float,
        "minimum": float,
        "maximum": float,
        "sumOfSquares": float,
        "variance": float,
        "stdDeviation": float,
    },
    total=False,
)

_RequiredStepFunctionsActionTypeDef = TypedDict(
    "_RequiredStepFunctionsActionTypeDef",
    {
        "stateMachineName": str,
        "roleArn": str,
    },
)
_OptionalStepFunctionsActionTypeDef = TypedDict(
    "_OptionalStepFunctionsActionTypeDef",
    {
        "executionNamePrefix": str,
    },
    total=False,
)


class StepFunctionsActionTypeDef(
    _RequiredStepFunctionsActionTypeDef, _OptionalStepFunctionsActionTypeDef
):
    pass


StreamFileTypeDef = TypedDict(
    "StreamFileTypeDef",
    {
        "fileId": int,
        "s3Location": "S3LocationTypeDef",
    },
    total=False,
)

StreamInfoTypeDef = TypedDict(
    "StreamInfoTypeDef",
    {
        "streamId": str,
        "streamArn": str,
        "streamVersion": int,
        "description": str,
        "files": List["StreamFileTypeDef"],
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "roleArn": str,
    },
    total=False,
)

StreamSummaryTypeDef = TypedDict(
    "StreamSummaryTypeDef",
    {
        "streamId": str,
        "streamArn": str,
        "streamVersion": int,
        "description": str,
    },
    total=False,
)

StreamTypeDef = TypedDict(
    "StreamTypeDef",
    {
        "streamId": str,
        "fileId": int,
    },
    total=False,
)

_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


TaskStatisticsForAuditCheckTypeDef = TypedDict(
    "TaskStatisticsForAuditCheckTypeDef",
    {
        "totalFindingsCount": int,
        "failedFindingsCount": int,
        "succeededFindingsCount": int,
        "skippedFindingsCount": int,
        "canceledFindingsCount": int,
    },
    total=False,
)

TaskStatisticsTypeDef = TypedDict(
    "TaskStatisticsTypeDef",
    {
        "totalChecks": int,
        "inProgressChecks": int,
        "waitingForDataCollectionChecks": int,
        "compliantChecks": int,
        "nonCompliantChecks": int,
        "failedChecks": int,
        "canceledChecks": int,
    },
    total=False,
)

TestAuthorizationResponseTypeDef = TypedDict(
    "TestAuthorizationResponseTypeDef",
    {
        "authResults": List["AuthResultTypeDef"],
    },
    total=False,
)

TestInvokeAuthorizerResponseTypeDef = TypedDict(
    "TestInvokeAuthorizerResponseTypeDef",
    {
        "isAuthenticated": bool,
        "principalId": str,
        "policyDocuments": List[str],
        "refreshAfterInSeconds": int,
        "disconnectAfterInSeconds": int,
    },
    total=False,
)

ThingAttributeTypeDef = TypedDict(
    "ThingAttributeTypeDef",
    {
        "thingName": str,
        "thingTypeName": str,
        "thingArn": str,
        "attributes": Dict[str, str],
        "version": int,
    },
    total=False,
)

ThingConnectivityTypeDef = TypedDict(
    "ThingConnectivityTypeDef",
    {
        "connected": bool,
        "timestamp": int,
    },
    total=False,
)

ThingDocumentTypeDef = TypedDict(
    "ThingDocumentTypeDef",
    {
        "thingName": str,
        "thingId": str,
        "thingTypeName": str,
        "thingGroupNames": List[str],
        "attributes": Dict[str, str],
        "shadow": str,
        "connectivity": "ThingConnectivityTypeDef",
    },
    total=False,
)

ThingGroupDocumentTypeDef = TypedDict(
    "ThingGroupDocumentTypeDef",
    {
        "thingGroupName": str,
        "thingGroupId": str,
        "thingGroupDescription": str,
        "attributes": Dict[str, str],
        "parentGroupNames": List[str],
    },
    total=False,
)

_RequiredThingGroupIndexingConfigurationTypeDef = TypedDict(
    "_RequiredThingGroupIndexingConfigurationTypeDef",
    {
        "thingGroupIndexingMode": ThingGroupIndexingModeType,
    },
)
_OptionalThingGroupIndexingConfigurationTypeDef = TypedDict(
    "_OptionalThingGroupIndexingConfigurationTypeDef",
    {
        "managedFields": List["FieldTypeDef"],
        "customFields": List["FieldTypeDef"],
    },
    total=False,
)


class ThingGroupIndexingConfigurationTypeDef(
    _RequiredThingGroupIndexingConfigurationTypeDef, _OptionalThingGroupIndexingConfigurationTypeDef
):
    pass


ThingGroupMetadataTypeDef = TypedDict(
    "ThingGroupMetadataTypeDef",
    {
        "parentGroupName": str,
        "rootToParentThingGroups": List["GroupNameAndArnTypeDef"],
        "creationDate": datetime,
    },
    total=False,
)

ThingGroupPropertiesTypeDef = TypedDict(
    "ThingGroupPropertiesTypeDef",
    {
        "thingGroupDescription": str,
        "attributePayload": "AttributePayloadTypeDef",
    },
    total=False,
)

_RequiredThingIndexingConfigurationTypeDef = TypedDict(
    "_RequiredThingIndexingConfigurationTypeDef",
    {
        "thingIndexingMode": ThingIndexingModeType,
    },
)
_OptionalThingIndexingConfigurationTypeDef = TypedDict(
    "_OptionalThingIndexingConfigurationTypeDef",
    {
        "thingConnectivityIndexingMode": ThingConnectivityIndexingModeType,
        "managedFields": List["FieldTypeDef"],
        "customFields": List["FieldTypeDef"],
    },
    total=False,
)


class ThingIndexingConfigurationTypeDef(
    _RequiredThingIndexingConfigurationTypeDef, _OptionalThingIndexingConfigurationTypeDef
):
    pass


ThingTypeDefinitionTypeDef = TypedDict(
    "ThingTypeDefinitionTypeDef",
    {
        "thingTypeName": str,
        "thingTypeArn": str,
        "thingTypeProperties": "ThingTypePropertiesTypeDef",
        "thingTypeMetadata": "ThingTypeMetadataTypeDef",
    },
    total=False,
)

ThingTypeMetadataTypeDef = TypedDict(
    "ThingTypeMetadataTypeDef",
    {
        "deprecated": bool,
        "deprecationDate": datetime,
        "creationDate": datetime,
    },
    total=False,
)

ThingTypePropertiesTypeDef = TypedDict(
    "ThingTypePropertiesTypeDef",
    {
        "thingTypeDescription": str,
        "searchableAttributes": List[str],
    },
    total=False,
)

TimeoutConfigTypeDef = TypedDict(
    "TimeoutConfigTypeDef",
    {
        "inProgressTimeoutInMinutes": int,
    },
    total=False,
)

_RequiredTimestreamActionTypeDef = TypedDict(
    "_RequiredTimestreamActionTypeDef",
    {
        "roleArn": str,
        "databaseName": str,
        "tableName": str,
        "dimensions": List["TimestreamDimensionTypeDef"],
    },
)
_OptionalTimestreamActionTypeDef = TypedDict(
    "_OptionalTimestreamActionTypeDef",
    {
        "timestamp": "TimestreamTimestampTypeDef",
    },
    total=False,
)


class TimestreamActionTypeDef(_RequiredTimestreamActionTypeDef, _OptionalTimestreamActionTypeDef):
    pass


TimestreamDimensionTypeDef = TypedDict(
    "TimestreamDimensionTypeDef",
    {
        "name": str,
        "value": str,
    },
)

TimestreamTimestampTypeDef = TypedDict(
    "TimestreamTimestampTypeDef",
    {
        "value": str,
        "unit": str,
    },
)

TlsContextTypeDef = TypedDict(
    "TlsContextTypeDef",
    {
        "serverName": str,
    },
    total=False,
)

TopicRuleDestinationConfigurationTypeDef = TypedDict(
    "TopicRuleDestinationConfigurationTypeDef",
    {
        "httpUrlConfiguration": "HttpUrlDestinationConfigurationTypeDef",
        "vpcConfiguration": "VpcDestinationConfigurationTypeDef",
    },
    total=False,
)

TopicRuleDestinationSummaryTypeDef = TypedDict(
    "TopicRuleDestinationSummaryTypeDef",
    {
        "arn": str,
        "status": TopicRuleDestinationStatusType,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "statusReason": str,
        "httpUrlSummary": "HttpUrlDestinationSummaryTypeDef",
        "vpcDestinationSummary": "VpcDestinationSummaryTypeDef",
    },
    total=False,
)

TopicRuleDestinationTypeDef = TypedDict(
    "TopicRuleDestinationTypeDef",
    {
        "arn": str,
        "status": TopicRuleDestinationStatusType,
        "createdAt": datetime,
        "lastUpdatedAt": datetime,
        "statusReason": str,
        "httpUrlProperties": "HttpUrlDestinationPropertiesTypeDef",
        "vpcProperties": "VpcDestinationPropertiesTypeDef",
    },
    total=False,
)

TopicRuleListItemTypeDef = TypedDict(
    "TopicRuleListItemTypeDef",
    {
        "ruleArn": str,
        "ruleName": str,
        "topicPattern": str,
        "createdAt": datetime,
        "ruleDisabled": bool,
    },
    total=False,
)

_RequiredTopicRulePayloadTypeDef = TypedDict(
    "_RequiredTopicRulePayloadTypeDef",
    {
        "sql": str,
        "actions": List["ActionTypeDef"],
    },
)
_OptionalTopicRulePayloadTypeDef = TypedDict(
    "_OptionalTopicRulePayloadTypeDef",
    {
        "description": str,
        "ruleDisabled": bool,
        "awsIotSqlVersion": str,
        "errorAction": "ActionTypeDef",
    },
    total=False,
)


class TopicRulePayloadTypeDef(_RequiredTopicRulePayloadTypeDef, _OptionalTopicRulePayloadTypeDef):
    pass


TopicRuleTypeDef = TypedDict(
    "TopicRuleTypeDef",
    {
        "ruleName": str,
        "sql": str,
        "description": str,
        "createdAt": datetime,
        "actions": List["ActionTypeDef"],
        "ruleDisabled": bool,
        "awsIotSqlVersion": str,
        "errorAction": "ActionTypeDef",
    },
    total=False,
)

TransferCertificateResponseTypeDef = TypedDict(
    "TransferCertificateResponseTypeDef",
    {
        "transferredCertificateArn": str,
    },
    total=False,
)

TransferDataTypeDef = TypedDict(
    "TransferDataTypeDef",
    {
        "transferMessage": str,
        "rejectReason": str,
        "transferDate": datetime,
        "acceptDate": datetime,
        "rejectDate": datetime,
    },
    total=False,
)

UpdateAuthorizerResponseTypeDef = TypedDict(
    "UpdateAuthorizerResponseTypeDef",
    {
        "authorizerName": str,
        "authorizerArn": str,
    },
    total=False,
)

UpdateBillingGroupResponseTypeDef = TypedDict(
    "UpdateBillingGroupResponseTypeDef",
    {
        "version": int,
    },
    total=False,
)

UpdateCACertificateParamsTypeDef = TypedDict(
    "UpdateCACertificateParamsTypeDef",
    {
        "action": Literal["DEACTIVATE"],
    },
)

UpdateCustomMetricResponseTypeDef = TypedDict(
    "UpdateCustomMetricResponseTypeDef",
    {
        "metricName": str,
        "metricArn": str,
        "metricType": CustomMetricTypeType,
        "displayName": str,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

UpdateDeviceCertificateParamsTypeDef = TypedDict(
    "UpdateDeviceCertificateParamsTypeDef",
    {
        "action": Literal["DEACTIVATE"],
    },
)

UpdateDimensionResponseTypeDef = TypedDict(
    "UpdateDimensionResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "type": Literal["TOPIC_FILTER"],
        "stringValues": List[str],
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

UpdateDomainConfigurationResponseTypeDef = TypedDict(
    "UpdateDomainConfigurationResponseTypeDef",
    {
        "domainConfigurationName": str,
        "domainConfigurationArn": str,
    },
    total=False,
)

UpdateDynamicThingGroupResponseTypeDef = TypedDict(
    "UpdateDynamicThingGroupResponseTypeDef",
    {
        "version": int,
    },
    total=False,
)

UpdateMitigationActionResponseTypeDef = TypedDict(
    "UpdateMitigationActionResponseTypeDef",
    {
        "actionArn": str,
        "actionId": str,
    },
    total=False,
)

UpdateRoleAliasResponseTypeDef = TypedDict(
    "UpdateRoleAliasResponseTypeDef",
    {
        "roleAlias": str,
        "roleAliasArn": str,
    },
    total=False,
)

UpdateScheduledAuditResponseTypeDef = TypedDict(
    "UpdateScheduledAuditResponseTypeDef",
    {
        "scheduledAuditArn": str,
    },
    total=False,
)

UpdateSecurityProfileResponseTypeDef = TypedDict(
    "UpdateSecurityProfileResponseTypeDef",
    {
        "securityProfileName": str,
        "securityProfileArn": str,
        "securityProfileDescription": str,
        "behaviors": List["BehaviorTypeDef"],
        "alertTargets": Dict[Literal["SNS"], "AlertTargetTypeDef"],
        "additionalMetricsToRetain": List[str],
        "additionalMetricsToRetainV2": List["MetricToRetainTypeDef"],
        "version": int,
        "creationDate": datetime,
        "lastModifiedDate": datetime,
    },
    total=False,
)

UpdateStreamResponseTypeDef = TypedDict(
    "UpdateStreamResponseTypeDef",
    {
        "streamId": str,
        "streamArn": str,
        "description": str,
        "streamVersion": int,
    },
    total=False,
)

UpdateThingGroupResponseTypeDef = TypedDict(
    "UpdateThingGroupResponseTypeDef",
    {
        "version": int,
    },
    total=False,
)

ValidateSecurityProfileBehaviorsResponseTypeDef = TypedDict(
    "ValidateSecurityProfileBehaviorsResponseTypeDef",
    {
        "valid": bool,
        "validationErrors": List["ValidationErrorTypeDef"],
    },
    total=False,
)

ValidationErrorTypeDef = TypedDict(
    "ValidationErrorTypeDef",
    {
        "errorMessage": str,
    },
    total=False,
)

ViolationEventAdditionalInfoTypeDef = TypedDict(
    "ViolationEventAdditionalInfoTypeDef",
    {
        "confidenceLevel": ConfidenceLevelType,
    },
    total=False,
)

ViolationEventOccurrenceRangeTypeDef = TypedDict(
    "ViolationEventOccurrenceRangeTypeDef",
    {
        "startTime": datetime,
        "endTime": datetime,
    },
)

ViolationEventTypeDef = TypedDict(
    "ViolationEventTypeDef",
    {
        "violationId": str,
        "thingName": str,
        "securityProfileName": str,
        "behavior": "BehaviorTypeDef",
        "metricValue": "MetricValueTypeDef",
        "violationEventAdditionalInfo": "ViolationEventAdditionalInfoTypeDef",
        "violationEventType": ViolationEventTypeType,
        "violationEventTime": datetime,
    },
    total=False,
)

_RequiredVpcDestinationConfigurationTypeDef = TypedDict(
    "_RequiredVpcDestinationConfigurationTypeDef",
    {
        "subnetIds": List[str],
        "vpcId": str,
        "roleArn": str,
    },
)
_OptionalVpcDestinationConfigurationTypeDef = TypedDict(
    "_OptionalVpcDestinationConfigurationTypeDef",
    {
        "securityGroups": List[str],
    },
    total=False,
)


class VpcDestinationConfigurationTypeDef(
    _RequiredVpcDestinationConfigurationTypeDef, _OptionalVpcDestinationConfigurationTypeDef
):
    pass


VpcDestinationPropertiesTypeDef = TypedDict(
    "VpcDestinationPropertiesTypeDef",
    {
        "subnetIds": List[str],
        "securityGroups": List[str],
        "vpcId": str,
        "roleArn": str,
    },
    total=False,
)

VpcDestinationSummaryTypeDef = TypedDict(
    "VpcDestinationSummaryTypeDef",
    {
        "subnetIds": List[str],
        "securityGroups": List[str],
        "vpcId": str,
        "roleArn": str,
    },
    total=False,
)
