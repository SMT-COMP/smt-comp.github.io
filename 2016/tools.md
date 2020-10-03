---
layout: tools
year: 2016

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2016.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2016 Scrambler
      starexecid: 349
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2016/SMT-COMP-2016-Application-Scrambler.tar.xz
    - name: track_application
      starexec: SMT-COMP 2016 Application Scrambler
      starexecid: 285
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2016/SMT-COMP-2016-Application-Scrambler.tar.xz
    - name: track_unsat_core
      starexec: SMT-COMP 2016 Unsat-Core Scrambler
      starexecid: 350
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2016/SMT-COMP-2016-Unsat-Core-Scrambler.tar.xz
      note: Patch <a href="https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2016/generate_unsat_core_benchmark.patch">generate_unsat_core_benchmark.patch</a> was applied on top of the sources.

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2016.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2016
      starexecid: 273
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2016/SMT-COMP-2016-Main-Track-Postprocessor.tgz
    - name: track_application
      starexec: SMT-COMP 2016 Application Track
      starexecid: 274
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2016/SMT-COMP-2016-Application-Track-Postprocessor.tgz
    - name: track_unsat_core
      starexec: SMT-COMP 2016 Unsat-Core Track
      starexecid: 297
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2016/SMT-COMP-2016-Unsat-Core-Track-Postprocessor.tgz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2016.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2016/SMT-COMP-2016-trace-executor.tar.xz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=259879

---
