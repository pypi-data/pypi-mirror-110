"""
Type annotations for dynamodbstreams service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_dynamodbstreams/type_defs.html)

Usage::

    ```python
    from mypy_boto3_dynamodbstreams.type_defs import AttributeValueTypeDef

    data: AttributeValueTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Union

from .literals import KeyTypeType, OperationTypeType, StreamStatusType, StreamViewTypeType

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AttributeValueTypeDef",
    "DescribeStreamOutputTypeDef",
    "GetRecordsOutputTypeDef",
    "GetShardIteratorOutputTypeDef",
    "IdentityTypeDef",
    "KeySchemaElementTypeDef",
    "ListStreamsOutputTypeDef",
    "RecordTypeDef",
    "ResponseMetadataTypeDef",
    "SequenceNumberRangeTypeDef",
    "ShardTypeDef",
    "StreamDescriptionTypeDef",
    "StreamRecordTypeDef",
    "StreamTypeDef",
)

AttributeValueTypeDef = TypedDict(
    "AttributeValueTypeDef",
    {
        "S": str,
        "N": str,
        "B": Union[bytes, IO[bytes]],
        "SS": List[str],
        "NS": List[str],
        "BS": List[Union[bytes, IO[bytes]]],
        "M": Dict[str, Dict[str, Any]],
        "L": List[Dict[str, Any]],
        "NULL": bool,
        "BOOL": bool,
    },
    total=False,
)

DescribeStreamOutputTypeDef = TypedDict(
    "DescribeStreamOutputTypeDef",
    {
        "StreamDescription": "StreamDescriptionTypeDef",
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetRecordsOutputTypeDef = TypedDict(
    "GetRecordsOutputTypeDef",
    {
        "Records": List["RecordTypeDef"],
        "NextShardIterator": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetShardIteratorOutputTypeDef = TypedDict(
    "GetShardIteratorOutputTypeDef",
    {
        "ShardIterator": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "PrincipalId": str,
        "Type": str,
    },
    total=False,
)

KeySchemaElementTypeDef = TypedDict(
    "KeySchemaElementTypeDef",
    {
        "AttributeName": str,
        "KeyType": KeyTypeType,
    },
)

ListStreamsOutputTypeDef = TypedDict(
    "ListStreamsOutputTypeDef",
    {
        "Streams": List["StreamTypeDef"],
        "LastEvaluatedStreamArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RecordTypeDef = TypedDict(
    "RecordTypeDef",
    {
        "eventID": str,
        "eventName": OperationTypeType,
        "eventVersion": str,
        "eventSource": str,
        "awsRegion": str,
        "dynamodb": "StreamRecordTypeDef",
        "userIdentity": "IdentityTypeDef",
    },
    total=False,
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, Any],
        "RetryAttempts": int,
    },
)

SequenceNumberRangeTypeDef = TypedDict(
    "SequenceNumberRangeTypeDef",
    {
        "StartingSequenceNumber": str,
        "EndingSequenceNumber": str,
    },
    total=False,
)

ShardTypeDef = TypedDict(
    "ShardTypeDef",
    {
        "ShardId": str,
        "SequenceNumberRange": "SequenceNumberRangeTypeDef",
        "ParentShardId": str,
    },
    total=False,
)

StreamDescriptionTypeDef = TypedDict(
    "StreamDescriptionTypeDef",
    {
        "StreamArn": str,
        "StreamLabel": str,
        "StreamStatus": StreamStatusType,
        "StreamViewType": StreamViewTypeType,
        "CreationRequestDateTime": datetime,
        "TableName": str,
        "KeySchema": List["KeySchemaElementTypeDef"],
        "Shards": List["ShardTypeDef"],
        "LastEvaluatedShardId": str,
    },
    total=False,
)

StreamRecordTypeDef = TypedDict(
    "StreamRecordTypeDef",
    {
        "ApproximateCreationDateTime": datetime,
        "Keys": Dict[str, "AttributeValueTypeDef"],
        "NewImage": Dict[str, "AttributeValueTypeDef"],
        "OldImage": Dict[str, "AttributeValueTypeDef"],
        "SequenceNumber": str,
        "SizeBytes": int,
        "StreamViewType": StreamViewTypeType,
    },
    total=False,
)

StreamTypeDef = TypedDict(
    "StreamTypeDef",
    {
        "StreamArn": str,
        "TableName": str,
        "StreamLabel": str,
    },
    total=False,
)
