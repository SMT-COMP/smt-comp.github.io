## Benchmark Selection

The benchmark selector used for 2012 is a slight modification of the one used for 2011.

<h3>Benchmark Eligibility</h3>

The rules for benchmark eligibility are summraized here, but stated more
completely in the <a href="rules12.pdf">rules document</a>.

First, benchmarks that are of `unknown` status are ineligible.

Benchmarks that are &ldquo;too easy&rdquo; are similarly ineligible.  &ldquo;Too easy&rdquo;
is understood to mean that all of last year's solvers can solve the benchmark correctly
in 5 seconds or less.  However, if removing such benchmarks leaves a division with fewer
than 300 eligible (non-check) benchmarks, then the easiest benchmarks are removed until
300 non-check benchmarks remain.

The organizers reserve the right to remove from competition eligibility
uninteresting or over-represented benchmarks.

<h3>Selection Algorithm</h3>

For each division, the `check` benchmarks are always included. In addition, the selection script will randomly select 200 benchmarks from each division with the following distribution (when possible): 170 `industrial`, 20 `crafted`, and 10 `random`.
In each category, the script selects (when possible):

- 10% `sat` with difficulty on the interval [0,1].
- 10% `sat` with difficulty on the interval (1,2].
- 10% `sat` with difficulty on the interval (2,3].
- 10% `sat` with difficulty on the interval (3,4].
- 10% `sat` with difficulty on the interval (4,5].
- 10% `unsat` with difficulty on the interval [0,1].
- 10% `unsat` with difficulty on the interval (1,2].
- 10% `unsat` with difficulty on the interval (2,3].
- 10% `unsat` with difficulty on the interval (3,4].
- 10% `unsat` with difficulty on the interval (4,5].

If there aren't enough `random` and `crafted` benchmarks, then
the slack is &ldquo;inherited&rdquo; by the `industrial` category.
It there aren't enough `industrial` benchmarks, then the slack
is &ldquo;inherited&rdquo; by the `crafted` category.
As a last resort, and only if necessary (as in divisions with only random
benchmarks), `random` benchmarks are allocated additional slots.

More detail on this procedure is included in a comment at the top of the
source file.  A less algorithmic description can be found in the
<a href="rules.shtml">official rules</a>.

<h3>Tool Download</h3>

- [select_benchmarks](tools/select_benchmarks_2012.c): Given an input file of benchmarks, selects benchmarks according to the rules; statistics on stderr, benchmarks on stdout.  Some changes may be made to this program before it is used officially for the competition benchmark selection; it is intended that these changes be limited to bug fixes, removal of obsolete debugging code, and documentation cleanups.
- [Eligible Benchmarks](smtcomp2012-eligible.txt.bz2): These are the eligible 2012 benchmarks for inclusion.  This file lists SMT-COMP 2012 benchmarks and their metadata.
- [All Benchmarks](smtlib2012-benchs.txt.bz2): this is the total list of 2012 benchmarks, including ineligible benchmarks.
