from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional, Union
from xsdata.models.datatype import XmlDate
from .verb_type import VerbType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class RequestType:
    """Define requestType, indicating the protocol request that led to the
    response.

    Element content is BASE-URL, attributes are arguments of protocol
    request, attribute-values are values of arguments of protocol
    request
    """
    class Meta:
        name = "requestType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    verb: Optional[VerbType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    identifier: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    metadata_prefix: Optional[str] = field(
        default=None,
        metadata={
            "name": "metadataPrefix",
            "type": "Attribute",
            "pattern": r"[A-Za-z0-9\-_\.!~\*'\(\)]+",
        }
    )
    from_value: Optional[Union[XmlDate, str]] = field(
        default=None,
        metadata={
            "name": "from",
            "type": "Attribute",
            "pattern": r".*Z",
        }
    )
    until: Optional[Union[XmlDate, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r".*Z",
        }
    )
    set: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"([A-Za-z0-9\-_\.!~\*'\(\)])+(:[A-Za-z0-9\-_\.!~\*'\(\)]+)*",
        }
    )
    resumption_token: Optional[str] = field(
        default=None,
        metadata={
            "name": "resumptionToken",
            "type": "Attribute",
        }
    )
