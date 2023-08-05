"""
Type annotations for dynamodb service ServiceResource

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_dynamodb import DynamoDBServiceResource
    import mypy_boto3_dynamodb.service_resource as dynamodb_resources

    resource: DynamoDBServiceResource = boto3.resource("dynamodb")

    my_table: dynamodb_resources.Table = resource.Table(...)
```
"""
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Iterator, List, Set, Union

from boto3.dynamodb.conditions import ConditionBase
from boto3.dynamodb.table import BatchWriter
from boto3.resources.base import ServiceResource as Boto3ServiceResource
from boto3.resources.collection import ResourceCollection

from .literals import (
    BillingModeType,
    ConditionalOperatorType,
    ReturnConsumedCapacityType,
    ReturnItemCollectionMetricsType,
    ReturnValueType,
    SelectType,
)
from .type_defs import (
    AttributeDefinitionTypeDef,
    AttributeValueUpdateTypeDef,
    BatchGetItemOutputTypeDef,
    BatchWriteItemOutputTypeDef,
    ConditionTypeDef,
    DeleteItemOutputTypeDef,
    DeleteTableOutputTypeDef,
    ExpectedAttributeValueTypeDef,
    GetItemOutputTypeDef,
    GlobalSecondaryIndexTypeDef,
    GlobalSecondaryIndexUpdateTypeDef,
    KeysAndAttributesTypeDef,
    KeySchemaElementTypeDef,
    LocalSecondaryIndexTypeDef,
    ProvisionedThroughputTypeDef,
    PutItemOutputTypeDef,
    QueryOutputTypeDef,
    ReplicationGroupUpdateTypeDef,
    ScanOutputTypeDef,
    SSESpecificationTypeDef,
    StreamSpecificationTypeDef,
    TagTypeDef,
    UpdateItemOutputTypeDef,
    WriteRequestTypeDef,
)

__all__ = ("DynamoDBServiceResource", "Table", "ServiceResourceTablesCollection")

class ServiceResourceTablesCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#serviceresourcetablescollection)
    """

    def all(self) -> "ServiceResourceTablesCollection":
        pass
    def filter(  # type: ignore
        self, *, ExclusiveStartTableName: str = None, Limit: int = None
    ) -> "ServiceResourceTablesCollection":
        pass
    def limit(self, count: int) -> "ServiceResourceTablesCollection":
        pass
    def page_size(self, count: int) -> "ServiceResourceTablesCollection":
        pass
    def pages(self) -> Iterator[List["Table"]]:
        pass
    def __iter__(self) -> Iterator["Table"]:
        pass

class Table(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.Table)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#table)
    """

    attribute_definitions: List[Any]
    table_name: str
    key_schema: List[Any]
    table_status: str
    creation_date_time: datetime
    provisioned_throughput: Dict[str, Any]
    table_size_bytes: int
    item_count: int
    table_arn: str
    table_id: str
    billing_mode_summary: Dict[str, Any]
    local_secondary_indexes: List[Any]
    global_secondary_indexes: List[Any]
    stream_specification: Dict[str, Any]
    latest_stream_label: str
    latest_stream_arn: str
    global_table_version: str
    replicas: List[Any]
    restore_summary: Dict[str, Any]
    sse_description: Dict[str, Any]
    archival_summary: Dict[str, Any]
    name: str
    def batch_writer(self, overwrite_by_pkeys: List[str] = None) -> BatchWriter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.batch_writer)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tablebatch_writer-method)
        """
    def delete(self) -> DeleteTableOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.delete)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tabledelete-method)
        """
    def delete_item(
        self,
        *,
        Key: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        Expected: Dict[str, ExpectedAttributeValueTypeDef] = None,
        ConditionalOperator: ConditionalOperatorType = None,
        ReturnValues: ReturnValueType = None,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = None,
        ConditionExpression: str = None,
        ExpressionAttributeNames: Dict[str, str] = None,
        ExpressionAttributeValues: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None
    ) -> DeleteItemOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.delete_item)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tabledelete_item-method)
        """
    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tableget_available_subresources-method)
        """
    def get_item(
        self,
        *,
        Key: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        AttributesToGet: List[str] = None,
        ConsistentRead: bool = None,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        ProjectionExpression: str = None,
        ExpressionAttributeNames: Dict[str, str] = None
    ) -> GetItemOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.get_item)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tableget_item-method)
        """
    def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.load)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tableload-method)
        """
    def put_item(
        self,
        *,
        Item: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        Expected: Dict[str, ExpectedAttributeValueTypeDef] = None,
        ReturnValues: ReturnValueType = None,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = None,
        ConditionalOperator: ConditionalOperatorType = None,
        ConditionExpression: str = None,
        ExpressionAttributeNames: Dict[str, str] = None,
        ExpressionAttributeValues: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None
    ) -> PutItemOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.put_item)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tableput_item-method)
        """
    def query(
        self,
        *,
        IndexName: str = None,
        Select: SelectType = None,
        AttributesToGet: List[str] = None,
        Limit: int = None,
        ConsistentRead: bool = None,
        KeyConditions: Dict[str, ConditionTypeDef] = None,
        QueryFilter: Dict[str, ConditionTypeDef] = None,
        ConditionalOperator: ConditionalOperatorType = None,
        ScanIndexForward: bool = None,
        ExclusiveStartKey: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        ProjectionExpression: str = None,
        FilterExpression: Union[str, ConditionBase] = None,
        KeyConditionExpression: Union[str, ConditionBase] = None,
        ExpressionAttributeNames: Dict[str, str] = None,
        ExpressionAttributeValues: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None
    ) -> QueryOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.query)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tablequery-method)
        """
    def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.reload)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tablereload-method)
        """
    def scan(
        self,
        *,
        IndexName: str = None,
        AttributesToGet: List[str] = None,
        Limit: int = None,
        Select: SelectType = None,
        ScanFilter: Dict[str, ConditionTypeDef] = None,
        ConditionalOperator: ConditionalOperatorType = None,
        ExclusiveStartKey: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        TotalSegments: int = None,
        Segment: int = None,
        ProjectionExpression: str = None,
        FilterExpression: Union[str, ConditionBase] = None,
        ExpressionAttributeNames: Dict[str, str] = None,
        ExpressionAttributeValues: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None,
        ConsistentRead: bool = None
    ) -> ScanOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.scan)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tablescan-method)
        """
    def update(
        self,
        *,
        AttributeDefinitions: List["AttributeDefinitionTypeDef"] = None,
        BillingMode: BillingModeType = None,
        ProvisionedThroughput: "ProvisionedThroughputTypeDef" = None,
        GlobalSecondaryIndexUpdates: List[GlobalSecondaryIndexUpdateTypeDef] = None,
        StreamSpecification: "StreamSpecificationTypeDef" = None,
        SSESpecification: SSESpecificationTypeDef = None,
        ReplicaUpdates: List[ReplicationGroupUpdateTypeDef] = None
    ) -> "_Table":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.update)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tableupdate-method)
        """
    def update_item(
        self,
        *,
        Key: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ],
        AttributeUpdates: Dict[str, AttributeValueUpdateTypeDef] = None,
        Expected: Dict[str, ExpectedAttributeValueTypeDef] = None,
        ConditionalOperator: ConditionalOperatorType = None,
        ReturnValues: ReturnValueType = None,
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = None,
        UpdateExpression: str = None,
        ConditionExpression: str = None,
        ExpressionAttributeNames: Dict[str, str] = None,
        ExpressionAttributeValues: Dict[
            str,
            Union[
                bytes,
                bytearray,
                str,
                int,
                Decimal,
                bool,
                Set[int],
                Set[Decimal],
                Set[str],
                Set[bytes],
                Set[bytearray],
                List[Any],
                Dict[str, Any],
                None,
            ],
        ] = None
    ) -> UpdateItemOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.update_item)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tableupdate_item-method)
        """
    def wait_until_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.wait_until_exists)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tablewait_until_exists-method)
        """
    def wait_until_not_exists(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.Table.wait_until_not_exists)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#tablewait_until_not_exists-method)
        """

_Table = Table

class DynamoDBServiceResource(Boto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource)[Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html)
    """

    tables: ServiceResourceTablesCollection
    def Table(self, name: str) -> _Table:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.Table)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#dynamodbserviceresourcetable-method)
        """
    def batch_get_item(
        self,
        *,
        RequestItems: Dict[str, "KeysAndAttributesTypeDef"],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None
    ) -> BatchGetItemOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.batch_get_item)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#dynamodbserviceresourcebatch_get_item-method)
        """
    def batch_write_item(
        self,
        *,
        RequestItems: Dict[str, List["WriteRequestTypeDef"]],
        ReturnConsumedCapacity: ReturnConsumedCapacityType = None,
        ReturnItemCollectionMetrics: ReturnItemCollectionMetricsType = None
    ) -> BatchWriteItemOutputTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.batch_write_item)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#dynamodbserviceresourcebatch_write_item-method)
        """
    def create_table(
        self,
        *,
        AttributeDefinitions: List["AttributeDefinitionTypeDef"],
        TableName: str,
        KeySchema: List["KeySchemaElementTypeDef"],
        LocalSecondaryIndexes: List[LocalSecondaryIndexTypeDef] = None,
        GlobalSecondaryIndexes: List[GlobalSecondaryIndexTypeDef] = None,
        BillingMode: BillingModeType = None,
        ProvisionedThroughput: "ProvisionedThroughputTypeDef" = None,
        StreamSpecification: "StreamSpecificationTypeDef" = None,
        SSESpecification: SSESpecificationTypeDef = None,
        Tags: List["TagTypeDef"] = None
    ) -> _Table:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.create_table)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#dynamodbserviceresourcecreate_table-method)
        """
    def get_available_subresources(self) -> List[str]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/dynamodb.html#DynamoDB.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource.html#dynamodbserviceresourceget_available_subresources-method)
        """
