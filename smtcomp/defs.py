from __future__ import annotations

import functools
import hashlib
import re
from enum import Enum
from pathlib import Path, PurePath
from typing import Any, Dict, cast, Optional, Iterable, TypeVar, Self, ClassVar, Union

from pydantic import BaseModel, Field, RootModel, model_validator, ConfigDict
from pydantic.networks import HttpUrl, validate_email
from datetime import date
from rich import print

U = TypeVar("U")


class EnumAutoInt(Enum):
    """
    Normal enum with strings, but each enum is associated to an int
    """

    __ordered__: ClassVar[list[Self]]

    def __str__(self) -> str:
        return str(self.value)

    def __new__(cls, id: str) -> Self:
        obj: Self = object.__new__(cls)
        obj._value_ = id
        value = len(cls.__members__)
        obj.id = value
        if "__ordered__" not in cls.__dict__:
            cls.__ordered__: list[Self] = []
        cls.__ordered__.append(obj)
        return obj

    def __init__(self, id: str) -> None:
        self.id: int = self.id  # For Mypy

    def __int__(self) -> int:
        return self.id

    @classmethod
    def of_int(cls, id: int) -> Self:
        return cast(Self, cls.__ordered__[id])

    @classmethod
    def name_of_int(cls, id: int) -> str:
        return cls.__ordered__[id].name

    def __hash__(self) -> int:
        return self.id

    def __lt__(self, a: EnumAutoInt) -> bool:
        return self.id.__lt__(a.id)

    def __le__(self, a: EnumAutoInt) -> bool:
        return self.id.__le__(a.id)

    def __gt__(self, a: EnumAutoInt) -> bool:
        return self.id.__gt__(a.id)

    def __ge__(self, a: EnumAutoInt) -> bool:
        return self.id.__ge__(a.id)


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
    it can be directly given. UTF8 can be used.
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


class SolverType(EnumAutoInt):
    wrapped = "wrapped"
    derived = "derived"
    standalone = "Standalone"
    portfolio = "Portfolio"


class Status(EnumAutoInt):
    Unsat = "unsat"
    Sat = "sat"
    Unknown = "unknown"
    Incremental = "incremental"


class Answer(EnumAutoInt):
    Unsat = "unsat"
    Sat = "sat"
    Unknown = "unknown"
    Incremental = "incremental"
    OOM = "OutOfMemory"
    Timeout = "Timeout"
    ModelNotValidated = "ModelNotValidated"
    ModelUnsat = "ModelUnsat"
    ModelParsingError = "ModelParsingError"
    ModelPartialFunctionMissing = "ModelPartialFunctionMissing"
    ModelValidatorException = "ModelValidatorException"
    ModelValidatorBenchmarkStrictTyping = "ModelValidatorBenchmarkStrictTyping"
    ModelValidatorTimeout = "ModelValidatorTimeout"
    IncrementalError = "IncrementalError"
    """
    At least one wrong answer
    """
    UnsatCoreInvalidated = "UnsatCoreNotValidated"
    """
    More solver said sat than unsat
    """


class Track(EnumAutoInt):
    UnsatCore = "UnsatCore"
    SingleQuery = "SingleQuery"
    ProofExhibition = "ProofExhibition"
    ModelValidation = "ModelValidation"
    Incremental = "Incremental"
    Cloud = "Cloud"
    Parallel = "Parallel"
    UnsatCoreValidation = "UnsatCoreValidation"

    def short_cut(self: Track) -> str:
        match self:
            case Track.UnsatCore:
                return "uc"
            case Track.UnsatCoreValidation:
                return "ucv"
            case Track.SingleQuery:
                return "sq"
            case Track.ProofExhibition:
                return "pe"
            case Track.ModelValidation:
                return "mv"
            case Track.Incremental:
                return "inc"
            case Track.Cloud:
                return "cloud"
            case Track.Parallel:
                return "parallel"


class Division(EnumAutoInt):
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


class Logic(EnumAutoInt):
    ABV = "ABV"
    ABVFP = "ABVFP"
    ABVFPLRA = "ABVFPLRA"
    ALIA = "ALIA"
    ANIA = "ANIA"
    AUFBV = "AUFBV"
    AUFBVDTLIA = "AUFBVDTLIA"
    AUFBVDTNIA = "AUFBVDTNIA"
    AUFBVDTNIRA = "AUFBVDTNIRA"
    AUFBVFPDTNIRA = "AUFBVFPDTNIRA"
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
    QF_BVLRA = "QF_BVLRA"
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
    UFBVDTLIA = "UFBVDTLIA"
    UFBVDTNIA = "UFBVDTNIA"
    UFBVDTNIRA = "UFBVDTNIRA"
    UFBVFP = "UFBVFP"
    UFBVFPDTNIRA = "UFBVFPDTNIRA"
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
    UFNIRA = "UFNIRA"
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
            Logic.AUFBVFPDTNIRA,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVDTLIA,
            Logic.UFBVDTNIA,
            Logic.UFBVDTNIRA,
            Logic.UFBVFP,
            Logic.UFBVFPDTNIRA,
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
            Logic.UFNIRA,
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
            Logic.QF_BVLRA,
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
            Logic.AUFBVFPDTNIRA,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVDTLIA,
            Logic.UFBVDTNIA,
            Logic.UFBVDTNIRA,
            Logic.UFBVFP,
            Logic.UFBVFPDTNIRA,
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
            Logic.UFNIRA,
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
            Logic.AUFBVFPDTNIRA,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVDTLIA,
            Logic.UFBVDTNIA,
            Logic.UFBVDTNIRA,
            Logic.UFBVFP,
            Logic.UFBVFPDTNIRA,
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
            Logic.UFNIRA,
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
            Logic.AUFBVFPDTNIRA,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVDTLIA,
            Logic.UFBVDTNIA,
            Logic.UFBVDTNIRA,
            Logic.UFBVFP,
            Logic.UFBVFPDTNIRA,
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
            Logic.UFNIRA,
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
            Logic.AUFBVFPDTNIRA,
            Logic.AUFFPDTNIRA,
            Logic.UFBV,
            Logic.UFBVDT,
            Logic.UFBVDTLIA,
            Logic.UFBVDTNIA,
            Logic.UFBVDTNIRA,
            Logic.UFBVFP,
            Logic.UFBVFPDTNIRA,
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
            Logic.UFNIRA,
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


def logic_used_for_track(t: Track) -> set[Logic]:
    return functools.reduce(lambda x, y: x | y, tracks[t].values())


class Logics(RootModel):
    """
    Can be a list of logics or a regexp matched on all the existing logics
    """

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
            if r.fullmatch(str(logic)):
                logics.append(logic)
        return logics


class Archive(BaseModel):
    """
    The url must be record from http://zenodo.org for the final submission. So
    the hash is not required because zenodo records are immutable.

    The hash can be used if you want to be sure of the archive used during the
    test runs.
    """

    url: HttpUrl = Field(
        description="The url should be valid at the time of submission and during all the competition. The url should be at zenodo for the final submission."
    )
    h: Hash | None = None

    def uniq_id(self) -> str:
        return hashlib.sha256(str(self.url).encode()).hexdigest()

    def path(self) -> Path:
        return Path(self.uniq_id())

    def check_final(self) -> None:
        if self.url.host != "zenodo.org":
            raise ValueError("Final version should have its archive in zenodo")


class Command(BaseModel, extra="forbid"):
    """
    Command with its arguments to run after the extraction of the archive.

    The path are relative to the directory in which the archive is unpacked.

    The input file is added at the end of the list of arguments.

    Two forms are accepted, using a dictionnary (separate binary and arguments) or a list ([binary]+arguments).

    The command run in the given environment
     https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                ["relative_cmd", "default_command_line"],
                {"binary": "relative_cmd", "arguments": ["default_command_line"]},
            ]
        }
    }

    binary: str
    arguments: list[str] = []
    compa_starexec: bool = Field(default=False, description="Used only for internal tests")

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
        h = hashlib.sha256(" ".join(data).encode())
        return h.hexdigest()


class ParticipationCompleted(BaseModel, extra="forbid"):
    """Participation using the default value in the submission root"""

    tracks: dict[Track, dict[Division, set[Logic]]]
    archive: Archive
    command: Command
    experimental: bool


class Participation(BaseModel, extra="forbid"):
    """
    tracks: select the participation tracks
    divisions: add all the logics of those divisions in each track
    logics: add all the specified logics in each selected track it exists

    aws_repository should be used only in conjunction with Cloud and Parallel track

    archive and command should not be used with Cloud and Parallel track. They superseed the one given at the root.
    """

    tracks: list[Track]
    logics: Logics = Logics(root=[])
    divisions: list[Division] = []
    archive: Archive | None = None
    command: Command | None = None
    aws_repository: str | None = None
    experimental: bool = False

    @model_validator(mode="after")
    def check_archive(self) -> Participation:
        aws_track = {Track.Cloud, Track.Parallel}
        if self.aws_repository is None and not set(self.tracks).isdisjoint(aws_track):
            raise ValueError("aws_repository is required by Cloud and Parallel track")
        if self.aws_repository is not None and not set(self.tracks).issubset(aws_track):
            raise ValueError("aws_repository can be used only with Cloud and Parallel track")
        if (self.archive is not None or self.command is not None) and not set(self.tracks).isdisjoint(aws_track):
            raise ValueError("archive and command field can't be used with Cloud and Parallel track")
        return self

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

    def get_logics_by_track(self) -> dict[Track, set[Logic]]:
        """Return the logics in which the solver participates"""
        tracks = self.get()
        return dict((track, union(tracks[track].values())) for track in tracks)

    def complete(self, archive: Archive | None, command: Command | None) -> ParticipationCompleted:
        archive = cast(Archive, archive if self.archive is None else self.archive)
        command = cast(Command, command if self.command is None else self.command)
        if (self.aws_repository is not None) or set(self.tracks).issubset({Track.Cloud, Track.Parallel}):
            raise ValueError("can't complete Cloud and Parallel track participations")
        return ParticipationCompleted(
            tracks=self.get(), archive=archive, command=command, experimental=self.experimental
        )


import itertools


def union(s: Iterable[set[U]]) -> set[U]:
    return functools.reduce(lambda x, y: x | y, s, set())


class Participations(RootModel):
    root: list[Participation]

    def get_divisions(self, l: list[Track] = list(Track)) -> set[Division]:
        """ " Return the divisions in which the solver participates"""
        tracks = self.get()
        return union(set(tracks[track].keys()) for track in l if track in tracks)

    def get_logics(self, l: list[Track] = list(Track)) -> set[Logic]:
        """ " Return the logics in which the solver participates"""
        tracks = self.get()
        return union(itertools.chain.from_iterable([tracks[track].values() for track in l if track in tracks]))

    def get_logics_by_track(self) -> dict[Track, set[Logic]]:
        """Return the logics in which the solver participates"""
        tracks = self.get()
        return dict((track, union(tracks[track].values())) for track in tracks)

    def get(self, d: None | dict[Track, dict[Division, set[Logic]]] = None) -> dict[Track, dict[Division, set[Logic]]]:
        if d is None:
            d = {}
        for p in self.root:
            p.get(d)
        return d


class Submission(BaseModel, extra="forbid"):
    name: str = Field(
        description="The solver name should respect the guidelines given in the rules of the SMT-competition (derived solver, wrapper solver, ...)"
    )
    contributors: list[Contributor] = Field(
        min_length=1, description="The contributors will not be contacted except if they are also in contacts"
    )
    contacts: list[NameEmail] = Field(min_length=1, description="Used if the organizers need to discuss the submission")
    archive: Archive | None = None
    command: Optional[Command] = Field(
        default=None, description="Fields command given in participations have priority over this one"
    )
    website: HttpUrl
    system_description: HttpUrl
    solver_type: SolverType
    participations: Participations
    seed: int | None = None
    competitive: bool = True
    final: bool = Field(
        default=False,
        description="Must be set for the final version of the submission. An archive on zenodo is needed in this case.",
    )

    @model_validator(mode="after")
    def check_archive(self) -> Submission:
        if self.archive is None and not all(p.archive or p.aws_repository for p in self.participations.root):
            raise ValueError(
                "Field archive (or aws_repository) is needed in all participations if not present at the root"
            )
        if self.command is None and not all(p.command or p.aws_repository for p in self.participations.root):
            raise ValueError(
                "Field command (or aws_repository) is needed in all participations if not present at the root"
            )

        def check_archive(archive: None | Archive) -> None:
            if archive:
                archive.check_final()

        if self.final:
            check_archive(self.archive)
            for p in self.participations.root:
                check_archive(p.archive)

        return self

    def uniq_id(self) -> str:
        return hashlib.sha256(self.name.encode()).hexdigest()

    def complete_participations(self) -> list[ParticipationCompleted]:
        """Push defaults from the submission into participations"""
        return [p.complete(self.archive, self.command) for p in self.participations.root if p.aws_repository is None]


class Smt2File(BaseModel):
    incremental: bool
    logic: Logic
    family: tuple[str, ...]
    name: str

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def check_archive(self) -> Smt2File:
        if "/" in self.name:
            raise ValueError("name should not contain /, directory part should go in family name")
        for f in self.family:
            if "/" in f:
                raise ValueError("family part should not contain /, it should be splitted")
        return self

    def path(self) -> Path:
        if self.incremental:
            i = "incremental"
        else:
            i = "non-incremental"
        return Path(i, str(self.logic)).joinpath(Path(*self.family)).joinpath(self.name)

    def family_path(self) -> Path:
        return Path(*self.family)

    @classmethod
    def of_tuple(cls, incremental: bool, logic: Logic, family: Path | str, name: str) -> Smt2File:
        parts = PurePath(family).parts

        return Smt2File(
            incremental=incremental,
            logic=logic,
            family=parts,
            name=name,
        )

    @classmethod
    def of_path(cls, p: Path) -> Smt2File:
        parts = PurePath(p).parts
        match parts[0]:
            case "incremental":
                incremental = True
            case "non-incremental":
                incremental = False
            case _:
                raise ValueError("Smt2File path should start with incremental or non-incremental")

        return Smt2File(
            incremental=incremental,
            logic=Logic(parts[1]),
            family=parts[2:-1],
            name=parts[-1],
        )


class InfoIncremental(BaseModel):
    file: Smt2File
    check_sats: int


class InfoNonIncremental(BaseModel):
    file: Smt2File
    status: Status
    asserts: int


class Benchmarks(BaseModel):
    incremental: list[InfoIncremental] = []
    non_incremental: list[InfoNonIncremental] = []


class Result(BaseModel):
    track: Track
    solver: str
    file: Smt2File
    result: Answer
    cpu_time: float
    wallclock_time: float
    memory_usage: float
    nb_answers: int = 1
    """
    For incremental track, number of answered check-sat
    For unsat-core, size of unsat-core
    """


class Results(BaseModel):
    results: list[Result]


## Parameters that can change each year
class Config:
    __next_id__: ClassVar[int] = 0
    current_year = 2024
    oldest_previous_results = 2018
    timelimit_s = 60 * 20
    memlimit_M = 1024 * 20
    cpuCores = 4
    min_used_benchmarks = 300
    ratio_of_used_benchmarks = 0.5
    use_previous_results_for_status = False
    """
    Complete the status given in the benchmarks using previous results
    """
    old_criteria = False
    """"Do we try to emulate <= 2023 criteria that does not really follow the rules"""
    invert_triviality = False
    """Prioritize triviality as much as possible for testing purpose.
        Look for simple problems instead of hard one"""

    nyse_seed = 17817
    """The integer part of one hundred times the opening value of the New York Stock Exchange Composite Index on the first day the exchange is open on or after the date specified in nyse_date"""
    nyse_date = date(year=2024, month=6, day=17)

    aws_timelimit_hard = 180
    """
    Time in seconds upon which benchmarks are considered hards
    """
    aws_num_selected = 400
    """
    Number of selected benchmarks
    """
    unsat_core_min_num_asserts = 2
    """
    Minimum number of assertions for unsat core
    """
    dolmen_commit = "871b9de26643052dfcfa5b47ee23785f0b983219"
    """
    Commit of the model validator dolmen (branch smtcomp-2023)
    """
    dolmen_force_logic_ALL = False
    """
    Some benchmarks are not accepted by dolmen in their current logic.
    During model validation we can rerun by forcing logic ALL to accept more models
    """

    removed_benchmarks = [
        {
            "logic": int(Logic.QF_LIA),
            "family": "20210219-Dartagnan/ConcurrencySafety-Main",
            "name": "39_rand_lock_p0_vs-O0.smt2",
        }  # scrambler segfault (perhaps stack limit)
    ]
    """
    Benchmarks to remove before selection (currently just for aws)
    """

    removed_results = [
        {
            "logic": int(Logic.QF_BV),
            "family": "20230221-oisc-gurtner",
            "name": "SLL-NESTED-8-32-sp-not-excluded.smt2",
        }  # wrong status in SMTLIB
    ]
    """
    Benchmarks to remove after running the solvers. Can be used when the selection has already been done.
    """

    def __init__(self, data: Path | None) -> None:
        self.id = self.__class__.__next_id__
        self.__class__.__next_id__ += 1
        if data is not None and data.name != "data":
            raise ValueError("Consistency check, data directory must be named 'data'")
        self._data = data

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Config):
            return self.id == other.id
        return False

    def __hash__(self: Config) -> int:
        return self.id

    @functools.cached_property
    def data(self) -> Path:
        if self._data is None:
            raise ValueError("Configuration without data")
        return self._data

    @functools.cached_property
    def previous_years(self) -> list[int]:
        return list(range(self.oldest_previous_results, self.current_year))

    @functools.cached_property
    def previous_results(self) -> list[tuple[int, Path]]:
        return [(year, self.data.joinpath(f"results-sq-{year}.json.gz")) for year in self.previous_years]

    @functools.cached_property
    def current_results(self) -> dict[Track, Path]:
        return dict(
            (track, self.data.joinpath(f"results-{track.short_cut()}-{self.current_year}.json.gz")) for track in Track
        )

    @functools.cached_property
    def cached_current_results(self) -> dict[Track, Path]:
        return dict(
            (track, self.data.joinpath(f"results-{track.short_cut()}-{self.current_year}.feather")) for track in Track
        )

    @functools.cached_property
    def benchmarks(self) -> Path:
        return self.data.joinpath(f"benchmarks-{Config.current_year}.json.gz")

    @functools.cached_property
    def cached_non_incremental_benchmarks(self) -> Path:
        return self.data.joinpath(f"benchmarks-non-incremental-{Config.current_year}.feather")

    @functools.cached_property
    def cached_incremental_benchmarks(self) -> Path:
        return self.data.joinpath(f"benchmarks-incremental-{Config.current_year}.feather")

    @functools.cached_property
    def cached_previous_results(self) -> Path:
        return self.data.joinpath(f"previous-sq-results-{Config.current_year}.feather")

    @functools.cached_property
    def submissions(self) -> list[Submission]:
        return [
            Submission.model_validate_json(Path(file).read_text()) for file in self.data.glob("../submissions/*.json")
        ]

    @functools.cached_property
    def web_results(self) -> Path:
        return self.data / ".." / "web" / "content" / "results"

    @functools.cached_property
    def dolmen_dir(self) -> Path:
        return self.data / "../external-tools/dolmen"

    @functools.cached_property
    def dolmen_binary(self) -> Path:
        return self.dolmen_dir / "binaries" / self.dolmen_commit / "dolmen"

    @functools.cached_property
    def seed(self) -> int:
        unknown_seed = 0
        seed = 0
        for s in self.submissions:
            if s.seed is None:
                unknown_seed += 1
            else:
                seed += s.seed
        seed = seed % (2**30)
        if self.nyse_seed is None:
            print(f"[red]Warning[/red] NYSE seed not set, and {unknown_seed} submissions are missing a seed")
        else:
            if unknown_seed > 0:
                raise ValueError(f"{unknown_seed} submissions are missing a seed")
            seed += self.nyse_seed
        return seed


class ValidationOk(BaseModel):
    stderr: str


class ValidationError(BaseModel):
    status: Answer
    stderr: str
    model: str


class NoValidation(BaseModel):
    """No validation possible"""


noValidation = NoValidation()

Validation = ValidationError | ValidationOk | NoValidation


class ValidationResult(RootModel):
    root: Union[ValidationError, ValidationOk, NoValidation] = Field(union_mode="left_to_right")
