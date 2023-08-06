from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from .resumption_token_type import ResumptionTokenType
from .set_type import SetType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class ListSetsType:
    set: List[SetType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "min_occurs": 1,
        }
    )
    resumption_token: Optional[ResumptionTokenType] = field(
        default=None,
        metadata={
            "name": "resumptionToken",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
