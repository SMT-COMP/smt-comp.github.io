---
layout: news
author:
title: SMT-COMP 2021 pre-announcement
newsdate: 2020-12-17
---
Dear SMT-COMP participants, dear SMT-LIB community,

We are happy to announce the plans for the upcoming SMT competition 2021.  It will be run by the same organizers as last year. We propose a few changes to run more benchmarks, fix issues with scoring, and extend the model validation track.

In 2020 we further reduced the percentage of randomly selected benchmarks for bigger divisions to 40%.  We plan to increase it back to 50% as in 2019.

We change the rules such that the error score is only given to unsound solver results.  Previously, models or unsat cores that could not be parsed by the postprocessors, would be treated as errors.

We fix the way unsound results affect the unsat/sat score. Previously, a solver that always returned unsat would get a perfect unsat score because any errors were counted for the sat score.

We plan to add new divisions to the model validation track.  We will aim for QF_UF and the combination with other supported theories (QF_UFBV, QF_UFLIA, etc.).

The number of SMT-LIB benchmarks has grown so much that running all benchmarks is not possible any more, but we think that running half of them is okay. The timeout has the highest impact on the total run-time of the competition.  We feel the current timeout of  20 minutes is a good compromise.  Also we want to keep limiting the solver submissions: each team submitting more than one solver should only submit substantially different solvers.


The motivation for changing the error score is to punish only solvers that cannot be trusted because they produce unsound results.  These results can easily go unnoticed and may have harmful consequences if a solver is used in safety critical applications.  However, a syntactically invalid output or a solver crash is easy to detect and does not affect the trustworthiness of correct results given by the solver.  Also there is historic precedent: the single query track always treated syntactically wrong output as unknown and not as error. By extending the model validation track, we want to encourage more model producing solvers as these give higher confidence in the soundness of the result.

For the model validation track, we are requiring the model to be given in SMT-LIB format.  In particular, abstract model values, i.e. those for uninterpreted constants and functions, need to be given in the form `(as @identifier Sort)`.  Function definitions must not be recursive and must only contain parameter variables, model values, and theory-defined functions. The model validator will not support cardinality constraints (which are not necessary for quantifier-free formulas). If these are given they must be guarded by a comment.  Two abstract model values with different names are assumed to be not equal. Solvers should also no longer output the non-standard `model` keyword, although the pre-processor will probably still allow it for this competition. Example:

```
(; U is sort of cardinality 2
 (define-fun a () U
    (as @0 U))
  (define-fun b () U
    (as @1 U))
  (define-fun f ((x U)) U
    (ite (= x (as @1 U)) (as @0 U)
      (as @1 U))))
```

We would be delighted to receive community's feedback on the suggestions, and take this opportunity to wish a happy holiday season for everybody who celebrates.


Best regards,

Haniel Barbosa, Jochen Hoenicke (chair), and Antti Hyvärinen