from dataclasses import field
from pathlib import Path
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass
from xsdata_pydantic.bindings import XmlParser

from .models.oai_pmh.org.openarchives.oai.pkg_2.oai_pmhtype import OaiPmhtype
from .models.oai_pmh.org.openarchives.oai.pkg_2.list_records_type import (
    ListRecordsType,
)
from .models.oai_pmh.org.openarchives.oai.pkg_2.record_type import RecordType
from .models.biorxiv.https.api.biorxiv.org.oaipmh.bio_rxiv_raw.bio_rxiv_raw import (
    BioRxivRaw,
)


@dataclass
class BioRxivMetadata:
    bioarxiv_raw: Optional[BioRxivRaw] = field(
        default=None,
        metadata={
            "type": "Element",
            "name": "bioRxivRaw",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
        },
    )


@dataclass
class BioRxivRecord(RecordType):
    metadata: Optional[BioRxivMetadata] = RecordType.__dataclass_fields__["metadata"]


@dataclass
class BioRxivListRecords(ListRecordsType):
    record: List[BioRxivRecord] = ListRecordsType.__dataclass_fields__["record"]


@dataclass
class BioRxiv(OaiPmhtype):
    list_records: Optional[BioRxivListRecords] = OaiPmhtype.__dataclass_fields__[
        "list_records"
    ]


def biorxiv_records(xml: Union[Path, str]) -> BioRxiv:
    parser = XmlParser()

    result = parser.parse(xml, BioRxiv)

    return result
