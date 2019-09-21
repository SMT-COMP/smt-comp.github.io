---
layout: tools
year: 2017

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2017.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2017 Scrambler
      starexecid: 349
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2017/SMT-COMP-2017-Application-Scrambler.tar.xz
    - name: track_application
      starexec: SMT-COMP 2016 Application Scrambler
      starexecid: 285
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2017/SMT-COMP-2017-Application-Scrambler.tar.xz
      note: For the Application Track, on StarExec, the 2016 benchmark scrambler was used.
    - name: track_unsat_core
      starexec: SMT-COMP 2017 Unsat-Core Scrambler
      starexecid: 350
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2017/SMT-COMP-2017-Unsat-Core-Scrambler.tar.xz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2018.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2017
      starexecid: 348
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/single-problem-challenge-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2017/SMT-COMP-2017-Main-Track-Postprocessor.tgz
    - name: track_application
      starexec: SMT-COMP 2016 Application Track
      starexecid: 274
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/incremental-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2017/SMT-COMP-2017-Application-Track-Postprocessor.tgz
      note: For the Application Track, on StarExec, the 2016 post-processor was used.
    - name: track_unsat_core
      starexec: SMT-COMP 2017 Unsat-Core Track
      starexecid: 351
      repo: https://github.com/SMT-COMP/postprocessors/tree/master/unsat-core-track
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2017/SMT-COMP-2017-Unsat-Core-Track-Postprocessor.tgz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2017.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2016/SMT-COMP-2016-trace-executor.tar.xz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=311571
  note: For the Application Track, the 2016 trace executor binary was used.
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=259879

---
