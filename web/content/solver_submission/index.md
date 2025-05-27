+++
title = 'Solver Submission'
date = 2024-02-16T22:38:03+01:00
draft = false
+++

The solvers are submitted via pull requests to the [SMT-COMP repository](https://github.com/SMT-COMP/smt-comp.github.io/tree/master/submissions). To
submit your solver, please follow the instructions that are below.

The solver is run in [this docker](https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines) environment.

## Changes

- 05/2025: the final field must be set for the final version. When final is set, the archive need to come from zenodo.

## Submissions directory

The creation of new submission is done through the creation of a new json file
in this directory and the submission of a Pull Request.

It could be done directly from the web-interface and starting with a template:
[create a new submission](https://github.com/SMT-COMP/smt-comp.github.io/new/master/submissions?value={{< submissions_template >}})

- The filename should start with the name of your solver and end with `.json`.
- The continuous integration will:
- check the format
- try to download your solver
- run it inside the docker used by the competition on trivial example

### Examples

The detailed description of the fields in the solver JSON file is available in the [schema](schema.html).
