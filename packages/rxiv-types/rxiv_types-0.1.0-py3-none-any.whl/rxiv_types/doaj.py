import io
from dataclasses import field
from pathlib import Path
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass
from xsdata_pydantic.bindings import XmlParser

from .models.oai_dc.org.openarchives.oai.pkg_2.pkg_0.oai_dc.dc import Dc
from .models.oai_pmh.org.openarchives.oai.pkg_2.header_type import HeaderType
from .models.oai_pmh.org.openarchives.oai.pkg_2.oai_pmhtype import OaiPmhtype
from .models.oai_pmh.org.openarchives.oai.pkg_2.list_records_type import (
    ListRecordsType,
)
from .models.oai_pmh.org.openarchives.oai.pkg_2.record_type import RecordType


@dataclass
class DoajMetadata:
    dc: Optional[Dc] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
        },
    )


@dataclass
class DoajRecord(RecordType):
    header: Optional[HeaderType] = RecordType.__dataclass_fields__["header"]
    metadata: Optional[DoajMetadata] = RecordType.__dataclass_fields__["metadata"]


@dataclass
class DoajListRecords(ListRecordsType):
    record: List[DoajRecord] = ListRecordsType.__dataclass_fields__["record"]


@dataclass
class Doaj(OaiPmhtype):
    list_records: Optional[DoajListRecords] = OaiPmhtype.__dataclass_fields__[
        "list_records"
    ]


def doaj_records(xml: Union[Path, str]) -> Doaj:
    parser = XmlParser()

    with open(xml, "rb") as fr:
        data = fr.read().replace("dcterms:".encode(), "".encode())
        fb = io.BytesIO(data)

    result = parser.parse(fb, Doaj)

    return result
