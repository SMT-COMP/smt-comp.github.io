# smtcomp

[![Release](https://img.shields.io/github/v/release/smtcomp/smtcomp.github.io)](https://img.shields.io/github/v/release/smtcomp/smtcomp.github.io)
[![Build status](https://img.shields.io/github/actions/workflow/status/smtcomp/smtcomp.github.io/main.yml?branch=main)](https://github.com/smtcomp/smtcomp.github.io/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/smtcomp/smtcomp.github.io/branch/main/graph/badge.svg)](https://codecov.io/gh/smtcomp/smtcomp.github.io)
[![Commit activity](https://img.shields.io/github/commit-activity/m/smtcomp/smtcomp.github.io)](https://img.shields.io/github/commit-activity/m/smtcomp/smtcomp.github.io)
[![License](https://img.shields.io/github/license/smtcomp/smtcomp.github.io)](https://img.shields.io/github/license/smtcomp/smtcomp.github.io)

Tools used for the organization of the SMT competition

- **Github repository**: <https://github.com/smtcomp/smtcomp.github.io/>
- **Documentation** <https://smtcomp.github.io/smtcomp/>

## Getting started with development in this project

```bash
git clone git@github.com:smtcomp/smtcomp.github.io.git
```

Finally, install the environment and the pre-commit hooks with

```bash
make install
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPi or Artifactory, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-poetry/features/codecov/).

## Using the smtcomp tool for generating benchexec

#### Generate submissions [Optional]
 The final solvers submitted during the smtcomp 2023 can be used:

```
smtcomp convert-csv tests/solvers_divisions_final.csv ../tmp/submissions
```

The generated files can be visualized using:

```
smtcomp show ../tmp/submissions/YicesQS.json
```

The solver downloaded using:

```
smtcomp download-archive ../tmp/submissions/*.json ../tmp/benchexec/cache
```

Trivial tests benchmarks generated with:

```
smtcomp generate-benchmarks ../tmp/benchexec/includes/ 
```

The benchexec tasks generated using:

```
smtcomp generate-benchexec ../tmp/submissions/*.json ../tmp/includes/all.xml ../tmp/benchexec/cache 
```

Benchexec started using:

```
(cd ../tmp/benchexec/includes; benchexec all.xml  --read-only-dir / --overlay-dir /home --full-access-dir .. --numOfThreads 8 -M 2GB -c 1)
```










---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
