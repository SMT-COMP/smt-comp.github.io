---
layout: tools
year: 2014

tools:

- name: Pre-Processor (Benchmark Scrambler)
  repo: https://github.com/SMT-COMP/scrambler
  sources: tools/smtcomp2012_scrambler.tar.gz
  tracks:
    - name: track_main
      starexec: SMT-COMP 2014 Scrambler
      starexecid: 120
      release: tools/SMT-COMP-2014-Scrambler.tgz
    - name: track_application
      starexec: SMT-COMP 2014 Application Scrambler
      starexecid: 134
      release: tools/SMT-COMP-2014-Application-Track-Scrambler.tgz

- name: Post-Processor
  repo: https://github.com/SMT-COMP/postprocessors
  sources:
  tracks:
    - name: track_application
      starexec: SMT-COMP 2014 Application Track
      starexecid: 140
      release: tools/SMT-COMP-2014-Application-Track-Postprocessor.tgz

- name: Trace executor
  repo: https://github.com/SMT-COMP/trace-executor
  sources: tools/SMT-COMP-2014-Trace-Executor.tgz
  release:
  wrapped: https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=54072

---
