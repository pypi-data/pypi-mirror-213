from pydantic.dataclasses import dataclass
from .oai_dc_type import OaiDcType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/oai_dc/"


@dataclass
class Dc(OaiDcType):
    class Meta:
        name = "dc"
        namespace = "http://www.openarchives.org/OAI/2.0/oai_dc/"
