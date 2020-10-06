---
layout: tools
year: 2015

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: https://github.com/SMT-COMP/scrambler/archive/smtcomp2015.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2015 Scrambler
      starexecid: 226
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2015/SMT-COMP-2015-Main-Scrambler.tar.xz
    - name: track_application
      starexec: SMT-COMP 2015 Application Scrambler
      starexecid: 225
      release: https://github.com/SMT-COMP/scrambler/releases/download/smtcomp2015/SMT-COMP-2015-Application-Track-Scrambler.tar.xz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources: https://github.com/SMT-COMP/postprocessors/archive/smtcomp2015.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2015
      starexecid: 189
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2015/SMT-COMP-2015-Main-Track-Postprocessor.tgz
    - name: track_application
      starexec: SMT-COMP 2015 Application Track
      starexecid: 198
      release: https://github.com/SMT-COMP/postprocessors/releases/download/smtcomp2015/SMT-COMP-2015-Application-Track-Postprocessor.tgz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: https://github.com/SMT-COMP/trace-executor/archive/smtcomp2015.tar.gz
  release: https://github.com/SMT-COMP/trace-executor/releases/download/smtcomp2015/SMT-COMP-2015-trace-executor.tar.xz
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=67803

---
