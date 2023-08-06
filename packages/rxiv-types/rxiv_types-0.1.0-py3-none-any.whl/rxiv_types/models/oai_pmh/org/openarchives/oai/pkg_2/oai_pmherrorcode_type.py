from enum import Enum

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


class OaiPmherrorcodeType(Enum):
    CANNOT_DISSEMINATE_FORMAT = "cannotDisseminateFormat"
    ID_DOES_NOT_EXIST = "idDoesNotExist"
    BAD_ARGUMENT = "badArgument"
    BAD_VERB = "badVerb"
    NO_METADATA_FORMATS = "noMetadataFormats"
    NO_RECORDS_MATCH = "noRecordsMatch"
    BAD_RESUMPTION_TOKEN = "badResumptionToken"
    NO_SET_HIERARCHY = "noSetHierarchy"
