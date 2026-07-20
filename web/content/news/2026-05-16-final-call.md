---
layout: single
author:
title: Final Call for Solvers  
date: 2026-05-16T00:00:00+01:00
---

 21st International Satisfiability Modulo Theories Competition
                        (SMT-COMP'26)
                    FINAL CALL FOR SOLVERS

                        July 24–25, 2026
                        Lisbon, Portugal



We invite registration of solvers for SMT-COMP 2026.


Solvers are entered into the competition via a pull request to the SMT-COMP
GitHub repository at:

https://github.com/SMT-COMP/smt-comp.github.io/tree/master/submissions

Detailed instructions can be found on the competition website
(https://smt-comp.github.io/2026/solver_submission/) . Note that solver binaries
must be uploaded to a publicly available space and the final version must be a
Zenodo (https://zenodo.org/) submission for reproducibility. Please include a
license file of your choice with your solver binaries.

The submission deadline for (first versions of) solvers is

    ***May 27, 2026 AoE***

After the above date, no new entrants will be accepted. However,
submitted solvers may be updated via the pull request until

    ***June 10, 2026 AoE***

Note that a short system description of 1-2 pages (see Section 4 of the
competition rules at https://smt-comp.github.io/2026/rules.pdf) is part of the
solver submission and is MANDATORY. The system descriptions can be submitted
until the initial solver deadline on May 27, 2026. Participants are
asked to provide a link to the system description in the submission. The system
description can be updated until June 10, 2026, but it must be
reviewable since the initial solver deadline. The links to the final solver
submission must be provided via the pull request to the organizers by the final
deadline.

As in the previous year, we will run single query, incremental, unsat-core, and
model-validation tracks on the BenchExec cluster
(https://github.com/sosy-lab/benchexec) owned by LMU's Software and
Computational Systems Lab (SoSy-Lab https://www.sosy-lab.org/), who are kind
enough to support our competition with their computing power. To be more
precise, the competition will be run on the 168 apollon nodes of the SoSy-Lab
BenchExec cluster (for more details see
https://vcloud.sosy-lab.org/cpachecker/webclient/master/info). It is also
possible to locally emulate and test the computing environment on the
competition machines using the following instructions:
https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines

You are encouraged to run the solvers in the above-mentioned environment for
testing. The submission process contains a continuous integration check that
tests the submitted binaries on a trivial set of input benchmarks for every pull
request. We will also run the first versions of all solvers on a small subset of
benchmarks using shorter timeout and send you the results. However, these checks
do not substitute thorough testing of the submitted solvers.

Your solver can have multiple configurations for different tracks, logics, etc.
These can be specified as part of the solver submission and changed until the
deadline for the final solver. The default configuration is used for all other
tracks.

Please see the competition rules for further details. Do not hesitate contacting us 
if you have any questions or comments.

Sincerely,

The organizing team

Dominik Winterer (chair) - University of Manchester, United Kingdom
Martin Jonáš - Masaryk University, Czechia
Tomáš Kolárik - Università della Svizzera italiana, Switzerland

## COMMUNICATION:
The competition website is at
https://smt-comp.github.io/2026/

The SMT-COMP repository is at
https://github.com/SMT-COMP/smt-comp.github.io

Public email regarding the competition may be sent to
smt-announce@googlegroups.com

