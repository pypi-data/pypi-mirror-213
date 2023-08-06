from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "https://api.bioriv.org/OAI/medRxivRaw/"


@dataclass
class MedRxivRawType:
    class Meta:
        name = "medRxivRaw_type"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    submitter: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    version: Optional["MedRxivRawType.Version"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    authors: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    corresponding_author: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    corresponding_author_institution: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    published: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    categories: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    msc_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "msc-class",
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    abstract: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )
    link_pdf: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
            "required": True,
        }
    )

    @dataclass
    class Version:
        date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
                "required": True,
            }
        )
        size: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "https://api.bioriv.org/OAI/medRxivRaw/",
                "required": True,
            }
        )
        version: Optional[int] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
