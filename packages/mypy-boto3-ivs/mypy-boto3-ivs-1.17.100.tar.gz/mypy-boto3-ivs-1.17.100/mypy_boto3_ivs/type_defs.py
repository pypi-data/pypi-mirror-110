"""
Type annotations for ivs service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_ivs/type_defs.html)

Usage::

    ```python
    from mypy_boto3_ivs.type_defs import BatchErrorTypeDef

    data: BatchErrorTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

from .literals import (
    ChannelLatencyModeType,
    ChannelTypeType,
    RecordingConfigurationStateType,
    StreamHealthType,
    StreamStateType,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BatchErrorTypeDef",
    "BatchGetChannelResponseTypeDef",
    "BatchGetStreamKeyResponseTypeDef",
    "ChannelSummaryTypeDef",
    "ChannelTypeDef",
    "CreateChannelResponseTypeDef",
    "CreateRecordingConfigurationResponseTypeDef",
    "CreateStreamKeyResponseTypeDef",
    "DestinationConfigurationTypeDef",
    "GetChannelResponseTypeDef",
    "GetPlaybackKeyPairResponseTypeDef",
    "GetRecordingConfigurationResponseTypeDef",
    "GetStreamKeyResponseTypeDef",
    "GetStreamResponseTypeDef",
    "ImportPlaybackKeyPairResponseTypeDef",
    "ListChannelsResponseTypeDef",
    "ListPlaybackKeyPairsResponseTypeDef",
    "ListRecordingConfigurationsResponseTypeDef",
    "ListStreamKeysResponseTypeDef",
    "ListStreamsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PlaybackKeyPairSummaryTypeDef",
    "PlaybackKeyPairTypeDef",
    "RecordingConfigurationSummaryTypeDef",
    "RecordingConfigurationTypeDef",
    "S3DestinationConfigurationTypeDef",
    "StreamKeySummaryTypeDef",
    "StreamKeyTypeDef",
    "StreamSummaryTypeDef",
    "StreamTypeDef",
    "UpdateChannelResponseTypeDef",
)

BatchErrorTypeDef = TypedDict(
    "BatchErrorTypeDef",
    {
        "arn": str,
        "code": str,
        "message": str,
    },
    total=False,
)

BatchGetChannelResponseTypeDef = TypedDict(
    "BatchGetChannelResponseTypeDef",
    {
        "channels": List["ChannelTypeDef"],
        "errors": List["BatchErrorTypeDef"],
    },
    total=False,
)

BatchGetStreamKeyResponseTypeDef = TypedDict(
    "BatchGetStreamKeyResponseTypeDef",
    {
        "streamKeys": List["StreamKeyTypeDef"],
        "errors": List["BatchErrorTypeDef"],
    },
    total=False,
)

ChannelSummaryTypeDef = TypedDict(
    "ChannelSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "latencyMode": ChannelLatencyModeType,
        "authorized": bool,
        "recordingConfigurationArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

ChannelTypeDef = TypedDict(
    "ChannelTypeDef",
    {
        "arn": str,
        "name": str,
        "latencyMode": ChannelLatencyModeType,
        "type": ChannelTypeType,
        "recordingConfigurationArn": str,
        "ingestEndpoint": str,
        "playbackUrl": str,
        "authorized": bool,
        "tags": Dict[str, str],
    },
    total=False,
)

CreateChannelResponseTypeDef = TypedDict(
    "CreateChannelResponseTypeDef",
    {
        "channel": "ChannelTypeDef",
        "streamKey": "StreamKeyTypeDef",
    },
    total=False,
)

CreateRecordingConfigurationResponseTypeDef = TypedDict(
    "CreateRecordingConfigurationResponseTypeDef",
    {
        "recordingConfiguration": "RecordingConfigurationTypeDef",
    },
    total=False,
)

CreateStreamKeyResponseTypeDef = TypedDict(
    "CreateStreamKeyResponseTypeDef",
    {
        "streamKey": "StreamKeyTypeDef",
    },
    total=False,
)

DestinationConfigurationTypeDef = TypedDict(
    "DestinationConfigurationTypeDef",
    {
        "s3": "S3DestinationConfigurationTypeDef",
    },
    total=False,
)

GetChannelResponseTypeDef = TypedDict(
    "GetChannelResponseTypeDef",
    {
        "channel": "ChannelTypeDef",
    },
    total=False,
)

GetPlaybackKeyPairResponseTypeDef = TypedDict(
    "GetPlaybackKeyPairResponseTypeDef",
    {
        "keyPair": "PlaybackKeyPairTypeDef",
    },
    total=False,
)

GetRecordingConfigurationResponseTypeDef = TypedDict(
    "GetRecordingConfigurationResponseTypeDef",
    {
        "recordingConfiguration": "RecordingConfigurationTypeDef",
    },
    total=False,
)

GetStreamKeyResponseTypeDef = TypedDict(
    "GetStreamKeyResponseTypeDef",
    {
        "streamKey": "StreamKeyTypeDef",
    },
    total=False,
)

GetStreamResponseTypeDef = TypedDict(
    "GetStreamResponseTypeDef",
    {
        "stream": "StreamTypeDef",
    },
    total=False,
)

ImportPlaybackKeyPairResponseTypeDef = TypedDict(
    "ImportPlaybackKeyPairResponseTypeDef",
    {
        "keyPair": "PlaybackKeyPairTypeDef",
    },
    total=False,
)

_RequiredListChannelsResponseTypeDef = TypedDict(
    "_RequiredListChannelsResponseTypeDef",
    {
        "channels": List["ChannelSummaryTypeDef"],
    },
)
_OptionalListChannelsResponseTypeDef = TypedDict(
    "_OptionalListChannelsResponseTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListChannelsResponseTypeDef(
    _RequiredListChannelsResponseTypeDef, _OptionalListChannelsResponseTypeDef
):
    pass


_RequiredListPlaybackKeyPairsResponseTypeDef = TypedDict(
    "_RequiredListPlaybackKeyPairsResponseTypeDef",
    {
        "keyPairs": List["PlaybackKeyPairSummaryTypeDef"],
    },
)
_OptionalListPlaybackKeyPairsResponseTypeDef = TypedDict(
    "_OptionalListPlaybackKeyPairsResponseTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListPlaybackKeyPairsResponseTypeDef(
    _RequiredListPlaybackKeyPairsResponseTypeDef, _OptionalListPlaybackKeyPairsResponseTypeDef
):
    pass


_RequiredListRecordingConfigurationsResponseTypeDef = TypedDict(
    "_RequiredListRecordingConfigurationsResponseTypeDef",
    {
        "recordingConfigurations": List["RecordingConfigurationSummaryTypeDef"],
    },
)
_OptionalListRecordingConfigurationsResponseTypeDef = TypedDict(
    "_OptionalListRecordingConfigurationsResponseTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListRecordingConfigurationsResponseTypeDef(
    _RequiredListRecordingConfigurationsResponseTypeDef,
    _OptionalListRecordingConfigurationsResponseTypeDef,
):
    pass


_RequiredListStreamKeysResponseTypeDef = TypedDict(
    "_RequiredListStreamKeysResponseTypeDef",
    {
        "streamKeys": List["StreamKeySummaryTypeDef"],
    },
)
_OptionalListStreamKeysResponseTypeDef = TypedDict(
    "_OptionalListStreamKeysResponseTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListStreamKeysResponseTypeDef(
    _RequiredListStreamKeysResponseTypeDef, _OptionalListStreamKeysResponseTypeDef
):
    pass


_RequiredListStreamsResponseTypeDef = TypedDict(
    "_RequiredListStreamsResponseTypeDef",
    {
        "streams": List["StreamSummaryTypeDef"],
    },
)
_OptionalListStreamsResponseTypeDef = TypedDict(
    "_OptionalListStreamsResponseTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListStreamsResponseTypeDef(
    _RequiredListStreamsResponseTypeDef, _OptionalListStreamsResponseTypeDef
):
    pass


_RequiredListTagsForResourceResponseTypeDef = TypedDict(
    "_RequiredListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
    },
)
_OptionalListTagsForResourceResponseTypeDef = TypedDict(
    "_OptionalListTagsForResourceResponseTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)


class ListTagsForResourceResponseTypeDef(
    _RequiredListTagsForResourceResponseTypeDef, _OptionalListTagsForResourceResponseTypeDef
):
    pass


PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PlaybackKeyPairSummaryTypeDef = TypedDict(
    "PlaybackKeyPairSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "tags": Dict[str, str],
    },
    total=False,
)

PlaybackKeyPairTypeDef = TypedDict(
    "PlaybackKeyPairTypeDef",
    {
        "arn": str,
        "name": str,
        "fingerprint": str,
        "tags": Dict[str, str],
    },
    total=False,
)

_RequiredRecordingConfigurationSummaryTypeDef = TypedDict(
    "_RequiredRecordingConfigurationSummaryTypeDef",
    {
        "arn": str,
        "destinationConfiguration": "DestinationConfigurationTypeDef",
        "state": RecordingConfigurationStateType,
    },
)
_OptionalRecordingConfigurationSummaryTypeDef = TypedDict(
    "_OptionalRecordingConfigurationSummaryTypeDef",
    {
        "name": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class RecordingConfigurationSummaryTypeDef(
    _RequiredRecordingConfigurationSummaryTypeDef, _OptionalRecordingConfigurationSummaryTypeDef
):
    pass


_RequiredRecordingConfigurationTypeDef = TypedDict(
    "_RequiredRecordingConfigurationTypeDef",
    {
        "arn": str,
        "destinationConfiguration": "DestinationConfigurationTypeDef",
        "state": RecordingConfigurationStateType,
    },
)
_OptionalRecordingConfigurationTypeDef = TypedDict(
    "_OptionalRecordingConfigurationTypeDef",
    {
        "name": str,
        "tags": Dict[str, str],
    },
    total=False,
)


class RecordingConfigurationTypeDef(
    _RequiredRecordingConfigurationTypeDef, _OptionalRecordingConfigurationTypeDef
):
    pass


S3DestinationConfigurationTypeDef = TypedDict(
    "S3DestinationConfigurationTypeDef",
    {
        "bucketName": str,
    },
)

StreamKeySummaryTypeDef = TypedDict(
    "StreamKeySummaryTypeDef",
    {
        "arn": str,
        "channelArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

StreamKeyTypeDef = TypedDict(
    "StreamKeyTypeDef",
    {
        "arn": str,
        "value": str,
        "channelArn": str,
        "tags": Dict[str, str],
    },
    total=False,
)

StreamSummaryTypeDef = TypedDict(
    "StreamSummaryTypeDef",
    {
        "channelArn": str,
        "state": StreamStateType,
        "health": StreamHealthType,
        "viewerCount": int,
        "startTime": datetime,
    },
    total=False,
)

StreamTypeDef = TypedDict(
    "StreamTypeDef",
    {
        "channelArn": str,
        "playbackUrl": str,
        "startTime": datetime,
        "state": StreamStateType,
        "health": StreamHealthType,
        "viewerCount": int,
    },
    total=False,
)

UpdateChannelResponseTypeDef = TypedDict(
    "UpdateChannelResponseTypeDef",
    {
        "channel": "ChannelTypeDef",
    },
    total=False,
)
