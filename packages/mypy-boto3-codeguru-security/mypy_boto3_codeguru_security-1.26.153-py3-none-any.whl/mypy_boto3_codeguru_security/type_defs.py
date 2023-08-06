"""
Type annotations for codeguru-security service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/type_defs/)

Usage::

    ```python
    from mypy_boto3_codeguru_security.type_defs import FindingMetricsValuePerSeverityTypeDef

    data: FindingMetricsValuePerSeverityTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    AnalysisTypeType,
    ErrorCodeType,
    ScanStateType,
    ScanTypeType,
    SeverityType,
    StatusType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "FindingMetricsValuePerSeverityTypeDef",
    "BatchGetFindingsErrorTypeDef",
    "FindingIdentifierTypeDef",
    "ResponseMetadataTypeDef",
    "CategoryWithFindingNumTypeDef",
    "CodeLineTypeDef",
    "ResourceIdTypeDef",
    "CreateUploadUrlRequestRequestTypeDef",
    "EncryptionConfigTypeDef",
    "ResourceTypeDef",
    "PaginatorConfigTypeDef",
    "GetFindingsRequestRequestTypeDef",
    "GetMetricsSummaryRequestRequestTypeDef",
    "GetScanRequestRequestTypeDef",
    "ListFindingsMetricsRequestRequestTypeDef",
    "ListScansRequestRequestTypeDef",
    "ScanSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ScanNameWithFindingNumTypeDef",
    "RecommendationTypeDef",
    "SuggestedFixTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AccountFindingsMetricTypeDef",
    "BatchGetFindingsRequestRequestTypeDef",
    "CreateUploadUrlResponseTypeDef",
    "GetScanResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "FilePathTypeDef",
    "CreateScanRequestRequestTypeDef",
    "CreateScanResponseTypeDef",
    "GetAccountConfigurationResponseTypeDef",
    "UpdateAccountConfigurationRequestRequestTypeDef",
    "UpdateAccountConfigurationResponseTypeDef",
    "GetFindingsRequestGetFindingsPaginateTypeDef",
    "ListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef",
    "ListScansRequestListScansPaginateTypeDef",
    "ListScansResponseTypeDef",
    "MetricsSummaryTypeDef",
    "RemediationTypeDef",
    "ListFindingsMetricsResponseTypeDef",
    "VulnerabilityTypeDef",
    "GetMetricsSummaryResponseTypeDef",
    "FindingTypeDef",
    "BatchGetFindingsResponseTypeDef",
    "GetFindingsResponseTypeDef",
)

FindingMetricsValuePerSeverityTypeDef = TypedDict(
    "FindingMetricsValuePerSeverityTypeDef",
    {
        "critical": float,
        "high": float,
        "info": float,
        "low": float,
        "medium": float,
    },
    total=False,
)

BatchGetFindingsErrorTypeDef = TypedDict(
    "BatchGetFindingsErrorTypeDef",
    {
        "errorCode": ErrorCodeType,
        "findingId": str,
        "message": str,
        "scanName": str,
    },
)

FindingIdentifierTypeDef = TypedDict(
    "FindingIdentifierTypeDef",
    {
        "findingId": str,
        "scanName": str,
    },
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

CategoryWithFindingNumTypeDef = TypedDict(
    "CategoryWithFindingNumTypeDef",
    {
        "categoryName": str,
        "findingNumber": int,
    },
    total=False,
)

CodeLineTypeDef = TypedDict(
    "CodeLineTypeDef",
    {
        "content": str,
        "number": int,
    },
    total=False,
)

ResourceIdTypeDef = TypedDict(
    "ResourceIdTypeDef",
    {
        "codeArtifactId": str,
    },
    total=False,
)

CreateUploadUrlRequestRequestTypeDef = TypedDict(
    "CreateUploadUrlRequestRequestTypeDef",
    {
        "scanName": str,
    },
)

EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "kmsKeyArn": str,
    },
    total=False,
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "id": str,
        "subResourceId": str,
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

_RequiredGetFindingsRequestRequestTypeDef = TypedDict(
    "_RequiredGetFindingsRequestRequestTypeDef",
    {
        "scanName": str,
    },
)
_OptionalGetFindingsRequestRequestTypeDef = TypedDict(
    "_OptionalGetFindingsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "status": StatusType,
    },
    total=False,
)


class GetFindingsRequestRequestTypeDef(
    _RequiredGetFindingsRequestRequestTypeDef, _OptionalGetFindingsRequestRequestTypeDef
):
    pass


GetMetricsSummaryRequestRequestTypeDef = TypedDict(
    "GetMetricsSummaryRequestRequestTypeDef",
    {
        "date": Union[datetime, str],
    },
)

_RequiredGetScanRequestRequestTypeDef = TypedDict(
    "_RequiredGetScanRequestRequestTypeDef",
    {
        "scanName": str,
    },
)
_OptionalGetScanRequestRequestTypeDef = TypedDict(
    "_OptionalGetScanRequestRequestTypeDef",
    {
        "runId": str,
    },
    total=False,
)


class GetScanRequestRequestTypeDef(
    _RequiredGetScanRequestRequestTypeDef, _OptionalGetScanRequestRequestTypeDef
):
    pass


_RequiredListFindingsMetricsRequestRequestTypeDef = TypedDict(
    "_RequiredListFindingsMetricsRequestRequestTypeDef",
    {
        "endDate": Union[datetime, str],
        "startDate": Union[datetime, str],
    },
)
_OptionalListFindingsMetricsRequestRequestTypeDef = TypedDict(
    "_OptionalListFindingsMetricsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListFindingsMetricsRequestRequestTypeDef(
    _RequiredListFindingsMetricsRequestRequestTypeDef,
    _OptionalListFindingsMetricsRequestRequestTypeDef,
):
    pass


ListScansRequestRequestTypeDef = TypedDict(
    "ListScansRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredScanSummaryTypeDef = TypedDict(
    "_RequiredScanSummaryTypeDef",
    {
        "createdAt": datetime,
        "runId": str,
        "scanName": str,
        "scanState": ScanStateType,
    },
)
_OptionalScanSummaryTypeDef = TypedDict(
    "_OptionalScanSummaryTypeDef",
    {
        "scanNameArn": str,
        "updatedAt": datetime,
    },
    total=False,
)


class ScanSummaryTypeDef(_RequiredScanSummaryTypeDef, _OptionalScanSummaryTypeDef):
    pass


ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ScanNameWithFindingNumTypeDef = TypedDict(
    "ScanNameWithFindingNumTypeDef",
    {
        "findingNumber": int,
        "scanName": str,
    },
    total=False,
)

RecommendationTypeDef = TypedDict(
    "RecommendationTypeDef",
    {
        "text": str,
        "url": str,
    },
    total=False,
)

SuggestedFixTypeDef = TypedDict(
    "SuggestedFixTypeDef",
    {
        "code": str,
        "description": str,
    },
    total=False,
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

AccountFindingsMetricTypeDef = TypedDict(
    "AccountFindingsMetricTypeDef",
    {
        "closedFindings": FindingMetricsValuePerSeverityTypeDef,
        "date": datetime,
        "meanTimeToClose": FindingMetricsValuePerSeverityTypeDef,
        "newFindings": FindingMetricsValuePerSeverityTypeDef,
        "openFindings": FindingMetricsValuePerSeverityTypeDef,
    },
    total=False,
)

BatchGetFindingsRequestRequestTypeDef = TypedDict(
    "BatchGetFindingsRequestRequestTypeDef",
    {
        "findingIdentifiers": Sequence[FindingIdentifierTypeDef],
    },
)

CreateUploadUrlResponseTypeDef = TypedDict(
    "CreateUploadUrlResponseTypeDef",
    {
        "codeArtifactId": str,
        "requestHeaders": Dict[str, str],
        "s3Url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetScanResponseTypeDef = TypedDict(
    "GetScanResponseTypeDef",
    {
        "analysisType": AnalysisTypeType,
        "createdAt": datetime,
        "numberOfRevisions": int,
        "runId": str,
        "scanName": str,
        "scanNameArn": str,
        "scanState": ScanStateType,
        "updatedAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FilePathTypeDef = TypedDict(
    "FilePathTypeDef",
    {
        "codeSnippet": List[CodeLineTypeDef],
        "endLine": int,
        "name": str,
        "path": str,
        "startLine": int,
    },
    total=False,
)

_RequiredCreateScanRequestRequestTypeDef = TypedDict(
    "_RequiredCreateScanRequestRequestTypeDef",
    {
        "resourceId": ResourceIdTypeDef,
        "scanName": str,
    },
)
_OptionalCreateScanRequestRequestTypeDef = TypedDict(
    "_OptionalCreateScanRequestRequestTypeDef",
    {
        "analysisType": AnalysisTypeType,
        "clientToken": str,
        "scanType": ScanTypeType,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateScanRequestRequestTypeDef(
    _RequiredCreateScanRequestRequestTypeDef, _OptionalCreateScanRequestRequestTypeDef
):
    pass


CreateScanResponseTypeDef = TypedDict(
    "CreateScanResponseTypeDef",
    {
        "resourceId": ResourceIdTypeDef,
        "runId": str,
        "scanName": str,
        "scanNameArn": str,
        "scanState": ScanStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountConfigurationResponseTypeDef = TypedDict(
    "GetAccountConfigurationResponseTypeDef",
    {
        "encryptionConfig": EncryptionConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateAccountConfigurationRequestRequestTypeDef",
    {
        "encryptionConfig": EncryptionConfigTypeDef,
    },
)

UpdateAccountConfigurationResponseTypeDef = TypedDict(
    "UpdateAccountConfigurationResponseTypeDef",
    {
        "encryptionConfig": EncryptionConfigTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredGetFindingsRequestGetFindingsPaginateTypeDef = TypedDict(
    "_RequiredGetFindingsRequestGetFindingsPaginateTypeDef",
    {
        "scanName": str,
    },
)
_OptionalGetFindingsRequestGetFindingsPaginateTypeDef = TypedDict(
    "_OptionalGetFindingsRequestGetFindingsPaginateTypeDef",
    {
        "status": StatusType,
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class GetFindingsRequestGetFindingsPaginateTypeDef(
    _RequiredGetFindingsRequestGetFindingsPaginateTypeDef,
    _OptionalGetFindingsRequestGetFindingsPaginateTypeDef,
):
    pass


_RequiredListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef = TypedDict(
    "_RequiredListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef",
    {
        "endDate": Union[datetime, str],
        "startDate": Union[datetime, str],
    },
)
_OptionalListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef = TypedDict(
    "_OptionalListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)


class ListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef(
    _RequiredListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef,
    _OptionalListFindingsMetricsRequestListFindingsMetricsPaginateTypeDef,
):
    pass


ListScansRequestListScansPaginateTypeDef = TypedDict(
    "ListScansRequestListScansPaginateTypeDef",
    {
        "PaginationConfig": PaginatorConfigTypeDef,
    },
    total=False,
)

ListScansResponseTypeDef = TypedDict(
    "ListScansResponseTypeDef",
    {
        "nextToken": str,
        "summaries": List[ScanSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricsSummaryTypeDef = TypedDict(
    "MetricsSummaryTypeDef",
    {
        "categoriesWithMostFindings": List[CategoryWithFindingNumTypeDef],
        "date": datetime,
        "openFindings": FindingMetricsValuePerSeverityTypeDef,
        "scansWithMostOpenCriticalFindings": List[ScanNameWithFindingNumTypeDef],
        "scansWithMostOpenFindings": List[ScanNameWithFindingNumTypeDef],
    },
    total=False,
)

RemediationTypeDef = TypedDict(
    "RemediationTypeDef",
    {
        "recommendation": RecommendationTypeDef,
        "suggestedFixes": List[SuggestedFixTypeDef],
    },
    total=False,
)

ListFindingsMetricsResponseTypeDef = TypedDict(
    "ListFindingsMetricsResponseTypeDef",
    {
        "findingsMetrics": List[AccountFindingsMetricTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VulnerabilityTypeDef = TypedDict(
    "VulnerabilityTypeDef",
    {
        "filePath": FilePathTypeDef,
        "id": str,
        "itemCount": int,
        "referenceUrls": List[str],
        "relatedVulnerabilities": List[str],
    },
    total=False,
)

GetMetricsSummaryResponseTypeDef = TypedDict(
    "GetMetricsSummaryResponseTypeDef",
    {
        "metricsSummary": MetricsSummaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FindingTypeDef = TypedDict(
    "FindingTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "detectorId": str,
        "detectorName": str,
        "detectorTags": List[str],
        "generatorId": str,
        "id": str,
        "remediation": RemediationTypeDef,
        "resource": ResourceTypeDef,
        "ruleId": str,
        "severity": SeverityType,
        "status": StatusType,
        "title": str,
        "type": str,
        "updatedAt": datetime,
        "vulnerability": VulnerabilityTypeDef,
    },
    total=False,
)

BatchGetFindingsResponseTypeDef = TypedDict(
    "BatchGetFindingsResponseTypeDef",
    {
        "failedFindings": List[BatchGetFindingsErrorTypeDef],
        "findings": List[FindingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetFindingsResponseTypeDef = TypedDict(
    "GetFindingsResponseTypeDef",
    {
        "findings": List[FindingTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
