from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_edta_cod import CfEdtaCod
from ukrdc_xsdata.ukrdc.types.clinician import Clinician

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class CauseOfDeath:
    """
    :ivar diagnosis_type:
    :ivar diagnosing_clinician: Clinician Coding Death
    :ivar diagnosis: Coded Caused of Death (EDTA)
    :ivar comments: Free text about the Diagnosis
    :ivar entered_on: The date the COD was recorded in the medical
        record.
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    diagnosis_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "DiagnosisType",
            "type": "Element",
            "namespace": "",
        }
    )
    diagnosing_clinician: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "DiagnosingClinician",
            "type": "Element",
            "namespace": "",
        }
    )
    diagnosis: Optional[CfEdtaCod] = field(
        default=None,
        metadata={
            "name": "Diagnosis",
            "type": "Element",
            "namespace": "",
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EnteredOn",
            "type": "Element",
            "namespace": "",
        }
    )
    updated_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "UpdatedOn",
            "type": "Element",
            "namespace": "",
        }
    )
    external_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalId",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
