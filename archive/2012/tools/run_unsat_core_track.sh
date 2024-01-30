#!/bin/bash
#
# Sample script for running the SMT-COMP 2012 unsat core track
#

# path to the scrambler (for constructing the "core" file)
SCRAMBLER=`dirname $0`/scrambler

SOLVER=$1
INSTANCE=$2

# base directory for storing the generated cores
COREBASEDIR=/tmp

n=`dirname $SOLVER`
SOLVERNAME=`basename $n`

d=`dirname $INSTANCE`
OUTDIR=$COREBASEDIR/$SOLVERNAME/$d

# create a directory for storing the core file
mkdir -p $OUTDIR

COREFILE=$OUTDIR/$INSTANCE.core.smt2
OUTFILE=$OUTDIR/$INSTANCE.output.txt

# execute the solver, get the output
$SOLVER $INSTANCE > $OUTFILE
s=$?

if [ $s -eq 0 ]; then
    # generate the core file
    $SCRAMBLER -core $OUTFILE < $INSTANCE > $COREFILE
    # print the number of assertions in the core
    head -1 $COREFILE | awk '/^;; parsed [0-9]+ names: .*/ { print $3 }'
fi

# return the exit code of the solver
exit $s
