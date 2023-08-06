from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_rr7_discharge import CfRr7Discharge
from ukrdc_xsdata.ukrdc.types.cf_rr7_treatment import CfRr7Treatment
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AttributesErf61(Enum):
    """
    :cvar VALUE_1: Unsuitable
    :cvar VALUE_2: Working Up or under discussion
    :cvar VALUE_3: On Transplant List
    :cvar VALUE_4: Suspended on Transplant List
    :cvar VALUE_5: Not Assessed by Start of Dialysis
    """
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"
    VALUE_5 = "5"


class AttributesQbl05(Enum):
    """
    :cvar HOSP: Hospital Dialysis Unit
    :cvar SATL: Satellite Dialysis Unit
    :cvar HOME: Home Dialysis
    """
    HOSP = "HOSP"
    SATL = "SATL"
    HOME = "HOME"


class TreatmentEncounterType(Enum):
    """
    :cvar E: Emergency
    :cvar I: Inpatient
    :cvar N: N/A
    :cvar G: ?
    :cvar P: Pre-Admit
    :cvar S: ?
    :cvar R: Reoccuring Patient
    :cvar B: Obstetrics
    :cvar C: Commercial Account
    :cvar U: Unknown
    """
    E = "E"
    I = "I"
    N = "N"
    G = "G"
    P = "P"
    S = "S"
    R = "R"
    B = "B"
    C = "C"
    U = "U"


@dataclass
class Treatment:
    """
    :ivar encounter_number:
    :ivar encounter_type: General Encounter Type (PV1-2)
    :ivar from_time: Start of Treatment (TXT00)
    :ivar to_time: End of Treatment (TXT01)
    :ivar admitting_clinician: Responsible Clinician as a National
        Clinicial code where possible or other local code if not.
    :ivar health_care_facility: Treatment Centre (TXT20)
    :ivar admit_reason: Modality
    :ivar admission_source: Prior Main Renal Unit
    :ivar discharge_reason: Reason for Discharge
    :ivar discharge_location: Destination Main Renal Unit
    :ivar entered_at: National code for the hospital providing care -
        e.g. RXF01
    :ivar visit_description: Free text about the Treatment record.
    :ivar attributes:
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    encounter_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "EncounterNumber",
            "type": "Element",
            "namespace": "",
        }
    )
    encounter_type: Optional[TreatmentEncounterType] = field(
        default=None,
        metadata={
            "name": "EncounterType",
            "type": "Element",
            "namespace": "",
        }
    )
    from_time: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "FromTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    to_time: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "ToTime",
            "type": "Element",
            "namespace": "",
        }
    )
    admitting_clinician: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "AdmittingClinician",
            "type": "Element",
            "namespace": "",
        }
    )
    health_care_facility: Optional[Location] = field(
        default=None,
        metadata={
            "name": "HealthCareFacility",
            "type": "Element",
            "namespace": "",
        }
    )
    admit_reason: Optional[CfRr7Treatment] = field(
        default=None,
        metadata={
            "name": "AdmitReason",
            "type": "Element",
            "namespace": "",
        }
    )
    admission_source: Optional[Location] = field(
        default=None,
        metadata={
            "name": "AdmissionSource",
            "type": "Element",
            "namespace": "",
        }
    )
    discharge_reason: Optional[CfRr7Discharge] = field(
        default=None,
        metadata={
            "name": "DischargeReason",
            "type": "Element",
            "namespace": "",
        }
    )
    discharge_location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "DischargeLocation",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_at: Optional[Location] = field(
        default=None,
        metadata={
            "name": "EnteredAt",
            "type": "Element",
            "namespace": "",
        }
    )
    visit_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "VisitDescription",
            "type": "Element",
            "namespace": "",
        }
    )
    attributes: Optional["Treatment.Attributes"] = field(
        default=None,
        metadata={
            "name": "Attributes",
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

    @dataclass
    class Attributes:
        """
        :ivar hdp01: Times Per Week
        :ivar hdp02: Time Dialysed in Minutes
        :ivar hdp03: Blood Flow Rate
        :ivar hdp04: Sodium in Dialysate
        :ivar qbl05: HD Treatment Location (RR8)
        :ivar qbl06: HD Shared Care (RR21)
        :ivar qbl07: Patient Participation
        :ivar erf61: Assessed for suitability for Transplant by start of
            Dialysis Date. This should only be supplied for the First
            RRT Treatment. (RR13)
        :ivar pat35: Date of referral to renal team (i.e. date letter
            received)
        """
        hdp01: Optional[int] = field(
            default=None,
            metadata={
                "name": "HDP01",
                "type": "Element",
                "namespace": "",
            }
        )
        hdp02: Optional[int] = field(
            default=None,
            metadata={
                "name": "HDP02",
                "type": "Element",
                "namespace": "",
            }
        )
        hdp03: Optional[int] = field(
            default=None,
            metadata={
                "name": "HDP03",
                "type": "Element",
                "namespace": "",
            }
        )
        hdp04: Optional[int] = field(
            default=None,
            metadata={
                "name": "HDP04",
                "type": "Element",
                "namespace": "",
            }
        )
        qbl05: Optional[AttributesQbl05] = field(
            default=None,
            metadata={
                "name": "QBL05",
                "type": "Element",
                "namespace": "",
            }
        )
        qbl06: Optional[str] = field(
            default=None,
            metadata={
                "name": "QBL06",
                "type": "Element",
                "namespace": "",
            }
        )
        qbl07: Optional[str] = field(
            default=None,
            metadata={
                "name": "QBL07",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N|U",
            }
        )
        erf61: Optional[AttributesErf61] = field(
            default=None,
            metadata={
                "name": "ERF61",
                "type": "Element",
                "namespace": "",
            }
        )
        pat35: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "PAT35",
                "type": "Element",
                "namespace": "",
            }
        )
