---
layout: participants

year: 2021
participants: participants_2021

nyse:
  date: 2021-06-15
  value: 

divisions:
- name: Arith
  logics:
  - NIA
  - LRA
  - LIA
  - NRA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: Bitvec
  logics:
  - BV
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: Equality
  logics:
  - UFDT
  - UF
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: Equality+LinearArith
  logics:
  - AUFLIRA
  - AUFLIA
  - AUFDTLIRA
  - UFLRA
  - UFDTLIA
  - ALIA
  - UFDTLIRA
  - AUFDTLIA
  - AUFFPDTLIRA
  - UFLIA
  - UFIDL
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: Equality+MachineArith
  logics:
  - UFBV
  - UFFPDTLIRA
  - UFFPDTNIRA
  - ABVFP
  - ABV
  - AUFBVFP
  - AUFBVDTNIA
  - AUFBVDTLIA
  - ABVFPLRA
  - UFBVLIA
  - UFBVFP
  - AUFBV
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: Equality+NonLinearArith
  logics:
  - UFDTNIA
  - UFNRA
  - AUFFPDTNIRA
  - UFNIA
  - AUFNIRA
  - UFDTNIRA
  - ANIA
  - AUFDTNIRA
  - AUFNIA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: FPArith
  logics:
  - BVFP
  - FP
  - BVFPLRA
  - FPLRA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: QF_Bitvec
  logics:
  - QF_BV
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
  - track_model_validation
- name: QF_Equality
  logics:
  - QF_AX
  - QF_DT
  - QF_UFDT
  - QF_UF
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
  - track_model_validation
- name: QF_Equality+Bitvec
  logics:
  - QF_UFBV
  - QF_AUFBV
  - QF_ABV
  - QF_BV
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
  - track_model_validation
- name: QF_Equality+Bitvec+Arith
  logics:
  - QF_AUFBVLIA
  - QF_UFBVLIA
  - QF_AUFBVNIA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: QF_Equality+LinearArith
  logics:
  - QF_UFLRA
  - QF_AUFLIA
  - QF_UFDTLIRA
  - QF_UFLIA
  - QF_UFIDL
  - QF_ALIA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
  - track_model_validation
- name: QF_Equality+NonLinearArith
  logics:
  - QF_UFNRA
  - QF_ANIA
  - QF_UFNIA
  - QF_AUFNIA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: QF_FPArith
  logics:
  - QF_ABVFPLRA
  - QF_FPLRA
  - QF_FP
  - QF_AUFBVFP
  - QF_BVFP
  - QF_ABVFP
  - QF_UFFP
  - QF_UFFPDTLIRA
  - QF_BVFPLRA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: QF_LinearIntArith
  logics:
  - QF_IDL
  - QF_LIA
  - QF_LRA
  - QF_LIRA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
  - track_model_validation
- name: QF_LinearRealArith
  logics:
  - QF_RDL
  - QF_LRA
  tracks:
  - track_single_query
  - track_unsat_core
  - track_model_validation
- name: QF_NonLinearIntArith
  logics:
  - QF_NIRA
  - QF_NIA
  tracks:
  - track_single_query
  - track_incremental
  - track_unsat_core
- name: QF_NonLinearRealArith
  logics:
  - QF_NRA
  tracks:
  - track_single_query
  - track_unsat_core
- name: QF_Strings
  logics:
  - QF_SNIA
  - QF_SLIA
  - QF_S
  tracks:
  - track_single_query
  - track_unsat_core
---