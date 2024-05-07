from pathlib import Path
from rich.progress import track
import subprocess
import concurrent.futures

def scramble_file(files: list, line: int, dstdir: Path, scrambler: Path, options: str, seed: int) -> None:
    dst = Path.joinpath(dstdir, "scrambled" + str(line) + ".smt2")
    subprocess.run([scrambler, options],stdin=Path(str(files[line]).strip()).open('r'), stdout=dst.open('w'))

def scramble(track: str, benchmark_list: Path, dstdir: Path, scrambler: Path, seed: int, max_workers: int) -> None:
    options = ""
    if track == "sequential":
    	options = "-term_annot pattern -seed " + str(seed)
    elif track == "incremental":
    	options = "-term_annot pattern -incremental true " + "-seed " + str(seed)
    elif track == "model-validation":
        options = "-term_annot pattern -gen-model-val true " + "-seed " + str(seed)
    elif track == "unsat-core":
        options = "-term_annot pattern -gen-unsat-core true " + "-seed " + str(seed)
    else:
        rich.print(f"[red]Not a known track name: {track}[/red]")
        exit(1)
    line  = int(0)
    files = benchmark_list.open().readlines()
    dstdir.mkdir(parents=True, exist_ok=True)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    results = list(track(
        executor.map(lambda line: scramble_file(files, line, dstdir, scrambler, options, seed), range(len(files))), total=len(files), description="Scrambling selected benchmarks..."))
    executor.shutdown()
