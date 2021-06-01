---
layout: participant
year: 2021
contact: "konstantin.korovin@manchester.ac.uk"
name: "iProver"
preliminaryID: "33052"
finalID: "-1"
team: "Konstantin Korovin, Andre Duarte, Edvard K Holden"
variantOf: ""
wrapperTool: "iProver does not call other SMT solvers for solving but since it accepts only CNF in TF0 TPTP format, a wrapper script calls SMTtoTPTP converter to obtain TFF file and  Vampire for clausification of TFF to TCF."
derivedTool: ""
competing: "yes"
seed: "12281"
solverHomePage: "http://www.cs.man.ac.uk/~korovink/iprover/"
sysDescrUrl: "http://www.cs.man.ac.uk/~korovink/iprover-smt-comp-2021.pdf"
sysDescrName: "iProver-v3.5 (SMT-COMP 2021)"
divisions:
- name: UF
  tracks:
  - track_single_query
- name: UFDT
  tracks:
  - track_single_query
---