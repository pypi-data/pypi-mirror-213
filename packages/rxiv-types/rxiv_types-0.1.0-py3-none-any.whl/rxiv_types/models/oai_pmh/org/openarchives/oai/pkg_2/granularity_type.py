from enum import Enum

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


class GranularityType(Enum):
    YYYY_MM_DD = "YYYY-MM-DD"
    YYYY_MM_DDTHH_MM_SS_Z = "YYYY-MM-DDThh:mm:ssZ"
