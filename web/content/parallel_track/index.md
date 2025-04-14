+++
title = 'Parallel Track'
date = 2024-05-07T10:09:02+01:00
draft = false
aliases = ['/parallel-and-cloud-tracks.html', '/parallel-track.html']
+++

## Parallel Track

Like last year we are organising an experimental parallel track for
SMT-COMP. Similar tracks were organised in the SAT competition 2020
and the competition had a positive impact on the development of
parallel SAT solvers (see <https://satcompetition.github.io/2020/>).

### The Concept

The goal in the parallel track is to measure the success of a solver in
solving a single, hard instance. This will be done by giving solvers instances
one at a time, similar to the SMT-COMP single-query track. The participating
solvers will be scored based on the number of instances that a solver solves
within the per-instance wall-clock time limit and the total run time, similar to
the single-query track’s parallel score.

For this track we need to choose in total 400 benchmarks from the single-query
track logics, and we are specifically reaching out to you, the community and
especially the competitors, for suggesting suitable instances to be included in
the tracks. In addition we will try to identify instances that are considered
interesting. All instances should come from the SMT-LIB benchmark library.

The solver submission rules follow those of the rest of the tracks. However, on
this track we **do accept** portfolio solvers, as defined in the rules, as
competitors. We encourage submission of non-portfolio solvers and reserve the
right to give special mentions to non-portfolio solvers in reporting the
results.

### Solver execution

The solvers participating in this track will be executed with a wall-clock time
limit of 20 minutes, thus similar to the Single Query Track. Each solver will be
run on a single machine with 256 virtual cores and 2 TB of memory.

### Submission

The submission process for the Parallel track is the same as for the other
tracks. In particular, the participants should follow the [submission process
using GitHub](solver_submission).

### Cloud track

During previous years, we also organized a Cloud track where the solvers were
executed on a large distributed cloud. This track is not a part of SMT-COMP 2025
due to the lack of suitable execution infrastructure. We hope it will return next year.
