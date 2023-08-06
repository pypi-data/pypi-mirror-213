from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "https://api.biorxiv.org/oaipmh/bioRxivRaw/"


@dataclass
class BioRxivRawType:
    class Meta:
        name = "bioRxivRaw_type"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    submitter: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    version: Optional["BioRxivRawType.Version"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    authors: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    corresponding_author: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    corresponding_author_institution: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    published: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    categories: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    msc_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "msc-class",
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    abstract: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )
    link_pdf: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
            "required": True,
        }
    )

    @dataclass
    class Version:
        date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
                "required": True,
            }
        )
        size: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "https://api.biorxiv.org/oaipmh/bioRxivRaw/",
                "required": True,
            }
        )
        version: Optional[int] = field(
            default=None,
            metadata={
                "type": "Attribute",
            }
        )
