from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from .get_record_type import GetRecordType
from .identify_type import IdentifyType
from .list_identifiers_type import ListIdentifiersType
from .list_metadata_formats_type import ListMetadataFormatsType
from .list_records_type import ListRecordsType
from .list_sets_type import ListSetsType
from .oai_pmherror_type import OaiPmherrorType
from .request_type import RequestType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class OaiPmhtype:
    class Meta:
        name = "OAI-PMHtype"

    response_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "responseDate",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    request: Optional[RequestType] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "required": True,
        }
    )
    error: List[OaiPmherrorType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    identify: Optional[IdentifyType] = field(
        default=None,
        metadata={
            "name": "Identify",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    list_metadata_formats: Optional[ListMetadataFormatsType] = field(
        default=None,
        metadata={
            "name": "ListMetadataFormats",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    list_sets: Optional[ListSetsType] = field(
        default=None,
        metadata={
            "name": "ListSets",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    get_record: Optional[GetRecordType] = field(
        default=None,
        metadata={
            "name": "GetRecord",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    list_identifiers: Optional[ListIdentifiersType] = field(
        default=None,
        metadata={
            "name": "ListIdentifiers",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
    list_records: Optional[ListRecordsType] = field(
        default=None,
        metadata={
            "name": "ListRecords",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
