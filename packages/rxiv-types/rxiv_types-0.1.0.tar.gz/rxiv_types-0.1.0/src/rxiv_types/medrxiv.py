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
from .models.medrxiv.https.api.bio_rxiv.org.oaipmh.med_rxiv_raw.med_rxiv_raw import (
    MedRxivRaw,
)


@dataclass
class MedRxivMetadata:
    medarxiv_raw: Optional[MedRxivRaw] = field(
        default=None,
        metadata={
            "type": "Element",
            "name": "medRxivRaw",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
        },
    )


@dataclass
class MedRxivRecord(RecordType):
    metadata: Optional[MedRxivMetadata] = RecordType.__dataclass_fields__["metadata"]


@dataclass
class MedRxivListRecords(ListRecordsType):
    record: List[MedRxivRecord] = ListRecordsType.__dataclass_fields__["record"]


@dataclass
class MedRxiv(OaiPmhtype):
    list_records: Optional[MedRxivListRecords] = OaiPmhtype.__dataclass_fields__[
        "list_records"
    ]


def medrxiv_records(xml: Union[Path, str]) -> MedRxiv:
    parser = XmlParser()

    result = parser.parse(xml, MedRxiv)

    return result
