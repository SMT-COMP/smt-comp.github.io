from pathlib import Path
from rich.progress import track
import subprocess
import smtcomp.defs as defs

def scramble(scrambler: Path, seed: int,benchmark_list: Path, dstdir: Path) -> None:
    line = int(0)
    dstdir.mkdir(parents=True, exist_ok=True)
    with open(benchmark_list) as file:
        for benchmark_path in track(file, description="Scrambling selected benchmarks"):
            dst = Path.joinpath(dstdir, "scrambled" + line.strip() + ".smt2")
            subprocess.run([scrambler, "-seed " + seed],stdin=benchmark_path, stdout=dst)
            line++
