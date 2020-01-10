---
layout: tools
year: 2020

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2020.tar.gz
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Non-Incremental Scrambler
      starexecid: 551
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP-2020-non-incremental-scrambler.tar.xz
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental Scrambler
      starexecid: 595
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP-2020-incremental-scrambler.tar.xz
    - name: track_single_query_challenge
      starexec: SMT-COMP 2020 Non-Incremental Scrambler
      starexecid: 551
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP-2020-non-incremental-scrambler.tar.xz
    - name: track_incremental_challenge
      starexec: SMT-COMP 2020 Incremental Scrambler
      starexecid: 595
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP-2020-incremental-scrambler.tar.xz
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core Scrambler
      starexecid: 589
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP-2020-unsat-core-scrambler.tar.xz
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation Scrambler
      starexecid: 554
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP-2020-model-validation-scrambler.tar.xz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2020.tar.gz
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Non-Incremental
      starexecid: 555
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-non-incremental-post-processor.tar.xz
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental
      starexecid: 556
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-incremental-post-processor.tar.xz
    - name: track_single_query_challenge
      starexec: SMT-COMP 2020 Non-Incremental
      starexecid: 555
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-non-incremental-post-processor.tar.xz
    - name: track_incremental_challenge
      starexec: SMT-COMP 2020 Incremental
      starexecid: 556
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-incremental-post-processor.tar.xz
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core
      starexecid: 594
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/unsat-core-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-unsat-core-post-processor.tar.xz
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation
      starexecid: 587
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/model-validation-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-model-validation-post-processor.tar.xz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2020.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2020/SMT-COMP-2020-trace-executor.tar.xz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=369598

---
