from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class MetadataType:
    """Metadata must be expressed in XML that complies with another XML Schema
    (namespace=#other).

    Metadata must be explicitly qualified in the response.
    """
    class Meta:
        name = "metadataType"

    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        }
    )
