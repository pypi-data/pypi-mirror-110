"""
Type annotations for meteringmarketplace service type definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_meteringmarketplace/type_defs.html)

Usage::

    ```python
    from mypy_boto3_meteringmarketplace.type_defs import BatchMeterUsageResultTypeDef

    data: BatchMeterUsageResultTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import List

from .literals import UsageRecordResultStatusType

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BatchMeterUsageResultTypeDef",
    "MeterUsageResultTypeDef",
    "RegisterUsageResultTypeDef",
    "ResolveCustomerResultTypeDef",
    "TagTypeDef",
    "UsageAllocationTypeDef",
    "UsageRecordResultTypeDef",
    "UsageRecordTypeDef",
)

BatchMeterUsageResultTypeDef = TypedDict(
    "BatchMeterUsageResultTypeDef",
    {
        "Results": List["UsageRecordResultTypeDef"],
        "UnprocessedRecords": List["UsageRecordTypeDef"],
    },
    total=False,
)

MeterUsageResultTypeDef = TypedDict(
    "MeterUsageResultTypeDef",
    {
        "MeteringRecordId": str,
    },
    total=False,
)

RegisterUsageResultTypeDef = TypedDict(
    "RegisterUsageResultTypeDef",
    {
        "PublicKeyRotationTimestamp": datetime,
        "Signature": str,
    },
    total=False,
)

ResolveCustomerResultTypeDef = TypedDict(
    "ResolveCustomerResultTypeDef",
    {
        "CustomerIdentifier": str,
        "ProductCode": str,
    },
    total=False,
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

_RequiredUsageAllocationTypeDef = TypedDict(
    "_RequiredUsageAllocationTypeDef",
    {
        "AllocatedUsageQuantity": int,
    },
)
_OptionalUsageAllocationTypeDef = TypedDict(
    "_OptionalUsageAllocationTypeDef",
    {
        "Tags": List["TagTypeDef"],
    },
    total=False,
)


class UsageAllocationTypeDef(_RequiredUsageAllocationTypeDef, _OptionalUsageAllocationTypeDef):
    pass


UsageRecordResultTypeDef = TypedDict(
    "UsageRecordResultTypeDef",
    {
        "UsageRecord": "UsageRecordTypeDef",
        "MeteringRecordId": str,
        "Status": UsageRecordResultStatusType,
    },
    total=False,
)

_RequiredUsageRecordTypeDef = TypedDict(
    "_RequiredUsageRecordTypeDef",
    {
        "Timestamp": datetime,
        "CustomerIdentifier": str,
        "Dimension": str,
    },
)
_OptionalUsageRecordTypeDef = TypedDict(
    "_OptionalUsageRecordTypeDef",
    {
        "Quantity": int,
        "UsageAllocations": List["UsageAllocationTypeDef"],
    },
    total=False,
)


class UsageRecordTypeDef(_RequiredUsageRecordTypeDef, _OptionalUsageRecordTypeDef):
    pass
