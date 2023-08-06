from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List
from .metadata_format_type import MetadataFormatType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class ListMetadataFormatsType:
    metadata_format: List[MetadataFormatType] = field(
        default_factory=list,
        metadata={
            "name": "metadataFormat",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "min_occurs": 1,
        }
    )
