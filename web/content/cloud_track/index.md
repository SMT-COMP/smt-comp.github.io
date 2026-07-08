# Cloud Track

The cloud track of SMT-COMP '26 is run separately from all other tracks with its own procedures, infrastructure, deadlines, and result announcement.

### Key dates  
- **Jul 21, 2026** — preliminary call for solvers (should compile & pass basic tests).
- **Aug 8, 2026** — final call for solvers

All deadlines are 11:59 PM AoE (Anywhere on Earth).

### Submission Instructions 

#### Infrastructure 
[`aws-samples/aws-batch-comp-infrastructure-sample`](https://github.com/aws-samples/aws-batch-comp-infrastructure-sample) on the **`mainline-2026`** (default). 

*Each submission needs to be prepared according based on this repository.*

#### What to Submit
In your solver's repo, add a top-level **`aws-build/`** directory containing:
1. **Dockerfile** — must extend the provided base Dockerfile; build solver **from source**; dependencies only via standard package managers (e.g. `apt-get`); `git clone` allowed only for open-source repos.
2. **`solver_cmd.py`** — returns the command-line args used to invoke your solver.

Repo (including source) must stay **open source** at least through the final deadline.

#### Solver Requirements
- Return exit codes: **10 = SAT, 20 = UNSAT, 0 = UNKNOWN**, anything else = error.
- One Dockerfile handles both leader and worker nodes (harness detects role at startup). Only the leader is invoked per problem; it drives workers over **SSH/MPI**.
- Harness downloads benchmarks from S3 (`.cnf`/`.smt2`, compressed OK) and runs until timeout/memout.

#### Steps
1. Fix exit codes.
2. Write Dockerfile + `solver_cmd.py`.
3. Add YAML config describing the solver.
4. Build/test locally with `satcomp.py` (recommended before submitting).
5. *(Optional, encouraged)* Test on AWS — you cover costs, likely under $100.
6. Submit repo link (or tarball) with `aws-build/`.

#### Timeouts & Specs
- Cloud track timeout: **200s** (recommended, mirrors SAT-COMP).
- Parallel track timeout: **1000s**.
- 2024 hardware reference: 100x m4.4xlarge (16 vCPU / 8 core, 64GB RAM each).

### Contacts
- Cayden Codel — crcodel@amazon.com
- Robert Jones — rbtjones@amazon.com
