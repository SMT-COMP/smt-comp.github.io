from pathlib import Path
from rich.progress import track
import subprocess
import concurrent.futures

def scramble_file(files: list, line: int, dstdir: Path, scrambler: Path, seed: int) -> None:
    dst = Path.joinpath(dstdir, "scrambled" + str(line) + ".smt2")
    subprocess.run([scrambler, "-seed", str(seed)],stdin=Path(str(files[line]).strip()).open('r'), stdout=dst.open('w'))

def scramble(benchmark_list: Path, dstdir: Path, scrambler: Path, seed: int, max_workers: int) -> None:
    line  = int(0)
    files = benchmark_list.open().readlines()
    dstdir.mkdir(parents=True, exist_ok=True)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    results = list(track(
        executor.map(lambda line: scramble_file(files, line, dstdir, scrambler, seed), range(len(files))), total=len(files), description="Scrambling selected benchmarks..."))
    executor.shutdown()
