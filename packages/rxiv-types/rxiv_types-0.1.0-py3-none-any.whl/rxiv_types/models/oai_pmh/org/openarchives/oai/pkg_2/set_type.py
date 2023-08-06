from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from .description_type import DescriptionType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class SetType:
    class Meta:
        name = "setType"

    set_spec: Optional[str] = field(
        default=None,
        metadata={
            "name": "setSpec",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
            "pattern": r"([A-Za-z0-9\-_\.!~\*'\(\)])+(:[A-Za-z0-9\-_\.!~\*'\(\)]+)*",
        }
    )
    set_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "setName",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    set_description: List[DescriptionType] = field(
        default_factory=list,
        metadata={
            "name": "setDescription",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
