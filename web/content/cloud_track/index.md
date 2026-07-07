+++
title = 'Benchmark Submission'
date = 2026-07-07T21:09:02+01:00
draft = false
+++

## SMT-COMP '26 Cloud track -


  Solver Submission Guide
This guide summarizes what solver authors need to do to submit to the SMT-COMP cloud track, based on the AWS competition infrastructure used for SAT-COMP and adapted for SMT-COMP.

## 1. Overview

The competition infrastructure runs solvers as Docker containers on AWS. It is **not SAT/SMT-specific** — the main work for solver authors is (a) packaging their solver in a Docker container and (b) using the provided networking primitives if their solver is distributed.

Reference repository: [`aws-samples/aws-batch-comp-infrastructure-sample`](https://github.com/aws-samples/aws-batch-comp-infrastructure-sample)

**Important:** use the `mainline-2026` (default) branch of the repository.

## 2. What You Need to Provide

Each submission consists of:

1. A **Dockerfile** that builds your solver.
2. A **`solver_cmd.py`** script that returns the command-line arguments used to invoke your solver.

Both files should live in a **top-level directory named `aws-build`** inside your own solver's repository (which should also contain your solver's source). This makes it easy for organizers to clone your repo, extract the `aws-build` contents, and build your image.

## 3. Requirements

- **Build from source.** For security, the Dockerfile must build the entire solver from source.
- **Dependencies.** Only standard package managers (e.g., `apt-get`) may be used to install dependencies.
- **Source code.** Provide source directly, or use `git clone` inside the Dockerfile — the referenced repository **must be open source**.
- **Base image.** Your Dockerfile must extend the base Dockerfile provided in the sample repo, which sets up common dependencies and the solving harness.
- **Single Dockerfile for distributed solvers.** Even for distributed solvers, you provide one Dockerfile. The harness detects at startup whether a given machine is the leader or a worker node.
- **Exit codes.** Your solver must return:
  | Result | Exit Code |
  |--------|-----------|
  | SAT | 10 |
  | UNSAT | 20 |
  | UNKNOWN | 0 |
  | Error | any other value |

  The harness relies on these codes to report results, so this step is critical.

## 4. Distributed Solvers

- Only the **leader node** is invoked when a new problem arrives; it is responsible for invoking the solver on all other machines in its group.
- Worker nodes idle in the harness until they receive a cleanup signal.
- Machines communicate via **SSH or MPI** over a VPC.
- The leader node receives the IP addresses of all machines belonging to its solver instance.
- A sample distributed `solver_cmd.py` is provided in the repository's documentation.

## 5. Input Files & Harness Behavior

- The harness is solver-agnostic: it downloads the benchmark from S3 into the container and passes it to your solver.
- Expected file extensions: `.cnf` or `.smt2` (compressed versions are automatically decompressed).
- The harness lets your solver run until **timeout** or **memout**.

## 6. Underlying AWS Architecture (for context/debugging)

You don't need to understand this to submit, but it helps when debugging:

- **ECR** — builds/stores your Docker image
- **ECS** (on EC2) — runs copies of your image
- **S3** — stores benchmark files
- **SQS** — queues problems to solve; each message links to an S3 file
- **VPC** — networking between distributed solver instances
- **DynamoDB** — tracks machine status

Full architecture details are in the repository's documentation folder.

## 7. Steps to Submit

1. Modify your solver to return the correct exit codes (see §3).
2. Prepare your **Dockerfile**, extending the provided base image.
3. Prepare your **`solver_cmd.py`**.
4. Configure a **YAML file** describing your solver for the harness.
5. **Build and test locally** using the provided `satcomp.py` script (heavily recommended before submitting). Note: an `smtcomp.py` alias may be made available on request.
6. *(Optional but strongly encouraged)* **Test on AWS.** This requires an AWS account. You are responsible for your own AWS costs — testing prudently should cost well under $100. Free AWS credits *may* be available to competitors, but this is unconfirmed.
7. Submit your repository (containing your solver source plus the `aws-build/` directory with your Dockerfile and `solver_cmd.py`) to the organizers.

## 8. Timeouts & Machine Specs

- **Cloud track timeout:** organizers recommend **200 seconds** (based on SAT-COMP's move from 5000s → 200s, which cut compute costs ~20x with no change in results).
- **Parallel track timeout:** **1000 seconds** (reduced from 1200s, again with no change in results).
- **2024 reference hardware** (SMT-COMP cloud track): 100× `m4.4xlarge` instances in parallel, each with 16 vCPUs (8 cores) and 64 GB memory.

## 9. Deadlines

| Milestone | Date |
|---|---|
| Preliminary deadline | **July 7, 2026** |
| Final deadline | **July 21, 2026** |

- By **July 7**, your solver should compile and pass basic tests within the framework — this gives organizers time to confirm everything builds and integrates correctly.
- Organizers will **re-clone repositories on July 21** for the final submission, so keep your repo (and its open-source status) intact through that date.

## 10. Open Source Requirement

Keep your repository **public/open source at least through the final deadline**. Organizers plan to copy all submissions (including cloned source) into a competition monorepo (e.g., `2026-submissions`), partly because past competitors have made their repos private after the competition ended.

## 11. Questions

Direct questions to the SMT-COMP cloud track organizers.

