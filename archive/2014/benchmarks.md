## Benchmarks

The SMT Competition will use a subset of the benchmarks available within SMT-LIB, as described
in the competition rules. New benchmarks are especially encouraged by the May 15 deadline. The set of benchmarks will be announced as soon as is feasible after that deadline. Please adhere to the following instructions in submitting new benchmarks:

- Benchmarks should be organized into separate directories by logic.
- Within each logic, there should be one or more directories containing
the benchmarks - you can choose the names of the directories, but they
should be different from any names currently existing in SMT-LIB for
that logic.
- Each benchmark should contain the following metadata:
<PRE>
(set-logic &lt;logic&gt;)
(set-info :source |&lt;information about where the benchmark came from
including author contact, paper citations, etc.&gt;|)
(set-info :smt-lib-version 2.0)
(set-info :category &lt;either "industrial", "crafted", or "random"&gt;)
(set-info :status &lt;either sat, unsat, or unknown&gt;)
</PRE>
In :category, the quotes are needed in the benchmark file.

Thanks to the following for new benchmarks in 2014:
- Clark Barrett
- Philipp Wendler -rec'd
- Aaron Tomb et al. (Galois) -rec'd
- Gergely Kovasznai
- Matthias Heizmann
- Hristina Palikareva
-  ...

### Benchmark Set And Difficulty Measurements

The benchmarks used in the competition are selected from the
SMT-LIB benchmark set. The complete set is reduced by a few restrictions:
- The correct result (sat or unsat) must be known
- Trivial benchmarks defined in the rules as those that are quickly solved by all solvers in the previous competition or evaluation.
- Any random selection is biased toward benchmarks categorized as "industrial" and toward more difficulty benchmarks.

For the last point a measurement of difficulty is needed. This is an approximate measure meant simply to make the competition more challenging. For 2014 we used the value of the fastest solver on that benchmark in the 2013 evaluation. For benchmarks introduced since then, an approximate value was determined by taking the best value from running one or more solvers from the evaluation during the
preparation for the 2014 competition.

The table from which benchmarks will be chosen for the competition is available <a href="difficulties-2014.txt">here</a>.
The table will be updated during the course of preparing for the competition as benchmarks are corrected, removed because they are ill-formed or inappropriate, moved among logics as needed, or difficuly or expected results determined.


The table is in space-separated form that is very amenable to text processing tools such as awk, grep and sort. You can turn it into a comma-separated table for Excel or similar tools by using sed or tr to turn spaces into commas.


The columns in the table are these:

1. **id** - the StarExec benchmark id. Note that this id will change if the benchmark is corrected. This is happening frequently during the preparation for the competition. The ids will be resynchronized with StarExec just prior to the final selection.
2. **difficulty** - this value is in seconds, or is one of the words "trivial" or "unknown". "trivial" benchmarks are those that have been determmined to be easy for every solver and so excluded by the rules. "unknown" means the difficulty value has not yet been determined. Valaues of 1500 or 1600 generally indicate that all solvers quit without a result (timeout or memout).
3. **starexec-expected-result** - this is the metadata value from StarExec and is the correct value expected for the benchmark. This should be one of
"sat", "unsat" or "unknown" (without the quotes). However, ther eare also values of "null" (metadata value is not set).
4. **status** - this is the :status value from the benchmark, as recorded in the StarExec metadata. It should be precisely the same as the starexec-expected-result.
5. **category** - this is the :category value as recorded in StarExec metadata, which should have determined it from a set-info command in the benchmark. This value should be one of "industrial", "crafted", "random", or "check" (without the quotes). Values of "null" (category not set), "unknown" (category explicitly set to the value "unknown"), and "none" (value in StarExec is an empty string) are also present.
6. **logic** - the SMT-LIB logic
7. **path** - the path of the benchmark within the non-incremental subspace of benchmarks.
