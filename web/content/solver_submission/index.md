+++
title = 'Solver Submission'
date = 2024-02-16T22:38:03+01:00
draft = false
+++

The solvers are submitted via pull requests to the [SMT-COMP repository](https://github.com/SMT-COMP/smt-comp.github.io/tree/master/submissions).

The solver is run in [this docker image](https://gitlab.com/sosy-lab/benchmarking/competition-scripts/#computing-environment-on-competition-machines), which is based on Ubuntu 24.04. The link also describes the packages that are installed in the image.

## Submissions directory

The creation of new submission is done through the creation of a new JSON file
in the `submission` directory of the repository and the submission of a pull
request. The filename should start with the name of your solver and end with
`.json`.

It could be done directly from the web interface and starting with a template:
[create a new submission](https://github.com/SMT-COMP/smt-comp.github.io/new/master/submissions?value={{< submissions_template >}})

The repository contains a continuous integration check that will

- check the format and all the required fields,
- try to download your solver,
- run it inside the docker container used by the competition on trivial examples,
- check that the final version of the solver is uploaded to Zenodo.

### Examples

For examples, take a look at the [last year's submissions](https://github.com/SMT-COMP/smt-comp.github.io/tree/smtcomp24/submissions).

The detailed description of the fields in the solver JSON file is available in the [schema](schema.html).

## Changes

- 05/2025: The field `final` must be set for the final version. When `final` is set, the archive URL needs to point to Zenodo.
