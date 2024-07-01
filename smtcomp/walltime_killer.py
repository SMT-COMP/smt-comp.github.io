#!/usr/bin/env python3

import sys

sys.path.insert(0, "benchexec")

from benchexec.runexecutor import RunExecutor
import logging

logging.basicConfig(level=logging.ERROR)


def main():
    if len(sys.argv) < 3:
        print("Usage: ./walltime_killer.py WALLTIME COMMAND")

    outfile = "runexec_output.log"

    executor = RunExecutor(use_namespaces=False)
    result = executor.execute_run(
        args=sys.argv[2:], walltimelimit=int(sys.argv[1]), output_filename=outfile, write_header=False
    )

    try:
        with open(outfile) as f:
            for line in f.readlines():
                print(line)
    except Exception as e:
        pass

    if result.get("terminationreason") == "walltime":
        print("TIMEOUT")
        exit(9)

    exit(result["exitcode"].raw)


if __name__ == "__main__":
    main()
