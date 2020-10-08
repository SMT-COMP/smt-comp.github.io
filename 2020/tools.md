---
layout: tools
year: 2020

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2020.tar.gz
  release:
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Single-Query Scrambler
      starexecid: 611
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP.2020.Single.Query.Scrambler.tar.xz
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental Scrambler
      starexecid: 609
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP.2020.Incremental.Scrambler.tar.xz
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core Scrambler
      starexecid: 607
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP.2020.Unsat-Core.Scrambler.tar.xz
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation Scrambler
      starexecid: 610
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2020/SMT-COMP.2020.Model-Validation.Scrambler.tar.xz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2020.tar.gz
  tracks:
    - name: track_single_query
      starexec: SMT-COMP 2020 Single Query 2020 05 27
      starexecid: 632
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-single-query-post-processor.tar.xz
    - name: track_incremental
      starexec: SMT-COMP 2020 Incremental
      starexecid: 615
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-incremental-post-processor.tar.xz
    - name: track_unsat_core
      starexec: SMT-COMP 2020 Unsat-Core 2020 06 12
      starexecid: 647
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-unsat-core-postprocessor.tar.xz
    - name: track_model_validation
      starexec: SMT-COMP 2020 Model-Validation
      starexecid: 631
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2020/SMT-COMP-2020-model-validation-post-processor.tar.xz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2020.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2020/SMT-COMP-2020-trace-executor.tar.xz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=414650

- name: Competition scripts
  repo: https://github.com/SMT-COMP/smt-comp
  sources: https://github.com/SMT-COMP/smt-comp/archive/smtcomp2020.tar.gz
  tag: https://github.com/SMT-COMP/smt-comp/releases/tag/smtcomp2020

---
