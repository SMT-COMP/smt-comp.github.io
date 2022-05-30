---
layout: tools
year: 2022

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
#  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2021.tar.gz
  release:
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2021 Single-Query Scrambler
      starexecid: 708
    - name: track_incremental
      starexec: SMT-COMP 2021 Incremental Scrambler
      starexecid: 709
    - name: track_unsat_core
      starexec: SMT-COMP 2021 Unsat Core Scrambler
      starexecid: 711
    - name: track_model_validation
      starexec: SMT-COMP 2021 Model Validation Scrambler
      starexecid: 710
    - name: track_proof_exhibition
      starexec: SMT-COMP 2022 Proof Exhibition Scrambler
      starexecid: 729

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
#  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2021.tar.gz
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2021 Single Query
      starexecid: 692
    - name: track_incremental
      starexec: SMT-COMP 2021 Incremental
      starexecid: 691
    - name: track_unsat_core
      starexec: SMT-COMP 2021 Unsat Core
      starexecid: 727
    - name: track_model_validation
      starexec: SMT-COMP 2021 Model-Validation
      starexecid: 672
    - name: track_proof_exhibition
      starexec: SMT-COMP 2022 Proof-Exhibition
      starexecid: 741

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2022.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2022/SMT-COMP-2022-trace-executor.tar.gz

- name: Competition scripts
  repo: https://github.com/SMT-COMP/smt-comp

---

There are no significant changes for the tracks from SMT-COMP 2021, so
the pre- and post-processors from SMT-COMP 2021 can be used for testing.

We will release the tools used in 2022 after the competition.
