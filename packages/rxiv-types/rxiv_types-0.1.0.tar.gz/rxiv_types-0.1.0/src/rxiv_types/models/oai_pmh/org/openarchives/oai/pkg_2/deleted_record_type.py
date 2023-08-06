from enum import Enum

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


class DeletedRecordType(Enum):
    NO = "no"
    PERSISTENT = "persistent"
    TRANSIENT = "transient"
