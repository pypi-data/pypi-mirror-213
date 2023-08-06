from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from .about_type import AboutType
from .header_type import HeaderType
from .metadata_type import MetadataType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class RecordType:
    """
    A record has a header, a metadata part, and an optional about container.
    """
    class Meta:
        name = "recordType"

    header: Optional[HeaderType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    metadata: Optional[MetadataType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    about: List[AboutType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
