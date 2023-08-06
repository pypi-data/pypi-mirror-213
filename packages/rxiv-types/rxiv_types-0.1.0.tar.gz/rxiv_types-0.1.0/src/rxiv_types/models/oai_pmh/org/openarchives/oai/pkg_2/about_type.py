from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class AboutType:
    """
    Data "about" the record must be expressed in XML that is compliant with an XML
    Schema defined by a community.
    """
    class Meta:
        name = "aboutType"

    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        }
    )
