---
layout: tools
year: 2018

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2018.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2018 Scrambler
      starexecid: 379
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2018/SMT-COMP-2018-Main-Scrambler.tar.xz
    - name: track_application
      starexec: SMT-COMP 2018 Application Scrambler
      starexecid: 380
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2018/SMT-COMP-2018-Application-Scrambler.tar.xz
    - name: track_unsat_core
      starexec: SMT-COMP 2018 Unsat-Core Scrambler
      starexecid: 381
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2018/SMT-COMP-2018-Unsat-Core-Scrambler.tar.xz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2018.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2018
      starexecid: 376
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2018/SMT-COMP-2018-Main-Track-Postprocessor.tgz
    - name: track_application
      starexec: SMT-COMP 2018 Application Track
      starexecid: 377
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2018/SMT-COMP-2018-Application-Track-Postprocessor.tgz
    - name: track_unsat_core
      starexec: SMT-COMP 2018 Unsat-Core Track
      starexecid: 389
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2018/SMT-COMP-2018-Unsat-Core-Track-Postprocessor.tgz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2018.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2018/SMT-COMP-2018-trace-executor.tar.xz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=311571

---
