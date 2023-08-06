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
class ChemRxivHeaderType(HeaderType):
    """This class only exists because chemRxiv does not follow OAI PMH schema."""

    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        },
    )

    version_history: List[str] = field(
        default_factory=list,
        metadata={
            "name": "version-history",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        },
    )

    submitted_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "submitted-date",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        },
    )


@dataclass
class ChemRxivMetadata:
    dc: Optional[Dc] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/oai_dc/",
        },
    )


@dataclass
class ChemRxivRecord(RecordType):
    header: Optional[ChemRxivHeaderType] = RecordType.__dataclass_fields__["header"]
    metadata: Optional[ChemRxivMetadata] = RecordType.__dataclass_fields__["metadata"]


@dataclass
class ChemRxivListRecords(ListRecordsType):
    record: List[ChemRxivRecord] = ListRecordsType.__dataclass_fields__["record"]


@dataclass
class ChemRxiv(OaiPmhtype):
    list_records: Optional[ChemRxivListRecords] = OaiPmhtype.__dataclass_fields__[
        "list_records"
    ]


def chemrxiv_records(xml: Union[Path, str]) -> ChemRxiv:
    parser = XmlParser()

    result = parser.parse(xml, ChemRxiv)

    return result
