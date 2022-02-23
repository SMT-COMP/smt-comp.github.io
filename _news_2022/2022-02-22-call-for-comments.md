---
layout: news
author:
title: Call for comments
newsdate: 2022-02-22
---
Dear SMT-COMP participants, dear SMT-LIB community,

We are happy to announce the plans for the upcoming SMT competition
2022. We are welcoming François Bobot in the organizing team and are
thankful to Antti Hyvärinen, who is leaving the team after serving on
it for three years.

The main intended changes are listed below. We would be delighted to
receive community's feedback on the suggestions.

  1. We plan a proof exhibition track. Teams would submit
  proof-producing solvers together with proof checkers for their proof
  formats. We would compile and present the results, as well as
  assemble a panel of non-organizer experts to do a qualitative
  assessment for the proof-producing solver, proof format, and proof
  checker.

  2. We intend to change the rules for the benchmarks to be used in
  the model validation, unsat core and proof exhibition tracks. Rather
  than just considering the annotated status, we would also consider
  unknown benchmarks whose status was determined with confidence in
  the single query track of the current year.

  3. We will split the quantifier free logics with datatypes (QF_UFDT
  and QF_DT) into their own division.

  4. We want to change the rules so that (as before) we will not run
  non-competitive logics, even if they are in competitive divisions.

  5. We plan to add new divisions to the model validation track. We
  will aim for QF_FP and the combination with other supported theories
  (QF_UFFP, QF_BVFP, etc.).

  6. We intend to change the model validator from pysmt to Dolmen.

The motivation for a proof exhibition track, rather than a proof
validation track, is to be less prescriptive and more descriptive for
how SMT-COMP will approach proofs. Proper comparison for competition
would require a standard, or at least a common solution, that the
community does not have yet. However by incentivizing to showcase
their solutions we hope to move towards that.

The motivation for including unknown benchmarks into the tracks that
require statuses is to be able to select new or old benchmarks without
an official status but that nevertheless can have their status
determined with confidence.

We want to separate datatypes from arrays and uninterpreted functions
because few solvers have support for the former. Similarly,
considering logics to be non-competitive even in a competitive
division is intended to favor less the solvers that support more
logics.

For the model validation track, we continue in the tradition of
successively increasing the supported logics. Floating points should
be relatively simple to produce models to. What may be more
challenging is validating them, which is the motivation for changing
pysmt by Dolmen. We expect Dolmen to be easier to extend and more
performant. Guillaume Bury has been kind enough to help us in this
transition.

The organizing team

* Haniel Barbosa (chair), Universidade Federal de Minas Gerais, Brazil
* François Bobot, CEA List, France
* Jochen Hoenicke, Albert-Ludwigs-Universität Freiburg, Germany
