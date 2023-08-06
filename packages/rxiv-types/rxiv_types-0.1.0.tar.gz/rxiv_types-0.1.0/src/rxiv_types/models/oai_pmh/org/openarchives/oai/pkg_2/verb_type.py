from enum import Enum

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


class VerbType(Enum):
    IDENTIFY = "Identify"
    LIST_METADATA_FORMATS = "ListMetadataFormats"
    LIST_SETS = "ListSets"
    GET_RECORD = "GetRecord"
    LIST_IDENTIFIERS = "ListIdentifiers"
    LIST_RECORDS = "ListRecords"
