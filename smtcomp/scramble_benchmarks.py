from pathlib import Path
from rich.progress import track
import subprocess
import concurrent.futures

def scramble_file(files: list, line: int, dstdir: Path, args: list) -> None:
    dst = Path.joinpath(dstdir, "scrambled" + str(line) + ".smt2")
    subprocess.run(args,stdin=Path(str(files[line]).strip()).open('r'), stdout=dst.open('w'))

def scramble(competition_track: str, benchmark_list: Path, dstdir: Path, scrambler: Path, seed: int, max_workers: int) -> None:
    args = []
    if competition_track == "single-query":
    	args = [scrambler,"-term_annot","pattern","-seed",str(seed)]
    elif competition_track == "incremental":
        args = [scrambler,"-term_annot","pattern","-incremental","true","-seed",str(seed)]
    elif competition_track == "model-validation":
        args = [scrambler,"-term_annot","pattern","-gen-model-val","true","-seed",str(seed)]
    elif competition_track == "unsat-core":
        args = [scrambler,"-term_annot","pattern","-gen-unsat-core","true","-seed",str(seed)]
    else:
        rich.print(f"[red]Not a known track name: {track}[/red]")
        exit(1)
    line  = int(0)
    files = benchmark_list.open().readlines()
    dstdir.mkdir(parents=True, exist_ok=True)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    results = list(track(
        executor.map(lambda line: scramble_file(files, line, dstdir, args), range(len(files))), total=len(files), description="Scrambling selected benchmarks..."))
    executor.shutdown()
