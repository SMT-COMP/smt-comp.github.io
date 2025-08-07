import math
import functools, itertools
from collections import defaultdict
from typing import Set, Dict, Optional, cast, List, DefaultDict, Tuple
from pathlib import Path, PurePath
from smtcomp import defs

import polars as pl
import altair as alt
import smtcomp.scoring
from smtcomp.utils import *
import smtcomp.results

c_file = pl.col("file")
c_logic = pl.col("logic")
c_solver = pl.col("solver")
c_solver2 = pl.col("solver2")
c_answer = pl.col("answer")
c_cputime_s = pl.col("cputime_s")
c_cputime_s2 = pl.col("cputime_s2")
c_run = pl.col("run")
c_bucket = pl.col("bucket")
c_bucket2 = pl.col("bucket2")


def output_for_logic(config: defs.Config, results: pl.LazyFrame, logic: defs.Logic, output_dir: Path) -> None:
    results = results.filter(c_run == True, c_logic == int(logic)).select(
        c_file,
        c_solver,
        c_answer,
        c_cputime_s,
        bucket=pl.lit(10.0).pow(c_cputime_s.log(10).floor()),
        # bucket=c_cputime_s.log(10).floor(),
    )
    results_with = results.select(c_file, solver2=c_solver, bucket2=c_bucket, cputime_s2=c_cputime_s)
    results = results.join(results_with, on=c_file, how="left")

    corr = (
        results.group_by(c_solver, c_solver2)
        .agg(corr=pl.corr(c_cputime_s, c_cputime_s2, method="pearson"))
        .sort(c_solver, c_solver2)
    )

    results = results.group_by(c_solver, c_solver2, c_bucket, c_bucket2).len().sort(c_solver, c_solver2)

    df_corr, df_results = pl.collect_all([corr, results])

    row1 = df_corr.row(1, named=True)

    # Create heatmap with selection
    select_x = alt.selection_point(fields=["solver"], name="solver1", value=row1["solver"], toggle=False)
    select_y = alt.selection_point(fields=["solver2"], name="solver2", value=row1["solver2"], toggle=False)
    g_select_provers = (
        alt.Chart(
            df_corr,
            title="Click a tile to compare solvers",
            height=250,
            width=250,
        )
        .mark_rect()
        .encode(
            alt.X("solver", title=None),
            alt.Y("solver2", title=None),
            alt.Color("corr", scale=alt.Scale(domain=[-1, 1], scheme="blueorange")),
            opacity=alt.when(select_x, select_y).then(alt.value(1)).otherwise(alt.value(0.4)),
        )
        .add_params(select_x, select_y)
    )

    title = alt.Title(alt.expr(f'{select_x.name}.solver + " vs " + {select_y.name}.solver2'))
    g_results = (
        alt.Chart(df_results, title=title, height=250, width=250)
        .transform_filter(select_x, select_y)
        .transform_aggregate(benchs="sum(len)", groupby=["bucket", "bucket2"])
        .add_params(select_x, select_y)
        .encode(
            alt.X("bucket:O").axis(title="solver1", bandPosition=0.5)
            # align should move the center of the cell, it does not
            .scale(type="band", align=0),
            alt.Y("bucket2:O").axis(title="solver2", bandPosition=0.5).scale(type="band", align=0).sort("descending"),
            text="benchs:Q",
        )
    )

    g_results_rect = g_results.mark_rect().encode(alt.Color("benchs:Q", scale=alt.Scale(scheme="yellowgreenblue")))

    g_results_text = g_results.mark_text(baseline="middle")

    graph = (g_select_provers | g_results_rect + g_results_text).resolve_scale(color="independent")

    graph.save(output_dir / "test.html")
    graph.save(output_dir / "test.json", format="json")
