from dataclasses import field
from pathlib import Path
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass
from xsdata_pydantic.bindings import XmlParser

from .models.oai_dc.org.openarchives.oai.pkg_2.pkg_0.oai_dc.dc import Dc
from .models.oai_pmh.org.openarchives.oai.pkg_2.oai_pmhtype import OaiPmhtype
from .models.oai_pmh.org.openarchives.oai.pkg_2.list_records_type import (
    ListRecordsType,
)
from .models.oai_pmh.org.openarchives.oai.pkg_2.record_type import RecordType


@dataclass
class ArxivMetadata:
    dc: Optional[Dc] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
        },
    )


@dataclass
class ArxivRecord(RecordType):
    metadata: Optional[ArxivMetadata] = RecordType.__dataclass_fields__["metadata"]


@dataclass
class ArxivListRecords(ListRecordsType):
    record: List[ArxivRecord] = ListRecordsType.__dataclass_fields__["record"]


@dataclass
class Arxiv(OaiPmhtype):
    list_records: Optional[ArxivListRecords] = OaiPmhtype.__dataclass_fields__[
        "list_records"
    ]


def arxiv_records(xml: Union[Path, str]) -> Arxiv:
    parser = XmlParser()

    result = parser.parse(xml, Arxiv)

    return result
