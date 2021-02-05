---
layout: news
author:
title: Preliminary Call for Solvers
newsdate: 2021-02-05
---
The submission deadline for the first version of the solvers is on May 30.  However, it is useful for the organizing team to know in advance which and how many solvers may be entering.  If you have not submitted a solver before, or if you think there may be unusual circumstances, we request that you let us know at your earliest convenience if you think you may be submitting a solver to SMT-COMP'21.  We require a system description for all submitted solvers as part of the submission of the final solver versions.

We have a few central changes to the competition rules with respect to previous years.

### Combining Multiple Logics into the Same Division

Previously, every logic was its own division.  There are currently over 60 logics in SMT-LIB, which makes a short summary of the results impossible.  On the other hand the competition-wide scoring does a comparison between solvers that cannot be sensibly compared as they support completely disjoint logics. To get a better overview, we plan to have divisions combining related logics, thus reducing the number of divisions and obtaining more manageable and meaningful results.  Rather than logics, solvers would declare the divisions they enter, being ranked by the number of benchmarks they solve across all logics in the divisions entered.  We are aware that any partitioning of logics into divisions can be disadvantageous to some solvers that support some but not all logics in the division. We believe however that to a lesser extent this situation is already common, thinking of different features among problems in the same logic. So in our view the disadvantages are offset by the benefit of having a better presentation of the results. Regardless, results per logic will still be accessible within the results page of a given division, similarly to how one can now see the different scores other than sequential for a given logic.

A proposal for the new divisions and the rationale behind the partition is available at:

 - <https://hanielb.github.io/smt-comp.github.io/2020/>

How the results of SMT-COMP 2020 (for the single-query track) would have looked like with the above divisions can be seen in:

 - <https://hanielb.github.io/smt-comp.github.io/2020/results/results-single-query>

Note this is a coarse approximation, as for example a solver entering only QF_LRA, which could easily be extended to support QF_RDL, will not be well ranked on QF_LinearRealArith.

Also note that the results pages of the divisions do not contain the links to the individual results per logic, as they would in the 2021 results.

### Parallel and Cloud Tracks

We plan separate parallel and cloud tracks, which should demonstrate the potential of parallelizing solvers for solving a single large problem.  In the parallel track a solver is given a single benchmark and runs on a 64-core processor.  In the cloud track, the solver has access to multiple machines that communicate via network.  There will be another more detailed announcement, soon.

### Stricter Parsing of Solver Output

Under the previous rules, the status returned by the solver was determined by searching for `sat` or `unsat` somewhere in the solver output. This year, we require that this output must be the first output of the solver.  If the solver output does not start with `sat` or `unsat`, it is treated as unknown, i.e., it neither adds to the solved benchmarks nor will it add to the error score.  Solver authors need to make sure that any debugging output is disabled or redirected to a different stream (note that output on stderr is treated the same as output to stdout, so the run script should make sure to redirect output of stderr).
On the other hand, a solver producing an output with the wrong syntax will not be punished with the error score, which is reserved for unsound results.

### Option print-success is Always Set

Under the new rules the option `:print-success` will be set to `false` for the single-query, the model validation, and the unsat core track.  This will be the first command in the input file.  Since setting the option should take effect immediately, it should not be acknowledged by `success`.  This is important as the solver should not print anything before the `sat` or `unsat` result, as mentioned above.

This option can be used to determine if the solver should run in incremental mode.  If the option is set to true, the solver must support incremental commands, if it is set to false, the benchmark will never use incremental commands like push, pop, but follow the stricter rules for single query, model validation, or unsat core tracks in SMT-COMP.

Sincerely,

The organizing team

- Haniel Barbosa, Universidade Federal de Minas Gerais, Brazil
- Jochen Hoenicke (chair), Albert-Ludwigs-Universität Freiburg, Germany
- Antti Hyvärinen, Università della Svizzera italiana, Switzerland

