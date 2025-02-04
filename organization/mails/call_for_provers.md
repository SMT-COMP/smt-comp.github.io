================================================


 <N-6>th International Satisfiability Modulo Theories Competition

                         (SMT-COMP'<N>)


               FINAL CALL FOR SOLVERS


=================================================


We now invite registration of solvers for SMT-COMP 20<N>.


Solvers are entered into the competition via a push request to the SMT-COMP GitHub repository at 

https://github.com/SMT-COMP/smt-comp.github.io/tree/master/submissions. 

Detailed instructions can be found in the README file there. Note that solvers must be uploaded to a publicly available space as a docker file that compiles the solver and the final version must be a Zenodo (https://zenodo.org/) submission for reproducibility.

The submission deadline for (first versions of) solvers is

    ***<deadline first version>***

After the above date, no new entrants will be accepted. However,
submitted solvers may be updated via a push request until

    ***<deadline last version> ***

We plan to publish the results including all materials in an artifact.
By participating, you agree that we may copy your solver binaries to
this artifact.  Please include a license file of your choice with your
solver binaries.  Please contact us, if you want to include other files
with the artifact.

Note that a short system description of 1-2 pages (see Section 4 of the
competition rules at https://smt-comp.github.io/20<N>/rules.pdf) is part
of the solver submission and MANDATORY. Submission of the system
description is THIS YEAR due for the initial solver deadline on <deadline first version>.
Participants are asked to provide a link to the system
description in the registration form. The system description can be
updated until <deadline last version>, however it must be reviewable since the
initial solver deadline. The links to the final solver submission must be 
provided via a push request to the organizers by the final deadline.

The single query, incremental, unsat-core, and model-validation tracks
will no longer run on StarExec (http://www.starexec.org) because 
StarExec is in the process of being decommissioned. As last year, 
we will run these tracks on the BenchExec cluster 
(https://github.com/sosy-lab/benchexec) owned by LMU's Software and 
Computational Systems Lab (SoSy-Lab https://www.sosy-lab.org/), who 
are kind enough to support our competition with their computing power.
To be more precise, the competition will be run on the 168 apollon nodes
of the SoSy-Lab BenchExec 4cluster (for more details see https://vcloud.sosy-lab.org/cpachecker/webclient/master/info).
It is also possible to locally emulate and test the computing environment
on the competition machines using the following instructions: https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines




<TO Update> As in the last year, we organize a separate parallel and cloud solving
track, hosted by Amazon Web Services.  For more information on the
participation on these two tracks, see
https://smt-comp.github.io/20<N>/parallel-and-cloud-tracks.html.


Please see the competition rules for further details.

Sincerely,

The organizing team
<Team>
