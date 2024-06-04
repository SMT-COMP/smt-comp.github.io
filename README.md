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
pip install poetry
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
smtcomp show-sq-selection-stats ./data/ 0
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
smtcomp download-archive ../tmp/submissions/*.json ../tmp/benchexec/execution
```

Trivial tests benchmarks generated with:

```
smtcomp generate-benchmarks ../tmp/benchexec/includes/
```

The benchexec tasks generated using:

```
smtcomp generate-benchexec ../tmp/submissions/*.json ../tmp/benchexec/includes/all.xml ../tmp/benchexec/execution
```

The benchexec execution environment generated using:

```
smtcomp prepare-execution ../tmp/benchexec/execution
```

Benchexec started using:

```
(cd ../tmp/benchexec/execution; benchexec ../includes/all.xml  --read-only-dir / --overlay-dir /home --full-access-dir .. --numOfThreads 8 -M 2GB -c 1)
```

Benchexec in verifier cloud started using:

```
(cd ../tmp/benchexec/execution; PATH_TO_BENCHEXEC/contrib/vcloud-benchmark.py ../includes/all.xml  --read-only-dir / --overlay-dir /home --full-access-dir .. --numOfThreads 8 -M 2GB -c 1 --vcloudMaster VCLOUD_MASTER --vcloudClientHeap 500)
```

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
