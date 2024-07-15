# SMT Competition

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

On Debian/Ubuntu installation a virtual env (here in .venv) is needed:

```
python3 -m venv .venv
source .venv/bin/activate
```

Poetry is used for handling dependencies:

```
pip install "poetry >=2.1.2"
```

Finally, install the environment with

```bash
make install
```

## For starting a new SMT-COMP year

Edit the file `smtcomp/defs.py`, in particular `Config.current_year`, `Logic` for adding new logics and `tracks` for new divisions. Reset `Config.NYSE_seed` to `None`, and set the date the New York Stock Exchange Index will be used in `Config.NYSE_date`.

Download the new benchmarks from zenodo, unpack them, unpack the .tar.zst, you should get something like:

```
$DIR/zenodo
├── incremental
│   ├── ABVFPLRA
│   ├── ALIA
│   ...
│   ├── UFNIA
│   └── UFNRA
└── non-incremental
    ├── ABV
    ├── ABVFP
    ├── ABVFPLRA
    ├── ALIA
    ├── ANIA
    ├── AUFBV
    ...
    ├── UFFPDTNIRA
    ├── UFIDL
    ├── UFLIA
    ├── UFLRA
    ├── UFNIA
    └── UFNIRA
```

Then you can run (very io intensive):

```
smtcomp create-benchmarks-list $DIR/zenodo ./data/
```

The directory `./data/` is the one present in this repository.

## Using the `smtcomp` tool for selecting the benchmarks

The list of benchmarks and the previous results are in `json` which are human-readable, but slow to parse (1min). So locally the tool use the feather format. The
feather files are generated with:

```
smtcomp create-cache ./data/
```

Working with the feather files with [polars](https://docs.pola.rs/) is very fast,
so no more intermediate files are needed.

However, statistics can be shown, for example for the selection of single track:

```
smtcomp show-selection-stats --track SingleQuery ./data/
```

Which outputs:

```
          Statistics on the benchmark selection for single query
┏━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┓
┃ Logic         ┃ trivial ┃ not trivial ┃ old never ran ┃  new ┃ selected ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━┩
│ ABV           │       0 │        2573 │          2402 │    0 │     2487 │
│ ABVFP         │       0 │          60 │             0 │    0 │       60 │
│ ABVFPLRA      │       0 │          77 │             0 │    0 │       77 │
│ ALIA          │      23 │        1545 │          1530 │    0 │     1537 │
│ ANIA          │       0 │          56 │             0 │   22 │       78 │
│ AUFBV         │       0 │        1333 │           190 │    0 │      761 │
│ AUFBVDTLIA    │     115 │        1434 │           134 │    0 │      784 │
...
```

## Using the `smtcomp` tool for generating `benchexec` configuration

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
smtcomp download-archive submissions/*.json ../tmp/execution
```

Trivial tests benchmarks generated with:

```
smtcomp generate-trivial-benchmarks ../tmp/execution/benchmarks
```

The benchexec execution environment generated using:

```
smtcomp prepare-execution ../tmp/execution
```

The benchmarks can be selected by running

```
smtcomp select-and-scramble SingleQuery ./data/ $DIR/zenodo ../tmp/execution SCRAMBLER_EXECUTABLE [--test]
smtcomp select-and-scramble Incremental ./data/ $DIR/zenodo ../tmp/execution SCRAMBLER_EXECUTABLE [--test]
smtcomp select-and-scramble ModelValidation ./data/ $DIR/zenodo ../tmp/execution SCRAMBLER_EXECUTABLE [--test]
smtcomp select-and-scramble UnsatCore ./data/ $DIR/zenodo ../tmp/execution SCRAMBLER_EXECUTABLE  [--test]
```

Use the `--test` switch if you want to select and scramble only a small number of easy benchmarks for each logic.

The benchexec tasks generated using:

```
smtcomp generate-benchexec submissions/*.json ../tmp/execution
```

Benchexec started using:

```
(cd ../tmp/execution; PYTHONPATH=$(pwd) benchexec run_definitions/SOLVERNAME.xml --read-only-dir / --overlay-dir /home --full-access-dir .. --numOfThreads 8 -M 2GB -c 1)
```

Benchexec in verifier cloud started using:

```
(cd ../tmp/execution; PYTHONPATH=$(pwd) PATH_TO_BENCHEXEC/contrib/vcloud-benchmark.py run_definitions/SOLVERNAME.xml --read-only-dir / --overlay-dir /home --full-access-dir .. --numOfThreads 8 -M 2GB -c 1 --vcloudMaster VCLOUD_MASTER --vcloudClientHeap 500)
```

<<<<<<< HEAD
## Using the `smtcomp` tool for handling `benchexec` results

All the track are similar, except model validation and unsat core needs some additional work to check the output of the solvers. Lets start with the simple case:

## Single Query

We will suppose that the results are locally available in directory `tmp/final_results`:

For example using rsync if `sosy` is configured in `.ssh/config`:

```
rsync sosy:/localhome/smt-comp/final_results -ra tmp/ --progress --exclude="*.logfiles"
```

The `original_id.csv` file generated at the same time that the scrambled benchmarks is needed in the results directory (even if we can recompute it, we use this one for safety):

```
scp sosy:/localhome/smt-comp/execution/benchmarks/files/original_id.csv tmp/final_results/
```

In order to allow looking at the results incrementally, the first step is to translate each `.xml` into a faster `.feather` file. The translation is done only for `.xml` without a corresponding `.feather` file.

```
smtcomp convert-benchexec-results tmp/final_results
```

Information on missing results can be obtained using:

```
smtcomp stats-of-benchexec-results data tmp/final_results SingleQuery
```

Computation of the scores can be obtained for the different way (parallel, sequential, sat, unsat, twenty-four seconds):

```
smtcomp show-scores data tmp/final_results/ [par|seq|sat|unsat|24]
```

Once all the results are available, they can be stored in `data/results-sq-{year}.json.gz`:

```
smtcomp store-results data tmp/final_results
```

(If the results of a track are in multiple directories they should all be given at the same time)

As usual the `.feather` cache need to be computed (`--only-current` create only the cache of the current year):

```
smtcomp create-cache data --only-current
```

Now the `tmp/final_results` directory is not needed anymore, since it will look into `data` for the current year results.

# Model Validation

It is the same than Single Query except we need to check the models. It is done using dolmen.

Compilation of dolmen (requires docker):

```
smtcomp build-dolmen data
```

The model validation needs the scrambled files:

```
rsync -ra sosy:/localhome/smt-comp/execution/benchmarks/files_model tmp/benchmarks/ --progress
```

The verification takes around 4hours (mainly because the validation of some models timeout):

```
smtcomp check-model-locally data tmp/ tmp/final_results_model/ --outdir tmp/bad_models_final/ --max-workers 13
```

(Only the validation of new results is computed)

The directory `tmp/bad_models_final/` contains for each solver the models that are not validated with the corresponding scrambled benchmark and the output of dolmen.

The step from Single Query can be followed with the model validation results whenever you want partial results (even before validating the models), but `store-results` should be done only when the model validation has been attempted for all the results. Moreover the "\*.feather" file in the subdirectories must be manually removed after validating new models before `convert-benchexec-results` (TODO invalidate the feather file cache automatically?)

Tasks for unsat core validation can be generated by:
```
smtcomp generate-unsatcore-validation-files ../tmp/execution SCRAMBLER_EXECUTABLE UNSAT_CORE_RESULT_DIR/*/*
```

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).

## Using the `smtcomp` tool for handling results for Cloud and Parallel tracks provided in `csv` format by AWS

Works the same for both Parallel and Cloud track. If only one csv file is provided, the file needs to be split into one just containing the results for the relevant track. Furthermore, the file must be called results.csv, stored in its own local directory (here tmp/cloud_results), and contain at least the columns: solver, scramble_id, logic, solver_time, file, track, and solver_result.

We will suppose that results.csv is locally available in directory `tmp/cloud_results`:

In order to allow looking at the results incrementally, the first step is to translate the `.csv` file into a faster `.feather` file.

```
smtcomp convert-aws-results tmp/cloud_results
```

Everything else works the same as for any feather file that was converted by `smtcomp convert-benchexec-results`.
