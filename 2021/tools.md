---
layout: tools
year: 2020

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  release:
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2021 Single-Query Scrambler
      starexecid: 674
    - name: track_incremental
      starexec: SMT-COMP 2021 Incremental Scrambler
      starexecid: 675
    - name: track_unsat_core
      starexec: SMT-COMP 2021 Unsat-Core Scrambler
      starexecid: 695
    - name: track_model_validation
      starexec: SMT-COMP 2021 Model-Validation Scrambler
      starexecid: 671

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2021 Single Query
      starexecid: 692
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental
      starexecid: 691
    - name: track_unsat_core
      starexec: SMT-COMP 2021 Unsat Core
      starexecid: 694
    - name: track_model_validation
      starexec: SMT-COMP 2021 Model-Validation
      starexecid: 672

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2021.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2021/SMT-COMP-2021-trace-executor.tar.gz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=414650

- name: Competition scripts
  repo: https://github.com/SMT-COMP/smt-comp

---
