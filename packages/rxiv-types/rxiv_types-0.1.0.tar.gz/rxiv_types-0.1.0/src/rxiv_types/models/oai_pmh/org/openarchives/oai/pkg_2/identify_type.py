from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate
from .deleted_record_type import DeletedRecordType
from .description_type import DescriptionType
from .granularity_type import GranularityType
from .protocol_version_type import ProtocolVersionType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class IdentifyType:
    repository_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "repositoryName",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    base_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "baseURL",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    protocol_version: Optional[ProtocolVersionType] = field(
        default=None,
        metadata={
            "name": "protocolVersion",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    admin_email: List[str] = field(
        default_factory=list,
        metadata={
            "name": "adminEmail",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "min_occurs": 1,
            "pattern": r"\S+@(\S+\.)+\S+",
        }
    )
    earliest_datestamp: Optional[Union[XmlDate, str]] = field(
        default=None,
        metadata={
            "name": "earliestDatestamp",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
            "pattern": r".*Z",
        }
    )
    deleted_record: Optional[DeletedRecordType] = field(
        default=None,
        metadata={
            "name": "deletedRecord",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    granularity: Optional[GranularityType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    compression: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    description: List[DescriptionType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
