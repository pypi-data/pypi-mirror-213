"""
Type annotations for codeguru-security service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codeguru_security.client import CodeGuruSecurityClient

    session = Session()
    client: CodeGuruSecurityClient = session.client("codeguru-security")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import AnalysisTypeType, ScanTypeType, StatusType
from .paginator import GetFindingsPaginator, ListFindingsMetricsPaginator, ListScansPaginator
from .type_defs import (
    BatchGetFindingsResponseTypeDef,
    CreateScanResponseTypeDef,
    CreateUploadUrlResponseTypeDef,
    EncryptionConfigTypeDef,
    FindingIdentifierTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetFindingsResponseTypeDef,
    GetMetricsSummaryResponseTypeDef,
    GetScanResponseTypeDef,
    ListFindingsMetricsResponseTypeDef,
    ListScansResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResourceIdTypeDef,
    UpdateAccountConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("CodeGuruSecurityClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeGuruSecurityClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruSecurityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#exceptions)
        """

    def batch_get_findings(
        self, *, findingIdentifiers: Sequence[FindingIdentifierTypeDef]
    ) -> BatchGetFindingsResponseTypeDef:
        """
        Returns a list of all requested findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.batch_get_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#batch_get_findings)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#close)
        """

    def create_scan(
        self,
        *,
        resourceId: ResourceIdTypeDef,
        scanName: str,
        analysisType: AnalysisTypeType = ...,
        clientToken: str = ...,
        scanType: ScanTypeType = ...,
        tags: Mapping[str, str] = ...
    ) -> CreateScanResponseTypeDef:
        """
        Use to create a scan using code uploaded to an S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.create_scan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#create_scan)
        """

    def create_upload_url(self, *, scanName: str) -> CreateUploadUrlResponseTypeDef:
        """
        Generates a pre-signed URL and request headers used to upload a code resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.create_upload_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#create_upload_url)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#generate_presigned_url)
        """

    def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        Use to get account level configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_account_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_account_configuration)
        """

    def get_findings(
        self,
        *,
        scanName: str,
        maxResults: int = ...,
        nextToken: str = ...,
        status: StatusType = ...
    ) -> GetFindingsResponseTypeDef:
        """
        Returns a list of all findings generated by a particular scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_findings)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_findings)
        """

    def get_metrics_summary(
        self, *, date: Union[datetime, str]
    ) -> GetMetricsSummaryResponseTypeDef:
        """
        Returns top level metrics about an account from a specified date, including
        number of open findings, the categories with most findings, the scans with most
        open findings, and scans with most open critical findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_metrics_summary)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_metrics_summary)
        """

    def get_scan(self, *, scanName: str, runId: str = ...) -> GetScanResponseTypeDef:
        """
        Returns details about a scan, including whether or not a scan has completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_scan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_scan)
        """

    def list_findings_metrics(
        self,
        *,
        endDate: Union[datetime, str],
        startDate: Union[datetime, str],
        maxResults: int = ...,
        nextToken: str = ...
    ) -> ListFindingsMetricsResponseTypeDef:
        """
        Returns metrics about all findings in an account within a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.list_findings_metrics)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#list_findings_metrics)
        """

    def list_scans(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListScansResponseTypeDef:
        """
        Returns a list of all the scans in an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.list_scans)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#list_scans)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags associated with a scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#list_tags_for_resource)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Use to add one or more tags to an existing scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Use to remove one or more tags from an existing scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#untag_resource)
        """

    def update_account_configuration(
        self, *, encryptionConfig: EncryptionConfigTypeDef
    ) -> UpdateAccountConfigurationResponseTypeDef:
        """
        Use to update account-level configuration with an encryption key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.update_account_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#update_account_configuration)
        """

    @overload
    def get_paginator(self, operation_name: Literal["get_findings"]) -> GetFindingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_findings_metrics"]
    ) -> ListFindingsMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_scans"]) -> ListScansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-security.html#CodeGuruSecurity.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codeguru_security/client/#get_paginator)
        """
