from pydantic.dataclasses import dataclass
from .bio_rxiv_raw_type import BioRxivRawType

__NAMESPACE__ = "https://api.biorxiv.org/oaipmh/bioRxivRaw/"


@dataclass
class BioRxivRaw(BioRxivRawType):
    class Meta:
        name = "bioRxivRaw"
        namespace = "https://api.biorxiv.org/oaipmh/bioRxivRaw/"
