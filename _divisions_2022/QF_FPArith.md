---
layout: division
year: 2022
division: QF_FPArith
logics: 
- QF_ABVFP: http://smtlib.cs.uiowa.edu/logics.shtml#QF_ABVFP
  QF_ABVFPLRA: http://smtlib.cs.uiowa.edu/logics.shtml#QF_ABVFPLRA
  QF_AUFBVFP: http://smtlib.cs.uiowa.edu/logics.shtml#QF_AUFBVFP
  QF_BVFP: http://smtlib.cs.uiowa.edu/logics.shtml#QF_BVFP
  QF_BVFPLRA: http://smtlib.cs.uiowa.edu/logics.shtml#QF_BVFPLRA
  QF_FP: http://smtlib.cs.uiowa.edu/logics.shtml#QF_FP
  QF_FPLRA: http://smtlib.cs.uiowa.edu/logics.shtml#QF_FPLRA
  QF_UFFP: http://smtlib.cs.uiowa.edu/logics.shtml#QF_UFFP
  QF_UFFPDTNIRA: http://smtlib.cs.uiowa.edu/logics.shtml#QF_UFFPDTNIRA
tracks:
- name: track_single_query
  status: competitive
  n_insts: 1654
  logic_insts:
  - QF_ABVFP: 600
    QF_ABVFPLRA: 25
    QF_AUFBVFP: 1
    QF_BVFP: 465
    QF_BVFPLRA: 69
    QF_FP: 285
    QF_FPLRA: 55
    QF_UFFP: 0
    QF_UFFPDTNIRA: 154
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
- name: track_incremental
  status: competitive
  n_insts: 9752
  logic_insts:
  - QF_ABVFP: 9214
    QF_ABVFPLRA: 7
    QF_BVFP: 300
    QF_BVFPLRA: 63
    QF_FP: 166
    QF_FPLRA: 1
    QF_UFFP: 1
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
- name: track_unsat_core
  status: competitive
  n_insts: 13674
  logic_insts:
  - QF_ABVFP: 1971
    QF_ABVFPLRA: 5
    QF_AUFBVFP: 0
    QF_BVFP: 1588
    QF_BVFPLRA: 52
    QF_FP: 10052
    QF_FPLRA: 0
    QF_UFFP: 2
    QF_UFFPDTNIRA: 4
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
- name: track_model_validation
  status: experimental
  n_insts: 17301
  logic_insts:
  - QF_BVFP: 7028
    QF_BVFPLRA: 116
    QF_FP: 10106
    QF_FPLRA: 51
    QF_UFFP: 0
  n_excluded: 0
  logic_excluded:
  - QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
- name: track_proof_exhibition
  status: competitive
  n_insts: 13848
  logic_insts:
  - QF_ABVFP: 1973
    QF_ABVFPLRA: 5
    QF_AUFBVFP: 0
    QF_BVFP: 1591
    QF_BVFPLRA: 52
    QF_FP: 10091
    QF_FPLRA: 6
    QF_UFFP: 2
    QF_UFFPDTNIRA: 128
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
- name: track_cloud
  status: competitive
  n_insts: 0
  logic_insts:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
- name: track_parallel
  status: competitive
  n_insts: 0
  logic_insts:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_AUFBVFP: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_FPLRA: 0
    QF_UFFP: 0
    QF_UFFPDTNIRA: 0
---

