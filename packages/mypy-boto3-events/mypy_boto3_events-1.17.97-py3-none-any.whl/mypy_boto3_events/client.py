"""
Type annotations for events service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_events import EventBridgeClient

    client: EventBridgeClient = boto3.client("events")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Type, overload

from botocore.client import ClientMeta

from .literals import (
    ApiDestinationHttpMethodType,
    ArchiveStateType,
    ConnectionAuthorizationTypeType,
    ConnectionStateType,
    ReplayStateType,
    RuleStateType,
)
from .paginator import (
    ListRuleNamesByTargetPaginator,
    ListRulesPaginator,
    ListTargetsByRulePaginator,
)
from .type_defs import (
    CancelReplayResponseTypeDef,
    ConditionTypeDef,
    CreateApiDestinationResponseTypeDef,
    CreateArchiveResponseTypeDef,
    CreateConnectionAuthRequestParametersTypeDef,
    CreateConnectionResponseTypeDef,
    CreateEventBusResponseTypeDef,
    CreatePartnerEventSourceResponseTypeDef,
    DeauthorizeConnectionResponseTypeDef,
    DeleteConnectionResponseTypeDef,
    DescribeApiDestinationResponseTypeDef,
    DescribeArchiveResponseTypeDef,
    DescribeConnectionResponseTypeDef,
    DescribeEventBusResponseTypeDef,
    DescribeEventSourceResponseTypeDef,
    DescribePartnerEventSourceResponseTypeDef,
    DescribeReplayResponseTypeDef,
    DescribeRuleResponseTypeDef,
    ListApiDestinationsResponseTypeDef,
    ListArchivesResponseTypeDef,
    ListConnectionsResponseTypeDef,
    ListEventBusesResponseTypeDef,
    ListEventSourcesResponseTypeDef,
    ListPartnerEventSourceAccountsResponseTypeDef,
    ListPartnerEventSourcesResponseTypeDef,
    ListReplaysResponseTypeDef,
    ListRuleNamesByTargetResponseTypeDef,
    ListRulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsByRuleResponseTypeDef,
    PutEventsRequestEntryTypeDef,
    PutEventsResponseTypeDef,
    PutPartnerEventsRequestEntryTypeDef,
    PutPartnerEventsResponseTypeDef,
    PutRuleResponseTypeDef,
    PutTargetsResponseTypeDef,
    RemoveTargetsResponseTypeDef,
    ReplayDestinationTypeDef,
    StartReplayResponseTypeDef,
    TagTypeDef,
    TargetTypeDef,
    TestEventPatternResponseTypeDef,
    UpdateApiDestinationResponseTypeDef,
    UpdateArchiveResponseTypeDef,
    UpdateConnectionAuthRequestParametersTypeDef,
    UpdateConnectionResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("EventBridgeClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    IllegalStatusException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidEventPatternException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ManagedRuleException: Type[BotocoreClientError]
    OperationDisabledException: Type[BotocoreClientError]
    PolicyLengthExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class EventBridgeClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def activate_event_source(self, *, Name: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.activate_event_source)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#activate_event_source)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#can_paginate)
        """

    def cancel_replay(self, *, ReplayName: str) -> CancelReplayResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.cancel_replay)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#cancel_replay)
        """

    def create_api_destination(
        self,
        *,
        Name: str,
        ConnectionArn: str,
        InvocationEndpoint: str,
        HttpMethod: ApiDestinationHttpMethodType,
        Description: str = None,
        InvocationRateLimitPerSecond: int = None
    ) -> CreateApiDestinationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.create_api_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#create_api_destination)
        """

    def create_archive(
        self,
        *,
        ArchiveName: str,
        EventSourceArn: str,
        Description: str = None,
        EventPattern: str = None,
        RetentionDays: int = None
    ) -> CreateArchiveResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.create_archive)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#create_archive)
        """

    def create_connection(
        self,
        *,
        Name: str,
        AuthorizationType: ConnectionAuthorizationTypeType,
        AuthParameters: CreateConnectionAuthRequestParametersTypeDef,
        Description: str = None
    ) -> CreateConnectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.create_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#create_connection)
        """

    def create_event_bus(
        self, *, Name: str, EventSourceName: str = None, Tags: List["TagTypeDef"] = None
    ) -> CreateEventBusResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.create_event_bus)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#create_event_bus)
        """

    def create_partner_event_source(
        self, *, Name: str, Account: str
    ) -> CreatePartnerEventSourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.create_partner_event_source)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#create_partner_event_source)
        """

    def deactivate_event_source(self, *, Name: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.deactivate_event_source)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#deactivate_event_source)
        """

    def deauthorize_connection(self, *, Name: str) -> DeauthorizeConnectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.deauthorize_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#deauthorize_connection)
        """

    def delete_api_destination(self, *, Name: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.delete_api_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#delete_api_destination)
        """

    def delete_archive(self, *, ArchiveName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.delete_archive)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#delete_archive)
        """

    def delete_connection(self, *, Name: str) -> DeleteConnectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.delete_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#delete_connection)
        """

    def delete_event_bus(self, *, Name: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.delete_event_bus)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#delete_event_bus)
        """

    def delete_partner_event_source(self, *, Name: str, Account: str) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.delete_partner_event_source)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#delete_partner_event_source)
        """

    def delete_rule(self, *, Name: str, EventBusName: str = None, Force: bool = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.delete_rule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#delete_rule)
        """

    def describe_api_destination(self, *, Name: str) -> DescribeApiDestinationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_api_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_api_destination)
        """

    def describe_archive(self, *, ArchiveName: str) -> DescribeArchiveResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_archive)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_archive)
        """

    def describe_connection(self, *, Name: str) -> DescribeConnectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_connection)
        """

    def describe_event_bus(self, *, Name: str = None) -> DescribeEventBusResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_event_bus)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_event_bus)
        """

    def describe_event_source(self, *, Name: str) -> DescribeEventSourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_event_source)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_event_source)
        """

    def describe_partner_event_source(
        self, *, Name: str
    ) -> DescribePartnerEventSourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_partner_event_source)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_partner_event_source)
        """

    def describe_replay(self, *, ReplayName: str) -> DescribeReplayResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_replay)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_replay)
        """

    def describe_rule(self, *, Name: str, EventBusName: str = None) -> DescribeRuleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.describe_rule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#describe_rule)
        """

    def disable_rule(self, *, Name: str, EventBusName: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.disable_rule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#disable_rule)
        """

    def enable_rule(self, *, Name: str, EventBusName: str = None) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.enable_rule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#enable_rule)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#generate_presigned_url)
        """

    def list_api_destinations(
        self,
        *,
        NamePrefix: str = None,
        ConnectionArn: str = None,
        NextToken: str = None,
        Limit: int = None
    ) -> ListApiDestinationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_api_destinations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_api_destinations)
        """

    def list_archives(
        self,
        *,
        NamePrefix: str = None,
        EventSourceArn: str = None,
        State: ArchiveStateType = None,
        NextToken: str = None,
        Limit: int = None
    ) -> ListArchivesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_archives)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_archives)
        """

    def list_connections(
        self,
        *,
        NamePrefix: str = None,
        ConnectionState: ConnectionStateType = None,
        NextToken: str = None,
        Limit: int = None
    ) -> ListConnectionsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_connections)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_connections)
        """

    def list_event_buses(
        self, *, NamePrefix: str = None, NextToken: str = None, Limit: int = None
    ) -> ListEventBusesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_event_buses)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_event_buses)
        """

    def list_event_sources(
        self, *, NamePrefix: str = None, NextToken: str = None, Limit: int = None
    ) -> ListEventSourcesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_event_sources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_event_sources)
        """

    def list_partner_event_source_accounts(
        self, *, EventSourceName: str, NextToken: str = None, Limit: int = None
    ) -> ListPartnerEventSourceAccountsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_partner_event_source_accounts)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_partner_event_source_accounts)
        """

    def list_partner_event_sources(
        self, *, NamePrefix: str, NextToken: str = None, Limit: int = None
    ) -> ListPartnerEventSourcesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_partner_event_sources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_partner_event_sources)
        """

    def list_replays(
        self,
        *,
        NamePrefix: str = None,
        State: ReplayStateType = None,
        EventSourceArn: str = None,
        NextToken: str = None,
        Limit: int = None
    ) -> ListReplaysResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_replays)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_replays)
        """

    def list_rule_names_by_target(
        self, *, TargetArn: str, EventBusName: str = None, NextToken: str = None, Limit: int = None
    ) -> ListRuleNamesByTargetResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_rule_names_by_target)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_rule_names_by_target)
        """

    def list_rules(
        self,
        *,
        NamePrefix: str = None,
        EventBusName: str = None,
        NextToken: str = None,
        Limit: int = None
    ) -> ListRulesResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_rules)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_rules)
        """

    def list_tags_for_resource(self, *, ResourceARN: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_tags_for_resource)
        """

    def list_targets_by_rule(
        self, *, Rule: str, EventBusName: str = None, NextToken: str = None, Limit: int = None
    ) -> ListTargetsByRuleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.list_targets_by_rule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#list_targets_by_rule)
        """

    def put_events(
        self, *, Entries: List[PutEventsRequestEntryTypeDef]
    ) -> PutEventsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.put_events)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#put_events)
        """

    def put_partner_events(
        self, *, Entries: List[PutPartnerEventsRequestEntryTypeDef]
    ) -> PutPartnerEventsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.put_partner_events)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#put_partner_events)
        """

    def put_permission(
        self,
        *,
        EventBusName: str = None,
        Action: str = None,
        Principal: str = None,
        StatementId: str = None,
        Condition: ConditionTypeDef = None,
        Policy: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.put_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#put_permission)
        """

    def put_rule(
        self,
        *,
        Name: str,
        ScheduleExpression: str = None,
        EventPattern: str = None,
        State: RuleStateType = None,
        Description: str = None,
        RoleArn: str = None,
        Tags: List["TagTypeDef"] = None,
        EventBusName: str = None
    ) -> PutRuleResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.put_rule)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#put_rule)
        """

    def put_targets(
        self, *, Rule: str, Targets: List["TargetTypeDef"], EventBusName: str = None
    ) -> PutTargetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.put_targets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#put_targets)
        """

    def remove_permission(
        self,
        *,
        StatementId: str = None,
        RemoveAllPermissions: bool = None,
        EventBusName: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.remove_permission)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#remove_permission)
        """

    def remove_targets(
        self, *, Rule: str, Ids: List[str], EventBusName: str = None, Force: bool = None
    ) -> RemoveTargetsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.remove_targets)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#remove_targets)
        """

    def start_replay(
        self,
        *,
        ReplayName: str,
        EventSourceArn: str,
        EventStartTime: datetime,
        EventEndTime: datetime,
        Destination: "ReplayDestinationTypeDef",
        Description: str = None
    ) -> StartReplayResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.start_replay)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#start_replay)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: List["TagTypeDef"]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.tag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#tag_resource)
        """

    def test_event_pattern(
        self, *, EventPattern: str, Event: str
    ) -> TestEventPatternResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.test_event_pattern)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#test_event_pattern)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: List[str]) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.untag_resource)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#untag_resource)
        """

    def update_api_destination(
        self,
        *,
        Name: str,
        Description: str = None,
        ConnectionArn: str = None,
        InvocationEndpoint: str = None,
        HttpMethod: ApiDestinationHttpMethodType = None,
        InvocationRateLimitPerSecond: int = None
    ) -> UpdateApiDestinationResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.update_api_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#update_api_destination)
        """

    def update_archive(
        self,
        *,
        ArchiveName: str,
        Description: str = None,
        EventPattern: str = None,
        RetentionDays: int = None
    ) -> UpdateArchiveResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.update_archive)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#update_archive)
        """

    def update_connection(
        self,
        *,
        Name: str,
        Description: str = None,
        AuthorizationType: ConnectionAuthorizationTypeType = None,
        AuthParameters: UpdateConnectionAuthRequestParametersTypeDef = None
    ) -> UpdateConnectionResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Client.update_connection)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/client.html#update_connection)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_rule_names_by_target"]
    ) -> ListRuleNamesByTargetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Paginator.ListRuleNamesByTarget)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/paginators.html#listrulenamesbytargetpaginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rules"]) -> ListRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Paginator.ListRules)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/paginators.html#listrulespaginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_targets_by_rule"]
    ) -> ListTargetsByRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/events.html#EventBridge.Paginator.ListTargetsByRule)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_events/paginators.html#listtargetsbyrulepaginator)
        """
