#!/usr/bin/env python

import MySQLdb
import os, sys
import math, csv
from dbdata import *


results_job_query = """\
select
        -- fix the QF_ABV <-> QF_AUFBV issue
        IF(divisions.name='QF_ABV', 'QF_AUFBV', divisions.name) as division,
        benchmarks.file as file,
        results.solversolution as solversolution,
        results.solverid as solverid,
        solvers.displayname as solvername,
        results.jobid as jobid,
        results.correct as correct,
        results.time as time,
        benchmarks.solution as solution,
        benchmarks.revision as revision,
        benchmarks.category as category,
        benchmarks.difficulty as difficulty,
        benchmarks.benchmarkid as benchmarkid
from
        results, benchmarks, divisions, solvers
where
        results.benchmarkid=benchmarks.benchmarkid
        and benchmarks.divisionid=divisions.divisionid
        and solvers.solverid=results.solverid
        and (results.jobid=962 or results.jobid=930 or results.jobid=970)
        and results.solverid != 1331
        and results.correct != 'N'
order by
        division, benchmarks.file, results.solverid
-- limit 20
"""


def get_difficulty(times_in_seconds):
    A = 30
    minutes = [min(t / 60.0, 30.0) for t in times_in_seconds]
    minutes.sort()
    if len(minutes) >= 5:
        minutes = minutes[1:-1]
    if minutes:
        A = sum(minutes) / float(len(minutes))
    difficulty = (5.0 * math.log(1.0 + A**2)) / (math.log(1.0 + 30**2))
    return round(difficulty, 3)


def get_solution(sols, benchsol):
    if benchsol in ("sat", "unsat"):
        return benchsol
    else:
        if len(sols) > 1 and len(set(sols)) == 1:
            s = sols[0]
            if s in ("sat", "unsat"):
                return s
    return "unknown"


def warn(msg):
    sys.stderr.write(msg)


def main():
    db = MySQLdb.connect(db=SMTEXEC_DB, user=SMTEXEC_USER, passwd=SMTEXEC_PWD)
    c = db.cursor()
    c.execute(results_job_query, ())
    prevkey = None
    times = []
    sols = []
    entries = []
    excluded = 0
    for row in c:
        curkey = list(row[:2]) + [row[-1], row[10], row[8]]
        cursol = row[2].strip()
        if curkey != prevkey:
            if prevkey:
                difficulty = "%.3f" % get_difficulty(times)
                solution = get_solution(sols, prevkey[-1])
                if solution in ("sat", "unsat"):
                    division = prevkey[0]
                    family, filename = prevkey[1].split("/", 1)
                    benchid = prevkey[2]
                    category = prevkey[3]
                    entries.append([division, family, category, difficulty, solution, benchid, filename])
                else:
                    excluded += 1
                    pass
                    ## warn('EXCLUDING %s\n' % prevkey)
            prevkey = curkey
            times = []
            sols = []
        t = float(row[7])
        if cursol not in ("sat", "unsat"):
            t = 1800.0
        else:
            sols.append(cursol)
        times.append(t)

    if prevkey:
        solution = get_solution(sols, prevkey[-1])
        if solution in ("sat", "unsat"):
            difficulty = "%.3f" % get_difficulty(times)
            division = prevkey[0]
            family, filename = prevkey[1].split("/", 1)
            benchid = prevkey[2]
            category = prevkey[3]
            entries.append([division, family, category, difficulty, solution, benchid, filename])
        else:
            # warn('EXCLUDING %s\n' % prevkey)
            excluded += 1

    c.close()
    db.close()

    entries.sort()
    pr = sys.stdout.write
    pr("%d\n" % len(entries))
    for r in entries:
        pr("%s\n" % " ".join(map(str, r)))
    pr("END x industrial 0 sat 0 x\n")

    sys.stderr.write("created competition pool with %d / %d benchmarks\n" % (len(entries), len(entries) + excluded))


if __name__ == "__main__":
    main()
