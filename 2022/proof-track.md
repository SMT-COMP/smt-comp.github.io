## Proof Exhibition Track

In the new Proof Exhibition Track, teams can submit a proof-producing solver
together with a proof checker for its proof format.  We will compile and
present the results, as well as assemble a panel of experts (not necessarily
organizers) to do a qualitative assessment for each proof-producing solver,
proof format, and proof checker.

### Solver Script for StarExec

Solver authors should provide two scripts with their solver.  The first
script called `smtcomp_solver`, should take the name of the
benchmark file as a single argument and run the solver on the benchmark.

As usual the benchmark is pre-processed, i.e., the identifiers are randomized
and the commands for producing proofs are added to the benchmark.  The solver
needs to understand the option `:produce-proofs` and the command `(get-proof)`.
Solvers must respond to each command in the benchmark script with the answer
defined in the SMT-LIB format specification.  There will be a `(check-sat)`
command for which `unsat` should be output and a `(get-proof)` command for
which the proof should be given as an s-expression according to the
SMT-LIB standard (the format is not specified otherwise).
Solvers that respond `unknown` to the `(check-sat)` command should respond
with an error to the following `(get-proof)` command.  Note that the error
result must be output to stdout.
In contrast to other tracks, anything written to stderr is ignored and the
output is saved for diagnostic purposes.

### Proof Checker Script for StarExec

The second script, `smtcomp_checker`, should take
the benchmark file name as first argument and the stdout output of the
solver script as second argument.  Note that this output will
usually start with the `unsat` result of the `(check-sat)`
command, which the checker must either parse or skip.

The checker should check the proof within the output and provide the result
to stdout.  Output printed to stderr is ignored (and saved for diagnostics).
The first line of the proof checker result should be either
`valid`, `invalid`, `holey`, `sat`, or `unknown`.
The answer `valid` must only be given when the checker certifies that the
given proof justifies the unsatisfiability of the given benchmark.
A checker that returns `valid` to a satisfiable benchmark is deemed to be
unsound.
The answer `invalid` should be returned if the proof is errorneous or
otherwise malformed.
If the proof checker determines that the proof is valid but it contains
holes, i.e., steps that are not checked for correctness, the answer should
be `holey`.
The answer `sat` should be given if the solver claimed that the benchmark
is satisfiable and `unknown` should be given if (1) the solver answered
`unknown`, (2) it answered `unsat` but did not give a proof, or (3) the
solver gave an error result.

After the first line, the proof checker can provide arbitrary `key=value`
pairs.  These will be collected in the final result table and can include
for example information about the number of proof steps, the number of nodes
in the proof, the number of holes, the number of different proof rules, etc.

### Evaluating the Results

The result of a solver is considered erroneous if the proof checker
returns `sat` or `invalid`.
Since the proof exhibition track is non-competitive and we are not fixing
the definition of a valid proof, there will be no score computed for this
track.

A proof checker is unsound if it returns `valid` for an (invalid) proof
of a satisfiable benchmark.
Thus, a proof checker must also check that the formula that was proved
corresponds to the benchmark given.  Soundness of the proof checker is
a central criterion by which the participants will be judged.

### Time Limit.

This track will use a wall-clock time limit of 20 minutes per
solver/benchmark pair.  This time limit includes the time for proof checking.
We will record the times for each stage.

### Wrapper

Solvers in this track will be wrapped in the competition to include the script
[starexec_run_proof](https://github.com/SMT-COMP/postprocessors/tree/master/proof-track/starexec_run_proof).  This script will call the solver
and checker script.

You can submit a single solver for all tracks, by providing a
`starexec_run_default` script for the other tracks and the
`smtcomp_solver` and `smtcomp_checker` scripts for the
proof exhibition track.  You can also include the script
`starexec_run_proof` so that the configuration for the proof
track is created.

### Key-Value Pairs

As mentioned above the proof checker can add arbitrary key-value pairs
that will be collected in the results.  To standardize the results, we
will at a later time propose some key-value pairs, that proof checkers
should print.  Please check this page for updates.

