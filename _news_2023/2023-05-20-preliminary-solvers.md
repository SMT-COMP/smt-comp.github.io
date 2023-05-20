---
layout: news
author:
title: Preliminary Solvers
newsdate: 2023-05-20
---

# List of Preliminary Solvers

The [list of submitted solvers](/2023/participants.html) is online now.  If you submitted a solver, please check
that your solver was added to the intended tracks and divisions and check the other info
we have. Note that there are a few new logics this year.


## StarExec Test Runs

We have run [Test Jobs](https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=543250) on StarExec
with the submitted solvers.  Please check if the result from your solver are as expected.
You should check the summary and you can download the job output and
check for suspicious error messages for your solvers.  In particular
if your solved count is 0.  We only ran a few benchmarks per logic for
testing and only with a 2 minute timeout.  I suspect some of the
solvers still have problems in the starexec environment.

Note that the scoring is not always correct. The incremental job
cannot be scored by starexec, so it's normal that the summary shows 0
solved.  For this job you have to check the output, or download the
Job Info table.  For the other tracks, the scoring may also be wrong
if the benchmark does not have a known status.

You can download the Job Info table which contains a CSV file with all
benchmark/solver pairs, the expected result and the starexec result.
The Job output file contains all outputs for all runs including error
messages.

If your solver has problems in the StarExec environment, you can use
the [StarExec VM image](https://www.starexec.org/vmimage/) to debug
any problems.  You can also use this to compile your solver to ensure
it is compatible with the glibc version.  Alternatively use static
binaries or a CentOS-7 docker image for compilation.
