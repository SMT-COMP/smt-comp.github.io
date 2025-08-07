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
c_division = pl.col("division")
c_solver = pl.col("solver")
c_solver2 = pl.col("solver2")
c_answer = pl.col("answer")
c_answer2 = pl.col("answer2")
c_cputime_s = pl.col("cputime_s")
c_cputime_s2 = pl.col("cputime_s2")
c_run = pl.col("run")
c_bucket = pl.col("bucket")
c_bucket2 = pl.col("bucket2")


def create_output(
    config: defs.Config,
    results: pl.LazyFrame,
    output: Path,
    logics: list[defs.Logic] = [],
    divisions: list[defs.Division] = [],
) -> None:

    # We are computing the buckets offline because we have too much data
    results = results.filter(
        c_run == True, c_logic.is_in(set(map(int, logics))) | c_division.is_in(set(map(int, divisions)))
    ).select(
        c_file,
        c_logic,
        c_division,
        c_solver,
        c_answer,
        c_cputime_s,
        bucket=pl.lit(10.0).pow(c_cputime_s.log(10).floor()),
        # bucket=c_cputime_s.log(10).floor(),
    )

    results_with = results.select(c_file, solver2=c_solver, bucket2=c_bucket, cputime_s2=c_cputime_s, answer2=c_answer)
    results = results.join(results_with, on=c_file, how="left")

    corr = (
        results.group_by(c_solver, c_solver2)
        .agg(corr=pl.corr(c_cputime_s, c_cputime_s2, method="pearson"))
        .sort(c_solver, c_solver2)
    )

    results = (
        results.group_by(c_solver, c_solver2, c_answer, c_answer2, c_bucket, c_bucket2, c_logic, c_division)
        .len()
        .sort(c_solver, c_solver2)
    )

    # Replace integer by names
    # It should be possible to do it later in altair; the html file would be smaller
    for lookup, replaced in [
        (defs.Answer, "answer"),
        (defs.Answer, "answer2"),
        (defs.Logic, "logic"),
        (defs.Division, "division"),
    ]:
        lf_lookup = pl.DataFrame(
            data=((int(n), str(n)) for n in lookup), schema=[(replaced, pl.Int8), ("pretty", pl.String)]
        ).lazy()
        results = results.join(lf_lookup, how="left", on=replaced).drop(replaced).rename({"pretty": replaced})

    buckets = results.select(c_bucket.unique())

    df_corr, df_results, df_buckets = pl.collect_all([corr, results, buckets])

    bucket_domain: list[float] = list(df_buckets["bucket"])

    row1 = df_corr.row(1, named=True)

    # Create heatmap with selection
    select_x = alt.selection_point(fields=["solver"], name="solver1", value=row1["solver"], toggle=False)
    select_y = alt.selection_point(fields=["solver2"], name="solver2", value=row1["solver2"], toggle=False)
    answer_x = alt.selection_point(fields=["answer"], name="answer1")
    answer_y = alt.selection_point(fields=["answer2"], name="answer2")
    logic = alt.selection_point(fields=["logic"], name="logic")
    division = alt.selection_point(fields=["division"], name="division")
    g_select_provers = (
        alt.Chart(df_corr, title="Click a tile to compare solvers", height=250, width=250)
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
        .transform_filter(select_x, select_y, answer_x, answer_y)
        .transform_aggregate(benchs="sum(len)", groupby=["bucket", "bucket2"])
        .add_params(select_x, select_y, answer_x, answer_y)
        .encode(
            alt.X("bucket:O").axis(title="solver1", bandPosition=0.5)
            # align should move the center of the cell, it does not
            .scale(type="band", align=0, domain=bucket_domain),
            alt.Y("bucket2:O")
            .axis(title="solver2", bandPosition=0.5)
            .scale(type="band", align=0, domain=list(reversed(bucket_domain))),
            text="benchs:Q",
        )
    )

    g_results_rect = g_results.mark_rect().encode(alt.Color("benchs:Q", scale=alt.Scale(scheme="yellowgreenblue")))

    g_results_text = g_results.mark_text(baseline="middle")

    # g_answers = (
    #     alt.Chart(df_results, title="Answers")
    #     .transform_filter(select_x, select_y, answer_x, answer_y)
    #     .transform_aggregate(benchs="sum(len)", groupby=["answer_x", "bucket2"])
    #     .add_params(select_x, select_y, answer_x, answer_y)
    #     .encode(
    #         alt.X("bucket:O").axis(title="solver1", bandPosition=0.5)
    #         # align should move the center of the cell, it does not
    #         .scale(type="band", align=0),
    #         alt.Y("bucket2:O").axis(title="solver2", bandPosition=0.5).scale(type="band", align=0).sort("descending"),
    #         text="benchs:Q",
    #     )
    #     .mark_bar()
    # )
    opacity = (
        alt.when(select_x, select_y, answer_x, answer_y, logic, division).then(alt.value(1)).otherwise(alt.value(0.0))
    )

    legend_answer_x = (
        alt.Chart(df_results, title=alt.Title(alt.expr(f'"solver1:" + {select_x.name}.solver')))
        .mark_point()
        .encode(alt.Y("answer:N").axis(title="", orient="right"), opacity=opacity)
        .add_params(answer_x)
    )

    legend_answer_y = (
        alt.Chart(df_results, title=alt.Title(alt.expr(f'"solver2:" + {select_y.name}.solver2')))
        .mark_point()
        .encode(alt.Y("answer2:N").axis(title="", orient="right"), opacity=opacity)
        .add_params(answer_y)
    )

    legend_logic = (
        alt.Chart(df_results, title="Logic")
        .mark_point()
        .encode(alt.Y("logic:N").axis(title="", orient="right"), opacity=opacity)
        .add_params(logic)
    )

    legend_division = (
        alt.Chart(df_results, title="Division")
        .mark_point()
        .encode(alt.Y("division:N").axis(title="", orient="right"), opacity=opacity)
        .add_params(division)
    )

    graph = (g_select_provers | g_results_rect + g_results_text).resolve_scale(color="independent")

    graph = alt.vconcat(graph, legend_answer_x | legend_answer_y | legend_logic | legend_division)

    graph = graph.resolve_scale(color="independent")

    graph.save(output)
