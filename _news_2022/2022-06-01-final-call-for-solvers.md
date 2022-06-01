---
layout: news
author:
title: Final call for solvers
newsdate: 2022-06-01
---
# 17th International Satisfiability Modulo Theories Competition (SMT-COMP'22)

## Final Call for Solvers

We now invite registration of solvers for SMT-COMP 2022.


Solvers must be uploaded to StarExec, and entered into the
competition via the [web form](https://forms.gle/ewNQdFJbmQ12GxpX8).

The submission deadline for (first versions of) solvers is


>    *** June 18, 2022. ***


After the above date, no new entrants will be accepted. However,
submitted solvers may be updated until


>    *** July 2, 2022. ***


We plan to publish the results including all materials in an artifact.
By participating, you agree that we may copy your solver binaries
to this artifact.  Please include a license file of your choice with
your solver binaries.  Please contact us, if you want to include other
files with the artifact.


Note that a short system description of 1-2 pages (see Section 4 of
the [competition rules](https://smt-comp.github.io/2022/rules.pdf))
is part of the solver submission and MANDATORY. Submission of the
system description is due until the final solver deadline on July 2,
2022. Participants are however asked to provide a link to the system
description in the registration form to facilitate the registration,
even if the actual description would not yet be available at the time
of the registration.  The StarExec links to the final solver
submission must be provided via email to the organizers by the final
deadline.

Some pre- and post-processors have changed for SMT-COMP 2022 and have
been uploaded to StarExec.  For the other tracks, you can use last
year’s pre-/post-processors for testing.  Note that for testing your solver in the
incremental track you need to [wrap the trace executor around your
solver](https://github.com/smt-comp/trace-executor#wrapping-your-solver).
If you don’t wrap it yourself, we will wrap your solver in
the competition.

**NEW**: Your solver can have multiple configurations for different
tracks.  To create different configurations, put multiple scripts into
the bin directory with the name `starexec_run_trackname`.   The
default configuration is used for all other tracks.

The model-validator currently does not work with the new experimental floating
point division.  We will upload a new post-processor for this division later.

As in the last year, we organize a separate parallel and cloud solving
track, hosted by Amazon Web Services.  More information on the
participation on these two tracks is available [here](https://smt-comp.github.io/2022/parallel-and-cloud-tracks.html).

Finally, this year we have a [proof exhibition
track](https://smt-comp.github.io/2022/proof-track.html) (details also at
Section 5.8 of the rules). Entrants are expected to submit a proof checker
together with solver. Moreover, the system description of entrants in this track
can have up to two extra pages for describing the respective proof format and
proof checker.

Please see the competition rules for further details.

Sincerely,

The organizing team

* Haniel Barbosa (chair), Universidade Federal de Minas Gerais, Brazil
* François Bobot, CEA List, France
* Jochen Hoenicke, Albert-Ludwigs-Universität Freiburg, Germany
