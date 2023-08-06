from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate
from ukrdc_xsdata.ukrdc.procedures.procedure import Procedure

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AttributesQhd20(Enum):
    """
    :cvar NLN: Non-Tunneled Line
    :cvar TLN: Tunneled Line
    :cvar AVF: Arteriovenous Fistula
    :cvar AVG: Arteriovenous Graft
    :cvar VLP: Vein Loop
    :cvar PDC: PD Catherer
    :cvar PDE: PD Embedded Catherer
    :cvar PDT: PD Catherer Temp
    :cvar HER: HeRO Graft
    """
    NLN = "NLN"
    TLN = "TLN"
    AVF = "AVF"
    AVG = "AVG"
    VLP = "VLP"
    PDC = "PDC"
    PDE = "PDE"
    PDT = "PDT"
    HER = "HER"


class AttributesQhd21(Enum):
    """
    :cvar BB: Brachio-Basilic
    :cvar BC: Brachio-Cephalic
    :cvar LA: Axillary Vein Line
    :cvar LF: Femoral Vein Line
    :cvar LJ: Intenal Jugular Line
    :cvar LS: Subclavian Line
    :cvar PS: Popliteal-Long Saphenous
    :cvar RC: Radio-Cephalic Wrist
    :cvar RU: Radio-Ulnar
    :cvar SB: Radio-Cephalic Snuff Box
    :cvar TB: Brachio-Basilic and Transposition
    :cvar TS: Popliteal-Long Saphenous and Transposition
    :cvar UA: Ankle
    :cvar UC: Ulna-Cephalic
    :cvar UF: Forearm NOS
    :cvar UO: Other
    :cvar UT: Thigh NOS
    """
    BB = "BB"
    BC = "BC"
    LA = "LA"
    LF = "LF"
    LJ = "LJ"
    LS = "LS"
    PS = "PS"
    RC = "RC"
    RU = "RU"
    SB = "SB"
    TB = "TB"
    TS = "TS"
    UA = "UA"
    UC = "UC"
    UF = "UF"
    UO = "UO"
    UT = "UT"


class AttributesQhd33(Enum):
    """
    :cvar L: Rope Ladder
    :cvar B: Button Hole
    :cvar U: Unknown
    """
    L = "L"
    B = "B"
    U = "U"


@dataclass
class DialysisSession(Procedure):
    attributes: Optional["DialysisSession.Attributes"] = field(
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
        :ivar qhd19: Symptomatic hypotension
        :ivar qhd20: Vascular Access Used (RR02)
        :ivar qhd21: Vascular Access Site (RR41)
        :ivar qhd22: Access in two sites simultaneously
        :ivar qhd30: Blood Flow Rate
        :ivar qhd31: Time Dialysed in Minutes
        :ivar qhd32: Sodium in Dialysate
        :ivar qhd33: Needling Method (RR50)
        """
        qhd19: Optional[str] = field(
            default=None,
            metadata={
                "name": "QHD19",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        qhd20: Optional[AttributesQhd20] = field(
            default=None,
            metadata={
                "name": "QHD20",
                "type": "Element",
                "namespace": "",
            }
        )
        qhd21: Optional[AttributesQhd21] = field(
            default=None,
            metadata={
                "name": "QHD21",
                "type": "Element",
                "namespace": "",
            }
        )
        qhd22: Optional[str] = field(
            default=None,
            metadata={
                "name": "QHD22",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        qhd30: Optional[int] = field(
            default=None,
            metadata={
                "name": "QHD30",
                "type": "Element",
                "namespace": "",
            }
        )
        qhd31: Optional[int] = field(
            default=None,
            metadata={
                "name": "QHD31",
                "type": "Element",
                "namespace": "",
            }
        )
        qhd32: Optional[int] = field(
            default=None,
            metadata={
                "name": "QHD32",
                "type": "Element",
                "namespace": "",
            }
        )
        qhd33: Optional[AttributesQhd33] = field(
            default=None,
            metadata={
                "name": "QHD33",
                "type": "Element",
                "namespace": "",
            }
        )


@dataclass
class DialysisSessions:
    dialysis_session: List[DialysisSession] = field(
        default_factory=list,
        metadata={
            "name": "DialysisSession",
            "type": "Element",
            "namespace": "",
        }
    )
    start: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    stop: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
