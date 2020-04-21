---
layout: tools
year: 2020

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources:
  release:
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Non-Incremental Scrambler
      starexecid: 611
      release:
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental Scrambler
      starexecid: 609
      release:
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core Scrambler
      starexecid: 607
      release:
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation Scrambler
      starexecid: 610
      release:

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources:
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Non-Incremental
      starexecid: 616
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release:
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental
      starexecid: 615
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release:
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core
      starexecid: 613
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/unsat-core-track
      release:
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation
      starexecid: 614
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/model-validation-track
      release:

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor

---
