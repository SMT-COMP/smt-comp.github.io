from __future__ import annotations

import hashlib
import re
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, RootModel, model_validator
from pydantic.networks import HttpUrl, validate_email


class NameEmail(BaseModel):
    """
    Name and valide email "name <email>"
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                "Jane Smith <jane.smith@edu.world>",
            ]
        }
    }

    name: str
    email: str

    @model_validator(mode="before")
    @classmethod
    def split_email(cls, data: NameEmail | str) -> Any:
        if isinstance(data, str):
            name, email = validate_email(data)
            return {"name": name, "email": email}
        return data

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Hash(BaseModel, extra="forbid"):
    sha256: str | None = None
    sha512: str | None = None

    @model_validator(mode="after")
    def check_one_set(self) -> Hash:
        if self.sha256 is None and self.sha512 is None:
            raise ValueError("one hash type is required")
        return self


class Contributor(BaseModel, extra="forbid"):
    """
    Contributors in the developement of the solver. If only name is provided,
    it can be directly given.
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                "Jane Smith",
                {
                    "name": "Jane Smith",
                    "website": "http://jane.smith.name",
                },
            ]
        }
    }

    name: str
    website: HttpUrl | None = None

    @model_validator(mode="before")
    @classmethod
    def name_is_default_field(cls, data: Any) -> Any:
        if isinstance(data, str):
            return {"name": data}
        return data


class SolverType(str, Enum):
    wrapped = "wrapped"
    derived = "derived"
    standalone = "Standalone"


# class RegexpTracks:


class Track(str, Enum):
    UnsatCore = "UnsatCore"
    SingleQuery = "SingleQuery"
    ProofExhibition = "ProofExhibition"
    ModelValidation = "ModelValidation"
    Incremental = "Incremental"
    Cloud = "Cloud"
    Parallel = "Parallel"


class Division(str, Enum):
    Arith = "Arith"
    Bitvec = "Bitvec"
    Equality = "Equality"
    Equality_LinearArith = "Equality+LinearArith"
    Equality_MachineArith = "Equality+MachineArith"
    Equality_NonLinearArith = "Equality+NonLinearArith"
    FPArith = "FPArith"
    QF_ADT_BitVec = "QF_ADT+BitVec"
    QF_ADT_LinArith = "QF_ADT+LinArith"
    QF_Bitvec = "QF_Bitvec"
    QF_Datatypes = "QF_Datatypes"
    QF_Equality = "QF_Equality"
    QF_Equality_Bitvec = "QF_Equality+Bitvec"
    QF_Equality_Bitvec_Arith = "QF_Equality+Bitvec+Arith"
    QF_Equality_LinearArith = "QF_Equality+LinearArith"
    QF_Equality_NonLinearArith = "QF_Equality+NonLinearArith"
    QF_FPArith = "QF_FPArith"
    QF_LinearIntArith = "QF_LinearIntArith"
    QF_LinearRealArith = "QF_LinearRealArith"
    QF_NonLinearIntArith = "QF_NonLinearIntArith"
    QF_NonLinearRealArith = "QF_NonLinearRealArith"
    QF_Strings = "QF_Strings"


class Logic(str, Enum):
    ABV = "ABV"
    ABVFP = "ABVFP"
    ABVFPLRA = "ABVFPLRA"
    ALIA = "ALIA"
    ANIA = "ANIA"
    AUFBV = "AUFBV"
    AUFBVDTLIA = "AUFBVDTLIA"
    AUFBVDTNIA = "AUFBVDTNIA"
    AUFBVDTNIRA = "AUFBVDTNIRA"
    AUFBVFP = "AUFBVFP"
    AUFDTLIA = "AUFDTLIA"
    AUFDTLIRA = "AUFDTLIRA"
    AUFDTNIRA = "AUFDTNIRA"
    AUFFPDTNIRA = "AUFFPDTNIRA"
    AUFLIA = "AUFLIA"
    AUFLIRA = "AUFLIRA"
    AUFNIA = "AUFNIA"
    AUFNIRA = "AUFNIRA"
    BV = "BV"
    BVFP = "BVFP"
    BVFPLRA = "BVFPLRA"
    FP = "FP"
    FPLRA = "FPLRA"
    LIA = "LIA"
    LRA = "LRA"
    NIA = "NIA"
    NRA = "NRA"
    QF_ABV = "QF_ABV"
    QF_ABVFP = "QF_ABVFP"
    QF_ABVFPLRA = "QF_ABVFPLRA"
    QF_ALIA = "QF_ALIA"
    QF_ANIA = "QF_ANIA"
    QF_AUFBV = "QF_AUFBV"
    QF_AUFBVFP = "QF_AUFBVFP"
    QF_AUFBVLIA = "QF_AUFBVLIA"
    QF_AUFBVNIA = "QF_AUFBVNIA"
    QF_AUFLIA = "QF_AUFLIA"
    QF_AUFNIA = "QF_AUFNIA"
    QF_AX = "QF_AX"
    QF_BV = "QF_BV"
    QF_BVFP = "QF_BVFP"
    QF_BVFPLRA = "QF_BVFPLRA"
    QF_DT = "QF_DT"
    QF_FP = "QF_FP"
    QF_FPLRA = "QF_FPLRA"
    QF_IDL = "QF_IDL"
    QF_LIA = "QF_LIA"
    QF_LIRA = "QF_LIRA"
    QF_LRA = "QF_LRA"
    QF_NIA = "QF_NIA"
    QF_NIRA = "QF_NIRA"
    QF_NRA = "QF_NRA"
    QF_RDL = "QF_RDL"
    QF_S = "QF_S"
    QF_SLIA = "QF_SLIA"
    QF_SNIA = "QF_SNIA"
    QF_UF = "QF_UF"
    QF_UFBV = "QF_UFBV"
    QF_UFBVDT = "QF_UFBVDT"
    QF_UFBVLIA = "QF_UFBVLIA"
    QF_UFDT = "QF_UFDT"
    QF_UFDTLIA = "QF_UFDTLIA"
    QF_UFDTLIRA = "QF_UFDTLIRA"
    QF_UFDTNIA = "QF_UFDTNIA"
    QF_UFFP = "QF_UFFP"
    QF_UFFPDTNIRA = "QF_UFFPDTNIRA"
    QF_UFIDL = "QF_UFIDL"
    QF_UFLIA = "QF_UFLIA"
    QF_UFLRA = "QF_UFLRA"
    QF_UFNIA = "QF_UFNIA"
    QF_UFNRA = "QF_UFNRA"
    UF = "UF"
    UFBV = "UFBV"
    UFBVDT = "UFBVDT"
    UFBVFP = "UFBVFP"
    UFBVLIA = "UFBVLIA"
    UFDT = "UFDT"
    UFDTLIA = "UFDTLIA"
    UFDTLIRA = "UFDTLIRA"
    UFDTNIA = "UFDTNIA"
    UFDTNIRA = "UFDTNIRA"
    UFFPDTNIRA = "UFFPDTNIRA"
    UFIDL = "UFIDL"
    UFLIA = "UFLIA"
    UFLRA = "UFLRA"
    UFNIA = "UFNIA"
    UFNRA = "UFNRA"


tracks: dict[Track, dict[Division, set[Logic]]] = {
    Track.SingleQuery: {
        Division.QF_Datatypes: {
            Logic.QF_DT,
            Logic.QF_UFDT,
        },
        Division.QF_Equality: {
            Logic.QF_AX,
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_UFDTLIA,
            Logic.QF_UFDTLIRA,
            Logic.QF_UFIDL,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_AUFNIA,
            Logic.QF_UFDTNIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBV,
            Logic.QF_UFBVDT,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_IDL,
            Logic.QF_LIA,
            Logic.QF_LIRA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
            Logic.QF_RDL,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_AUFBVFP,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_FPLRA,
            Logic.QF_UFFP,
            Logic.QF_UFFPDTNIRA,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
            Logic.QF_NIRA,
        },
        Division.QF_NonLinearRealArith: {
            Logic.QF_NRA,
        },
        Division.QF_Strings: {
            Logic.QF_S,
            Logic.QF_SLIA,
            Logic.QF_SNIA,
        },
        Division.Equality: {
            Logic.UF,
            Logic.UFDT,
        },
        Division.Equality_LinearArith: {
            Logic.ALIA,
            Logic.AUFDTLIA,
            Logic.AUFDTLIRA,
            Logic.AUFLIA,
            Logic.AUFLIRA,
            Logic.UFDTLIA,
            Logic.UFDTLIRA,
            Logic.UFIDL,
            Logic.UFLIA,
            Logic.UFLRA,
        },
        Division.Equality_MachineArith: {
            Logic.ABV,
            Logic.ABVFP,
            Logic.ABVFPLRA,
            Logic.AUFBV,
            Logic.AUFBVDTLIA,
            Logic.AUFBVDTNIA,
            Logic.AUFBVDTNIRA,
            Logic.AUFBVFP,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVFP,
            Logic.UFBVLIA,
            Logic.UFFPDTNIRA,
        },
        Division.Equality_NonLinearArith: {
            Logic.ANIA,
            Logic.AUFDTNIRA,
            Logic.AUFNIA,
            Logic.AUFNIRA,
            Logic.UFDTNIA,
            Logic.UFDTNIRA,
            Logic.UFNIA,
        },
        Division.Arith: {
            Logic.LIA,
            Logic.LRA,
            Logic.NIA,
            Logic.NRA,
        },
        Division.Bitvec: {
            Logic.BV,
        },
        Division.FPArith: {
            Logic.BVFP,
            Logic.BVFPLRA,
            Logic.FP,
            Logic.FPLRA,
        },
    },
    Track.Incremental: {
        Division.QF_Equality: {
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBV,
        },
        Division.QF_Equality_Bitvec_Arith: {
            Logic.QF_AUFBVLIA,
            Logic.QF_AUFBVNIA,
            Logic.QF_UFBVLIA,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_LIA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_UFFP,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
        },
        Division.Equality: {
            Logic.UF,
        },
        Division.Equality_LinearArith: {
            Logic.ALIA,
            Logic.UFLRA,
        },
        Division.Equality_MachineArith: {
            Logic.ABVFPLRA,
        },
        Division.Equality_NonLinearArith: {
            Logic.ANIA,
            Logic.AUFNIRA,
            Logic.UFDTNIA,
            Logic.UFNIA,
            Logic.UFNRA,
        },
        Division.Arith: {
            Logic.LIA,
            Logic.LRA,
        },
        Division.Bitvec: {
            Logic.BV,
        },
        Division.FPArith: {
            Logic.BVFP,
            Logic.BVFPLRA,
        },
    },
    Track.UnsatCore: {
        Division.QF_Datatypes: {
            Logic.QF_DT,
            Logic.QF_UFDT,
        },
        Division.QF_Equality: {
            Logic.QF_AX,
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_UFDTLIA,
            Logic.QF_UFDTLIRA,
            Logic.QF_UFIDL,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_AUFNIA,
            Logic.QF_UFDTNIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBV,
            Logic.QF_UFBVDT,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_IDL,
            Logic.QF_LIA,
            Logic.QF_LIRA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
            Logic.QF_RDL,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_AUFBVFP,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_FPLRA,
            Logic.QF_UFFP,
            Logic.QF_UFFPDTNIRA,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
            Logic.QF_NIRA,
        },
        Division.QF_NonLinearRealArith: {
            Logic.QF_NRA,
        },
        Division.QF_Strings: {
            Logic.QF_S,
            Logic.QF_SLIA,
            Logic.QF_SNIA,
        },
        Division.Equality: {
            Logic.UF,
            Logic.UFDT,
        },
        Division.Equality_LinearArith: {
            Logic.ALIA,
            Logic.AUFDTLIA,
            Logic.AUFDTLIRA,
            Logic.AUFLIA,
            Logic.AUFLIRA,
            Logic.UFDTLIA,
            Logic.UFDTLIRA,
            Logic.UFIDL,
            Logic.UFLIA,
            Logic.UFLRA,
        },
        Division.Equality_MachineArith: {
            Logic.ABV,
            Logic.ABVFP,
            Logic.ABVFPLRA,
            Logic.AUFBV,
            Logic.AUFBVDTLIA,
            Logic.AUFBVDTNIA,
            Logic.AUFBVDTNIRA,
            Logic.AUFBVFP,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVFP,
            Logic.UFBVLIA,
            Logic.UFFPDTNIRA,
        },
        Division.Equality_NonLinearArith: {
            Logic.ANIA,
            Logic.AUFDTNIRA,
            Logic.AUFNIA,
            Logic.AUFNIRA,
            Logic.UFDTNIA,
            Logic.UFDTNIRA,
            Logic.UFNIA,
        },
        Division.Arith: {
            Logic.LIA,
            Logic.LRA,
            Logic.NIA,
            Logic.NRA,
        },
        Division.Bitvec: {
            Logic.BV,
        },
        Division.FPArith: {
            Logic.BVFP,
            Logic.BVFPLRA,
            Logic.FP,
            Logic.FPLRA,
        },
    },
    Track.ModelValidation: {
        Division.QF_Datatypes: {
            Logic.QF_DT,
            Logic.QF_UFDT,
        },
        Division.QF_Equality: {
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_UFIDL,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_AUFNIA,
            Logic.QF_UFDTNIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_UFBV,
        },
        Division.QF_ADT_BitVec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBVDT,
        },
        Division.QF_ADT_LinArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_AX,
            Logic.QF_UFDTLIA,
            Logic.QF_UFDTLIRA,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_IDL,
            Logic.QF_LIA,
            Logic.QF_LIRA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
            Logic.QF_RDL,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_AUFBVFP,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_FPLRA,
            Logic.QF_UFFP,
            Logic.QF_UFFPDTNIRA,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
            Logic.QF_NIRA,
        },
        Division.QF_NonLinearRealArith: {
            Logic.QF_NRA,
        },
    },
    Track.ProofExhibition: {
        Division.QF_Datatypes: {
            Logic.QF_DT,
            Logic.QF_UFDT,
        },
        Division.QF_Equality: {
            Logic.QF_AX,
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_UFDTLIA,
            Logic.QF_UFDTLIRA,
            Logic.QF_UFIDL,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_AUFNIA,
            Logic.QF_UFDTNIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBV,
            Logic.QF_UFBVDT,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_IDL,
            Logic.QF_LIA,
            Logic.QF_LIRA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
            Logic.QF_RDL,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_AUFBVFP,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_FPLRA,
            Logic.QF_UFFP,
            Logic.QF_UFFPDTNIRA,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
            Logic.QF_NIRA,
        },
        Division.QF_NonLinearRealArith: {
            Logic.QF_NRA,
        },
        Division.QF_Strings: {
            Logic.QF_S,
            Logic.QF_SLIA,
            Logic.QF_SNIA,
        },
        Division.Equality: {
            Logic.UF,
            Logic.UFDT,
        },
        Division.Equality_LinearArith: {
            Logic.ALIA,
            Logic.AUFDTLIA,
            Logic.AUFDTLIRA,
            Logic.AUFLIA,
            Logic.AUFLIRA,
            Logic.UFDTLIA,
            Logic.UFDTLIRA,
            Logic.UFIDL,
            Logic.UFLIA,
            Logic.UFLRA,
        },
        Division.Equality_MachineArith: {
            Logic.ABV,
            Logic.ABVFP,
            Logic.ABVFPLRA,
            Logic.AUFBV,
            Logic.AUFBVDTLIA,
            Logic.AUFBVDTNIA,
            Logic.AUFBVDTNIRA,
            Logic.AUFBVFP,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVFP,
            Logic.UFBVLIA,
            Logic.UFFPDTNIRA,
        },
        Division.Equality_NonLinearArith: {
            Logic.ANIA,
            Logic.AUFDTNIRA,
            Logic.AUFNIA,
            Logic.AUFNIRA,
            Logic.UFDTNIA,
            Logic.UFDTNIRA,
            Logic.UFNIA,
        },
        Division.Arith: {
            Logic.LIA,
            Logic.LRA,
            Logic.NIA,
            Logic.NRA,
        },
        Division.Bitvec: {
            Logic.BV,
        },
        Division.FPArith: {
            Logic.BVFP,
            Logic.BVFPLRA,
            Logic.FP,
            Logic.FPLRA,
        },
    },
    Track.Cloud: {
        Division.QF_Datatypes: {
            Logic.QF_DT,
            Logic.QF_UFDT,
        },
        Division.QF_Equality: {
            Logic.QF_AX,
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_UFDTLIA,
            Logic.QF_UFDTLIRA,
            Logic.QF_UFIDL,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_AUFNIA,
            Logic.QF_UFDTNIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBV,
            Logic.QF_UFBVDT,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_IDL,
            Logic.QF_LIA,
            Logic.QF_LIRA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
            Logic.QF_RDL,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_AUFBVFP,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_FPLRA,
            Logic.QF_UFFP,
            Logic.QF_UFFPDTNIRA,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
            Logic.QF_NIRA,
        },
        Division.QF_NonLinearRealArith: {
            Logic.QF_NRA,
        },
        Division.QF_Strings: {
            Logic.QF_S,
            Logic.QF_SLIA,
            Logic.QF_SNIA,
        },
        Division.Equality: {
            Logic.UF,
            Logic.UFDT,
        },
        Division.Equality_LinearArith: {
            Logic.ALIA,
            Logic.AUFDTLIA,
            Logic.AUFDTLIRA,
            Logic.AUFLIA,
            Logic.AUFLIRA,
            Logic.UFDTLIA,
            Logic.UFDTLIRA,
            Logic.UFIDL,
            Logic.UFLIA,
            Logic.UFLRA,
        },
        Division.Equality_MachineArith: {
            Logic.ABV,
            Logic.ABVFP,
            Logic.ABVFPLRA,
            Logic.AUFBV,
            Logic.AUFBVDTLIA,
            Logic.AUFBVDTNIA,
            Logic.AUFBVDTNIRA,
            Logic.AUFBVFP,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVFP,
            Logic.UFBVLIA,
            Logic.UFFPDTNIRA,
        },
        Division.Equality_NonLinearArith: {
            Logic.ANIA,
            Logic.AUFDTNIRA,
            Logic.AUFNIA,
            Logic.AUFNIRA,
            Logic.UFDTNIA,
            Logic.UFDTNIRA,
            Logic.UFNIA,
        },
        Division.Arith: {
            Logic.LIA,
            Logic.LRA,
            Logic.NIA,
            Logic.NRA,
        },
        Division.Bitvec: {
            Logic.BV,
        },
        Division.FPArith: {
            Logic.BVFP,
            Logic.BVFPLRA,
            Logic.FP,
            Logic.FPLRA,
        },
    },
    Track.Parallel: {
        Division.QF_Datatypes: {
            Logic.QF_DT,
            Logic.QF_UFDT,
        },
        Division.QF_Equality: {
            Logic.QF_AX,
            Logic.QF_UF,
        },
        Division.QF_Equality_LinearArith: {
            Logic.QF_ALIA,
            Logic.QF_AUFLIA,
            Logic.QF_UFDTLIA,
            Logic.QF_UFDTLIRA,
            Logic.QF_UFIDL,
            Logic.QF_UFLIA,
            Logic.QF_UFLRA,
        },
        Division.QF_Equality_NonLinearArith: {
            Logic.QF_ANIA,
            Logic.QF_AUFNIA,
            Logic.QF_UFDTNIA,
            Logic.QF_UFNIA,
            Logic.QF_UFNRA,
        },
        Division.QF_Equality_Bitvec: {
            Logic.QF_ABV,
            Logic.QF_AUFBV,
            Logic.QF_UFBV,
            Logic.QF_UFBVDT,
        },
        Division.QF_LinearIntArith: {
            Logic.QF_IDL,
            Logic.QF_LIA,
            Logic.QF_LIRA,
        },
        Division.QF_LinearRealArith: {
            Logic.QF_LRA,
            Logic.QF_RDL,
        },
        Division.QF_Bitvec: {
            Logic.QF_BV,
        },
        Division.QF_FPArith: {
            Logic.QF_ABVFP,
            Logic.QF_ABVFPLRA,
            Logic.QF_AUFBVFP,
            Logic.QF_BVFP,
            Logic.QF_BVFPLRA,
            Logic.QF_FP,
            Logic.QF_FPLRA,
            Logic.QF_UFFP,
            Logic.QF_UFFPDTNIRA,
        },
        Division.QF_NonLinearIntArith: {
            Logic.QF_NIA,
            Logic.QF_NIRA,
        },
        Division.QF_NonLinearRealArith: {
            Logic.QF_NRA,
        },
        Division.QF_Strings: {
            Logic.QF_S,
            Logic.QF_SLIA,
            Logic.QF_SNIA,
        },
        Division.Equality: {
            Logic.UF,
            Logic.UFDT,
        },
        Division.Equality_LinearArith: {
            Logic.ALIA,
            Logic.AUFDTLIA,
            Logic.AUFDTLIRA,
            Logic.AUFLIA,
            Logic.AUFLIRA,
            Logic.UFDTLIA,
            Logic.UFDTLIRA,
            Logic.UFIDL,
            Logic.UFLIA,
            Logic.UFLRA,
        },
        Division.Equality_MachineArith: {
            Logic.ABV,
            Logic.ABVFP,
            Logic.ABVFPLRA,
            Logic.AUFBV,
            Logic.AUFBVDTLIA,
            Logic.AUFBVDTNIA,
            Logic.AUFBVDTNIRA,
            Logic.AUFBVFP,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVFP,
            Logic.UFBVLIA,
            Logic.UFFPDTNIRA,
        },
        Division.Equality_NonLinearArith: {
            Logic.ANIA,
            Logic.AUFDTNIRA,
            Logic.AUFNIA,
            Logic.AUFNIRA,
            Logic.UFDTNIA,
            Logic.UFDTNIRA,
            Logic.UFNIA,
        },
        Division.Arith: {
            Logic.LIA,
            Logic.LRA,
            Logic.NIA,
            Logic.NRA,
        },
        Division.Bitvec: {
            Logic.BV,
        },
        Division.FPArith: {
            Logic.BVFP,
            Logic.BVFPLRA,
            Logic.FP,
            Logic.FPLRA,
        },
    },
}


class Logics(RootModel):
    root: list[Logic]

    @model_validator(mode="before")
    @classmethod
    def name_is_default_field(cls, data: Any) -> Any:
        if isinstance(data, str):
            return cls.logics_from_regexp(data)
        return data

    @classmethod
    def from_regexp(cls, data: str) -> Logics:
        return Logics(root=cls.logics_from_regexp(data))

    @classmethod
    def logics_from_regexp(cls, data: str) -> list[Logic]:
        logics = []
        r = re.compile(data)
        for logic in Logic:
            if r.fullmatch(logic):
                logics.append(logic)
        return logics


class Archive(BaseModel):
    url: HttpUrl
    h: Hash | None = None

    def uniq_id(self) -> str:
        return hashlib.sha256(str(self.url).encode()).hexdigest()

    def path(self) -> Path:
        return Path(self.uniq_id())


class Command(BaseModel, extra="forbid"):
    binary: str
    arguments: list[str] = []

    @model_validator(mode="before")
    @classmethod
    def split_command(cls, data: Any) -> Any:
        if isinstance(data, list):
            if len(data) < 1:
                raise ValueError("Command must be a non empty list")
            return {"binary": data[0], "arguments": data[1:]}
        return data

    def uniq_id(self, name: str, archive: Archive) -> str:
        data = [name, str(archive.url), self.binary, *self.arguments]
        h = hashlib.sha256(*[s.encode() for s in data])
        return h.hexdigest()


class Participation(BaseModel, extra="forbid"):
    tracks: list[Track]
    logics: Logics = Logics(root=[])
    divisions: list[Division] = []
    archive: Archive | None = None
    command: Command | None = None
    experimental: bool = False

    def get(self, d: None | dict[Track, dict[Division, set[Logic]]] = None) -> dict[Track, dict[Division, set[Logic]]]:
        if d is None:
            d = {}
        for track in self.tracks:
            divs = d.setdefault(track, {})
            for division in self.divisions:
                logics: set[Logic] = divs.setdefault(division, set())
                logics.update(tracks[track][division])
            for logic in self.logics.root:
                for div, logics in tracks[track].items():
                    if logic in logics:
                        logics = divs.setdefault(div, set())
                        logics.add(logic)
        return d


class Participations(RootModel):
    root: list[Participation]

    def get_divisions(self, track: Track) -> list[Division]:
        """ " Return the divisions in which the solver participates"""
        return []  # TODO

    def get_logics(self, track: Track) -> list[Logic]:
        """ " Return the logics in which the solver participates"""
        return []  # TODO

    def get(self, d: None | dict[Track, dict[Division, set[Logic]]] = None) -> dict[Track, dict[Division, set[Logic]]]:
        if d is None:
            d = {}
        for p in self.root:
            p.get(d)
        return d


class Submission(BaseModel, extra="forbid"):
    name: str
    contributors: list[Contributor] = Field(min_length=1)
    contacts: list[NameEmail] = Field(min_length=1)
    archive: Archive | None = None
    command: Command | None = None
    website: HttpUrl
    system_description: HttpUrl
    solver_type: SolverType
    participations: Participations

    @model_validator(mode="after")
    def check_archive(self) -> Submission:
        if self.archive is None and not all(p.archive for p in self.participations.root):
            raise ValueError("Field archive is needed in all participations if not present at the root")
        if self.command is None and not all(p.command for p in self.participations.root):
            raise ValueError("Field command is needed in all participations if not present at the root")
        return self

    def uniq_id(self) -> str:
        return hashlib.sha256(self.name.encode()).hexdigest()


default = {"timelimit_s": 60, "memlimit_M": 1024 * 20, "cpuCores": 4}