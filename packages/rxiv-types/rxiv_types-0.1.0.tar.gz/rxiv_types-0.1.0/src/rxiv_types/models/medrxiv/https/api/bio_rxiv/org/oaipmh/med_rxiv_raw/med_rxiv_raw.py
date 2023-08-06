from pydantic.dataclasses import dataclass
from .med_rxiv_raw_type import MedRxivRawType

__NAMESPACE__ = "https://api.bioriv.org/OAI/medRxivRaw/"


@dataclass
class MedRxivRaw(MedRxivRawType):
    class Meta:
        name = "medRxivRaw"
        namespace = "https://api.bioriv.org/OAI/medRxivRaw/"
