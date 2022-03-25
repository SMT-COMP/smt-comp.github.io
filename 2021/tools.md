---
layout: tools
year: 2021

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2021.tar.gz
  release:
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2021 Single-Query Scrambler
      starexecid: 708
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2021/SMT-COMP-2021-single-query-scrambler.tar.gz
    - name: track_incremental
      starexec: SMT-COMP 2021 Incremental Scrambler
      starexecid: 709
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2021/SMT-COMP-2021-incremental-scrambler.tar.gz
    - name: track_unsat_core
      starexec: SMT-COMP 2021 Unsat-Core Scrambler
      starexecid: 711
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2021/SMT-COMP-2021-unsat-core-scrambler.tar.gz
    - name: track_model_validation
      starexec: SMT-COMP 2021 Model-Validation Scrambler
      starexecid: 710
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2021/SMT-COMP-2021-model-validation-scrambler.tar.gz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2021.tar.gz
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2021 Single Query
      starexecid: 692
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2021/SMT-COMP-2021-single-query-post-processor.tar.gz
    - name: track_incremental
      starexec: SMT-COMP 2021 Incremental
      starexecid: 691
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2021/SMT-COMP-2021-incremental-post-processor.tar.gz
    - name: track_unsat_core
      starexec: SMT-COMP 2021 Unsat Core
      starexecid: 727
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2021/SMT-COMP-2021-unsat-core-post-processor.tar.gz
    - name: track_model_validation
      starexec: SMT-COMP 2021 Model-Validation
      starexecid: 672
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2021/SMT-COMP-2021-model-validation-post-processor.tar.gz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2021.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2021/SMT-COMP-2021-trace-executor.tar.gz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=458983

- name: Competition scripts
  repo: https://github.com/SMT-COMP/smt-comp

---
