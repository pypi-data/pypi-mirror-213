from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class ResumptionTokenType:
    """
    A resumptionToken may have 3 optional attributes and can be used in ListSets,
    ListIdentifiers, ListRecords responses.
    """
    class Meta:
        name = "resumptionTokenType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    expiration_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "expirationDate",
            "type": "Attribute",
        }
    )
    complete_list_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "completeListSize",
            "type": "Attribute",
        }
    )
    cursor: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
