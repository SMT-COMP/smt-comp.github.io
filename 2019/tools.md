---
layout: tools
year: 2019

tools:

- name: Benchmark Scrambler
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2019.tar.gz
  tracks:
    - name: track_single_query
      release:
        name: SMT-COMP 2019 Pre-Processor
        url: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2019/SMT-COMP-2019-non-incremental-scrambler.tar.xz
    - name: track_incremental
      release:
        name: SMT-COMP 2019 Pre-Processor
        url: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2019/SMT-COMP-2019-incremental-scrambler.tar.xz
    - name: track_single_query_challenge
      release:
        name: SMT-COMP 2019 Pre-Processor
        url: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2019/SMT-COMP-2019-non-incremental-scrambler.tar.xz
    - name: track_incremental_challenge
      release:
        name: SMT-COMP 2019 Pre-Processor
        url: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2019/SMT-COMP-2019-incremental-scrambler.tar.xz
    - name: track_unsat_core
      release:
        name: SMT-COMP 2019 Pre-Processor
        url: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2019/SMT-COMP-2019-unsat-core-scrambler.tar.xz
    - name: track_model_validation
      release:
        name: SMT-COMP 2019 Pre-Processor
        url: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2019/SMT-COMP-2019-model-validation-scrambler.tar.xz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2019.tar.gz
  tracks:
    - name: track_single_query
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release:
        name: SMT-COMP 2019 Post-Processor
        url: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2019/SMT-COMP-2019-non-incremental-post-processor.tar.xz
    - name: track_incremental
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release:
        name: SMT-COMP 2019 Post-Processor
        url: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2019/SMT-COMP-2019-incremental-post-processor.tar.xz
    - name: track_single_query_challenge
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release:
        name: SMT-COMP 2019 Post-Processor
        url: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2019/SMT-COMP-2019-non-incremental-post-processor.tar.xz
    - name: track_incremental_challenge
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release:
        name: SMT-COMP 2019 Post-Processor
        url: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2019/SMT-COMP-2019-incremental-post-processor.tar.xz
    - name: track_unsat_core
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/unsat-core-track
      release:
        name: SMT-COMP 2019 Post-Processor
        url: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2019/SMT-COMP-2019-unsat-core-post-processor.tar.xz
    - name: track_model_validation
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/model-validation-track
      release:
        name: SMT-COMP 2019 Post-Processor
        url: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2019/SMT-COMP-2019-model-validation-post-processor.tar.xz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2019.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2019/SMT-COMP-2019-trace-executor.tar.xz
---
