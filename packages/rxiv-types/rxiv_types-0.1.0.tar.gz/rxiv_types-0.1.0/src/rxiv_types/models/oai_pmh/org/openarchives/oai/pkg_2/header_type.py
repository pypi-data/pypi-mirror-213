from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate
from .status_type import StatusType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class HeaderType:
    """A header has a unique identifier, a datestamp, and setSpec(s) in case the
    item from which the record is disseminated belongs to set(s).

    the header can carry a deleted status indicating that the record is
    deleted.
    """
    class Meta:
        name = "headerType"

    identifier: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    datestamp: Optional[Union[XmlDate, str]] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
            "pattern": r".*Z",
        }
    )
    set_spec: List[str] = field(
        default_factory=list,
        metadata={
            "name": "setSpec",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "pattern": r"([A-Za-z0-9\-_\.!~\*'\(\)])+(:[A-Za-z0-9\-_\.!~\*'\(\)]+)*",
        }
    )
    status: Optional[StatusType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
