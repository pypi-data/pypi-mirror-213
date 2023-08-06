from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class MetadataFormatType:
    class Meta:
        name = "metadataFormatType"

    metadata_prefix: Optional[str] = field(
        default=None,
        metadata={
            "name": "metadataPrefix",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
            "pattern": r"[A-Za-z0-9\-_\.!~\*'\(\)]+",
        }
    )
    schema_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "schema",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    metadata_namespace: Optional[str] = field(
        default=None,
        metadata={
            "name": "metadataNamespace",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
