from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class DescriptionType:
    """The descriptionType is used for the description element in Identify and for
    setDescription element in ListSets.

    Content must be compliant with an XML Schema defined by a community.
    """
    class Meta:
        name = "descriptionType"

    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        }
    )
