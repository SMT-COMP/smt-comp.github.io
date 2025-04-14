+++
title = 'Solver Submission'
date = 2024-02-16T22:38:03+01:00
draft = false
+++

The solvers are submitted via pull requests to the SMT-COMP repository. To
submit your solver, please follow the
[instructions](https://github.com/SMT-COMP/smt-comp.github.io/tree/master/submissions).
The detailed description of the fields in the solver JSON file is available in
the [schema](schema.html).

The solver is run in [this docker](https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines) environment.

## Submissions directory

The creation of new submission is done through the creation of a new json file
in this directory and the submission of a Pull Request.

It could be done directly from the web-interface and starting with a template:
[create a new submission](https://github.com/SMT-COMP/smt-comp.github.io/new/master/submissions?value={{< submissions_template >}})

- The filename should start with the name of your solver and end with `.json`.
- The continuous integration will check the format.

### Fields

- `name`: The solver name should respect the guidelines in the given in the
  rules of the SMT-competition (derived solver, wrapper solver, ...)
- `authors`: UTF8 can be used.
- `url`: The url should be valid at the time of submission and during all the competition. The url should be at zenodo for the final submission.
