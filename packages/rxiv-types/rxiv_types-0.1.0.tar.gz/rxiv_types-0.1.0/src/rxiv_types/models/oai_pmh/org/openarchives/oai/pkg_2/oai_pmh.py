from pydantic.dataclasses import dataclass
from .oai_pmhtype import OaiPmhtype

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class OaiPmh(OaiPmhtype):
    class Meta:
        name = "OAI-PMH"
        namespace = "http://www.openarchives.org/OAI/2.0/"
