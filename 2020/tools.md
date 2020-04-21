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
      starexecid:
      release:
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental Scrambler
      starexecid:
      release:
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core Scrambler
      starexecid:
      release:
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation Scrambler
      starexecid:
      release:

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2020.tar.gz
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Non-Incremental
      starexecid:
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release:
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental
      starexecid:
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release:
    - name: track_single_query_challenge
      starexec: SMT-COMP 2020 Non-Incremental
      starexecid:
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release:
    - name: track_incremental_challenge
      starexec: SMT-COMP 2020 Incremental
      starexecid:
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release:
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core
      starexecid:
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/unsat-core-track
      release:
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation
      starexecid:
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/model-validation-track
      release:

---
