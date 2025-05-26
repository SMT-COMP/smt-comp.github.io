================================================


 <N-6>th International Satisfiability Modulo Theories Competition

                         (SMT-COMP'<N>)


               FINAL CALL FOR SOLVERS


=================================================


We now invite registration of solvers for SMT-COMP 20<N>.


Solvers are entered into the competition via a pull request to the SMT-COMP
GitHub repository at

https://github.com/SMT-COMP/smt-comp.github.io/tree/master/submissions

Detailed instructions can be found in the README file there. Note that solver
binaries must be uploaded to a publicly available space and the final version
must be a Zenodo (https://zenodo.org/) submission for reproducibility. Please
include a license file of your choice with your solver binaries.

The submission deadline for (first versions of) solvers is

    ***<deadline first version>***

After the above date, no new entrants will be accepted. However,
submitted solvers may be updated via additional pull requests until

    ***<deadline last version>***

Note that a short system description of 1-2 pages (see Section 4 of the
competition rules at https://smt-comp.github.io/2025/rules.pdf) is part of the
solver submission and is MANDATORY. The system descriptions can be submitted
until the initial solver deadline on <deadline first version>. Participants are
asked to provide a link to the system description in the submission. The system
description can be updated until <deadline last version>, but it must be
reviewable since the initial solver deadline. The links to the final solver
submission must be provided via a pull request to the organizers by the final
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

Due to the lack of suitable infrastructure, Cloud track is not taking place for
SMT-COMP 2025. Parallel track is going to be executed on the same
BenchExec-based infrastructure as the other tracks, only on machines with a
higher numbers of CPU cores. As a result, there is no special submission process
for the parallel track and the submissions should follow the some process as the
rest of the competition.

Please see the competition rules for further details.

Sincerely,

The organizing team
<Team>
