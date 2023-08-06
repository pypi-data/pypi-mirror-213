from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional
from .oai_pmherrorcode_type import OaiPmherrorcodeType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class OaiPmherrorType:
    class Meta:
        name = "OAI-PMHerrorType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    code: Optional[OaiPmherrorcodeType] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
