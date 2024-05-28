+++
title = 'Machine Specifications'
date = 2024-05-28T08:08:10+02:00
draft = false
+++

The single query, incremental, unsat-core, and model-validation tracks we will
run on the [VerifierCloud
cluster](https://vcloud.sosy-lab.org/cpachecker/webclient/master/info) owned by
LMU's Software and Computational Systems Lab
([SoSy-Lab](https://www.sosy-lab.org/)), who are kind enough to support our
competition with their computing power. The cluster is also used for
[Competition on Software Verification (SV-COMP)](https://sv-comp.sosy-lab.org/).

To be more precise, the competition will be run on the 168 apollon nodes of the
cluster. Each of the nodes is equipped with `Intel Xeon E3-1230 v5 @ 3.40 GHz`
CPU and 33 GB of RAM. Each processor has 4 cores, which will be available to the
solver.

It is also possible to locally emulate and test the computing environment on the
competition machines using the following instructions:
https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines
