---
layout: division
year: 2023
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
  n_insts: 1596
  logic_insts:
  - QF_ABVFP: 593
    QF_ABVFPLRA: 25
    QF_AUFBVFP: 1
    QF_BVFP: 414
    QF_BVFPLRA: 78
    QF_FP: 273
    QF_FPLRA: 58
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
    QF_BVFPLRA: 64
    QF_FP: 166
    QF_UFFP: 1
  n_excluded: 0
  logic_excluded:
  - QF_ABVFP: 0
    QF_ABVFPLRA: 0
    QF_BVFP: 0
    QF_BVFPLRA: 0
    QF_FP: 0
    QF_UFFP: 0
- name: track_unsat_core
  status: competitive
  n_insts: 13674
  logic_insts:
  - QF_ABVFP: 1972
    QF_ABVFPLRA: 5
    QF_AUFBVFP: 0
    QF_BVFP: 1589
    QF_BVFPLRA: 52
    QF_FP: 10050
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
  n_insts: 24441
  logic_insts:
  - QF_ABVFP: 7046
    QF_ABVFPLRA: 25
    QF_AUFBVFP: 1
    QF_BVFP: 7030
    QF_BVFPLRA: 124
    QF_FP: 10137
    QF_FPLRA: 54
    QF_UFFP: 0
    QF_UFFPDTNIRA: 24
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
- name: track_proof_exhibition
  status: competitive
  n_insts: 7041
  logic_insts:
  - QF_ABVFP: 990
    QF_ABVFPLRA: 5
    QF_AUFBVFP: 0
    QF_BVFP: 797
    QF_BVFPLRA: 53
    QF_FP: 5061
    QF_FPLRA: 5
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

