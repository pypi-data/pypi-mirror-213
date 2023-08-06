from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional
from .record_type import RecordType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class GetRecordType:
    record: Optional[RecordType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
