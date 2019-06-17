---
layout: logic
division: QF_FP
description: http://smtlib.cs.uiowa.edu/logics.shtml#QF_FP
tracks:
- name: track_single_query
  n_insts: 250
  n_excluded: 0
  status: competitive
- name: track_incremental
  n_insts: 2
  n_excluded: 0
  status: non-competitive
- name: track_single_query_challenge
  n_insts: 0
  n_excluded: 0
  status: competitive
- name: track_incremental_challenge
  n_insts: 0
  n_excluded: 0
  status: competitive
- name: track_unsat_core
  n_insts: 10031
  n_excluded: 0
  status: non-competitive
- name: track_model_validation
  n_insts: 0
  n_excluded: 0
  status: competitive
---
QF_FP Incremental Track track participated only by Z3, CVC4.
QF_FP Unsat Core Track track participated only by Z3, CVC4.
