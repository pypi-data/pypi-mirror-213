from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.procedures.procedure import Procedure
from ukrdc_xsdata.ukrdc.types.gender import Gender
from ukrdc_xsdata.ukrdc.types.nv_rr14 import NvRr14

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AttributesTra65(Enum):
    """
    :cvar VALUE_10: Hyperacute Rejection
    :cvar VALUE_11: Non-Viable Transplant Kidney
    :cvar VALUE_12: Primary Non-Function of Transplant Kidney
    :cvar VALUE_13: Acute Rejection
    :cvar VALUE_14: Chronic Allograft Nephropathy
    :cvar VALUE_15: Rejection following withdrawal of immunosuppression
        - non Medical Reason
    :cvar VALUE_16: Rejection following withdrawal of immunosuppression
        - Medical Reason
    """
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"


class AttributesTra77(Enum):
    DBD = "DBD"
    DCD = "DCD"
    LIVE = "LIVE"


@dataclass
class TransplantProcedure(Procedure):
    attributes: Optional["TransplantProcedure.Attributes"] = field(
        default=None,
        metadata={
            "name": "Attributes",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class Attributes:
        """
        :ivar tra64: Failure Date
        :ivar tra65: Cause of Failure (RR10)
        :ivar tra66: Description of Failure
        :ivar tra69: Date graft nephrectomy if graft failed
        :ivar tra76: Graft Type (RR24)
        :ivar tra77: NHSBT Type
        :ivar tra78: rCMV - Recipient CMV status at transplant
        :ivar tra79: rEBV - Recipient EBV status at transplant
        :ivar tra80: Donor age
        :ivar tra8_a: Donor sex
        :ivar tra81: rCMV - Donor CMV status at transplant
        :ivar tra82: rEBV - Donor CMV status at transplant
        :ivar tra83: Mismatch A
        :ivar tra84: Mismatch B
        :ivar tra85: Mismatch DR
        :ivar tra86: ABO compatible
        :ivar tra87: Plasma exchange
        :ivar tra88: Immunoadsorption
        :ivar tra89: Rituximab
        :ivar tra90: IV immunoglobulin
        :ivar tra91: Cold ischaemic time in hours
        :ivar tra92: Primary function
        :ivar tra93: Anticoagulation (RR15)
        :ivar tra94: CMV prophylaxis (RR16)
        :ivar tra95: Pneumocystis prophylaxis (RR17)
        :ivar tra96: Functioning
        :ivar tra97: Other organ transplanted simultaneously 1 (RR14)
        :ivar tra98: Other organ transplanted simultaneously 2 (RR14)
        """
        tra64: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "TRA64",
                "type": "Element",
                "namespace": "",
            }
        )
        tra65: Optional[AttributesTra65] = field(
            default=None,
            metadata={
                "name": "TRA65",
                "type": "Element",
                "namespace": "",
            }
        )
        tra66: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA66",
                "type": "Element",
                "namespace": "",
            }
        )
        tra69: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "TRA69",
                "type": "Element",
                "namespace": "",
            }
        )
        tra76: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA76",
                "type": "Element",
                "namespace": "",
            }
        )
        tra77: Optional[AttributesTra77] = field(
            default=None,
            metadata={
                "name": "TRA77",
                "type": "Element",
                "namespace": "",
            }
        )
        tra78: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA78",
                "type": "Element",
                "namespace": "",
                "pattern": r"NEG|POS|UK",
            }
        )
        tra79: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA79",
                "type": "Element",
                "namespace": "",
                "pattern": r"NEG|POS|UK",
            }
        )
        tra80: Optional[int] = field(
            default=None,
            metadata={
                "name": "TRA80",
                "type": "Element",
                "namespace": "",
            }
        )
        tra8_a: Optional[Gender] = field(
            default=None,
            metadata={
                "name": "TRA8A",
                "type": "Element",
                "namespace": "",
            }
        )
        tra81: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA81",
                "type": "Element",
                "namespace": "",
                "pattern": r"NEG|POS|UK",
            }
        )
        tra82: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA82",
                "type": "Element",
                "namespace": "",
                "pattern": r"NEG|POS|UK",
            }
        )
        tra83: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA83",
                "type": "Element",
                "namespace": "",
            }
        )
        tra84: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA84",
                "type": "Element",
                "namespace": "",
            }
        )
        tra85: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA85",
                "type": "Element",
                "namespace": "",
            }
        )
        tra86: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA86",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra87: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA87",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra88: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA88",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra89: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA89",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra90: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA90",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra91: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA91",
                "type": "Element",
                "namespace": "",
            }
        )
        tra92: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA92",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra93: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA93",
                "type": "Element",
                "namespace": "",
            }
        )
        tra94: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA94",
                "type": "Element",
                "namespace": "",
            }
        )
        tra95: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA95",
                "type": "Element",
                "namespace": "",
            }
        )
        tra96: Optional[str] = field(
            default=None,
            metadata={
                "name": "TRA96",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        tra97: Optional[NvRr14] = field(
            default=None,
            metadata={
                "name": "TRA97",
                "type": "Element",
                "namespace": "",
            }
        )
        tra98: Optional[NvRr14] = field(
            default=None,
            metadata={
                "name": "TRA98",
                "type": "Element",
                "namespace": "",
            }
        )
