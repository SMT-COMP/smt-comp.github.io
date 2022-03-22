---
layout: news
author:
title: Call for solvers
newsdate: 2022-03-22
---
Hello everybody,

The submission deadline for the first version of the solvers is on Jun
18.  However, it is useful for the organizing team to know in advance
which and how many solvers may be entering.  If you have not submitted
a solver before, or if you think there may be unusual circumstances,
please let us know at your earliest convenience if you think you may
be submitting a solver to SMT-COMP'22.  We require a system
description for all submitted solvers as part of the submission of the
final solver versions (deadline Jul 2).

The parallel and cloud tracks will again run on AWS, which is kindly
supporting them. Participants of these tracks are required to submit
their solver via a GitHub repository (which can be private). The
repository should contain a docker file that compiles the
solver. Detailed instructions for submitting to these tracks are
available [in this link](https://github.com/aws-samples/aws-batch-comp-infrastructure-sample) (they lift to SMT).

To participate teams must email aws-smtcomp-2022@googlegroups.com with
the following:

1. name of the solver and a list of the authors
2. your AWS account number
3. the URL of the GitHub repository including the branch
4. the full, 40-character SHA-1 hash of the commit

We have a few central changes to the competition rules with respect to
previous years.

PROOF EXHIBITION TRACK

In this track teams can submit proof-producing solvers together with
proof checkers for their proof formats. We will compile and present
the results, as well as assemble a panel of non-organizer experts to
do a qualitative assessment for each proof-producing solver, proof
format, and proof checker.

NEW BENCHMARK SELECTION FOR CLOUD TRACK

The benchmark selection is simplified by using a unique way to select
elements from a set. For example randomly selecting n problems from a
set of problems is done by shuffling a list of the problems and
selecting the first n. So if there are less than n problems, they are
all selected. The complete selection is first done by selecting in
each category in each logic, then selecting the resulting set in each
category. At the end 400 benchmarks are selected.


BENCHMARKS WITHOUT STATUS CAN BE USED IN VALIDATION TRACKS

Unknown benchmarks that were confidently determined to be sat or unsat
during the single query track will be used in the model validation,
unsat core and proof exhibition tracks.

CHANGES FOR MULTIPLE LOGIC DIVISIONS

The quantifier free logics with datatypes (QF_UFDT and QF_DT) will
become their own division, moving out of the QF_Equality
division. Moreover, non-competitive logics will not run even if they
are in competitive divisions.

NEW MODEL VALIDATION TRACK LOGIC AND VALIDATOR

We will add to the model validation track quantifier free logics with
floating points. So QF_FP and the combination with other supported
theories (QF_UFFP, QF_BVFP, etc.), which are a subset of the
QF_FPArith division. This division will be experimental. We are also
changing the model validator from pysmt for Dolmen, which is a better
long-term solution, both for maintenance and for scalability.

Best,

* Haniel Barbosa (chair), Universidade Federal de Minas Gerais, Brazil
* François Bobot, CEA List, France Jochen Hoenicke,
* Albert-Ludwigs-Universität Freiburg, Germany
