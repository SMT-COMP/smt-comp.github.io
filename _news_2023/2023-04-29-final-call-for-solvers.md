---
layout: news
author:
title: Final call for solvers
newsdate: 2023-02-07
---

================================================


 18th International Satisfiability Modulo Theories Competition

                         (SMT-COMP'23)


               FINAL CALL FOR SOLVERS


=================================================


We now invite registration of solvers for SMT-COMP 2023.


Solvers must be uploaded to StarExec, and entered into the competition via the web form at

https://forms.gle/xhUDQaTynbS3mccE7

The submission deadline for (first versions of) solvers is


    ***May 13, 2023. ***


After the above date, no new entrants will be accepted. However, submitted solvers may be updated until


    ***May 27, 2023. ***


We plan to publish the results including all materials in an artifact. By participating, you agree that we may copy your solver binaries to this artifact.  Please include a license file of your choice with your solver binaries.  Please contact us, if you want to include other files with the artifact.


Note that a short system description of 1-2 pages (see Section 4 of the competition rules at https://smt-comp.github.io/2023/rules.pdf) is part of the solver submission and MANDATORY. Submission of the system description is THIS YEAR due for the initial solver deadline on May 13, 2023. Participants are asked to provide a link to the system description in the registration form. The system description can be updated until May 27, 2023, however it must be reviewable since the initial solver deadline. The StarExec links to the final solver submission must be provided via email to the organizers by the final deadline.


The pre- and post-processors have changed for the model validator (see below) for SMT-COMP 2023 and will be uploaded soon to StarExec.  For the other tracks, you can use last year’s pre-/post-processors for testing.  Note that for testing your solver in the incremental track you need to wrap the trace executor around your solver, see https://github.com/smt-comp/trace-executor#wrapping-your-solver. If you don’t wrap it yourself, we will wrap your solver in the competition.

Your solver can have multiple configurations for different tracks.  To create different configurations, put multiple scripts into the bin directory with the name starexec_run_trackname.  The default configuration is used for all other tracks.

As in the last year, we organize a separate parallel and cloud solving track, hosted by Amazon Web Services.  For more information on the participation on these two tracks, see https://smt-comp.github.io/2023/parallel-and-cloud-tracks.html.

We propose some new syntax for the model output in the new experimental logics at https://smt-comp.github.io/2023/model.html. The model validator will accept it.

Finally, like last year we have a proof exhibition track (details on https://smt-comp.github.io/2023/proof-track.html and in Section 5.8 of the rules). Entrants are expected to submit a proof checker together with their solver. Moreover, the system description of entrants in this track can have up to two extra pages for describing the respective proof format and proof checker.

Please see the competition rules for further details.

Sincerely,

The organizing team

François Bobot (chair), CEA List, France
Martin Bromberger, MPI for Informatics, Germany
Jochen Hoenicke, Certora, Israel
