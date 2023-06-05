---
layout: news
author:
title: SMT-COMP 2023 is Live
newsdate: 2023-06-05
---
The SMT-COMP 2023 is live.  You can follow it on StarExec:

[https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=543471](https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=543471)

So far we have only started the single query track. The benchmark selected
for the other tracks will depend on the results of this track.  We will
add the jobs for the other tracks to the same space.

Note that the job summary is not always accurate:  Benchmarks with
unknown status are classified as unknown, even if the solver replied
with sat or unsat.  In the model validation track an error message in
the output is classified as wrong, even though our script classifies
it as unknown. We will use a script running on the Job Information
downloaded from the StarExec site and, especially in cases of
unsoundness, confirm manually whether the classification is correct or
not.
