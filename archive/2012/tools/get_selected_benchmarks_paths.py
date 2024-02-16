#!/usr/bin/env python

"""
Given a list of benchmark IDs and a file in the format used for SMT-COMP
benchmark selection, prints the paths of the selected instances
"""

import os, sys


def usage():
    sys.stdout.write("Usage: %s benchmarks-file selected-ids-file\n" % os.path.basename(sys.argv[0]))
    sys.exit(1)


def main():
    if len(sys.argv) != 3:
        usage()

    with open(sys.argv[2]) as f:
        selected = set(int(l) for l in f)

    pr = sys.stdout.write
    with open(sys.argv[1]) as f:
        f.readline()  # skip the first line with the count
        for line in f:
            bits = line.split()
            bench_id = int(bits[5])
            if bench_id in selected:
                pth = "%s/%s/%s" % (bits[0], bits[1], bits[-1])
                pr(pth)
                pr("\n")


if __name__ == "__main__":
    main()
