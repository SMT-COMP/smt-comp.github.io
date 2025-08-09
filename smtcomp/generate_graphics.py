import math
import functools, itertools
from collections import defaultdict
from typing import Set, Dict, Optional, cast, List, DefaultDict, Tuple
from pathlib import Path, PurePath
from smtcomp import defs
from rich.progress import track as rich_track

import polars as pl
import altair as alt
import altair.utils.html
import altair.vegalite.display
from smtcomp.utils import *
import smtcomp.generate_website_page
import frontmatter
from random import Random
import math

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


def correlation_sorting(solvers: List[U], corrs: Mapping[Tuple[U, U], float], nb_iteration: int) -> None:
    """
    Strangely I can't find easy to use lib creating a well clustered correlation matrix. block modelling.

    We use simulated annealing
    """
    if len(solvers) <= 2:
        return

    r = Random(0)

    def neighbor(i: int) -> float:
        s = 0.0
        n = 0
        if 0 < i:
            s += 1 - corrs[solvers[i - 1], solvers[i]]
            n += 1
        if i < len(solvers) - 1:
            s += 1 - corrs[solvers[i], solvers[i + 1]]
            n += 1
        # At the bounds there is only one neighbor
        return s / n

    def swap(i: int, j: int) -> None:
        tmp = solvers[i]
        solvers[i] = solvers[j]
        solvers[j] = tmp

    for i in range(0, nb_iteration):
        a = r.randint(0, len(solvers) - 1)
        b = r.randint(0, len(solvers) - 2)
        if a <= b:
            b += 1
        s1 = neighbor(a) + neighbor(b)
        swap(a, b)
        s2 = neighbor(a) + neighbor(b)
        swap(a, b)
        t = 1 - (i / (nb_iteration + 1))
        if s2 < s1 or math.exp((s1 - s2) / t) > r.uniform(0.0, 1.0):
            swap(a, b)


def create_output(
    config: defs.Config,
    results: pl.LazyFrame,
    logics: list[defs.Logic] = [],
    divisions: list[defs.Division] = [],
) -> alt.api.ChartType:

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
        .select(c_solver, c_solver2, "corr")
    )

    results = (
        results.group_by(c_solver, c_solver2, c_answer, c_answer2, c_bucket, c_bucket2, c_logic, c_division)
        .len()
        .sort(c_solver, c_solver2)
    )

    # Replace integer by names
    # It should be possible to do it later in altair; the html file would be smaller
    if True:
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

    df_corr, df_results, df_buckets, df_answers, df_solvers = pl.collect_all(
        [
            corr,
            results,
            results.select(c_bucket.unique()),
            results.select(c_answer.unique()),
            results.select(c_solver.unique()),
        ]
    )

    bucket_domain: list[float] = list(df_buckets["bucket"])
    answer_domain: list[str] = list(df_answers["answer"])
    answer_domain.sort(key=lambda x: defs.Answer(x).id)

    solver_domain: list[str] = list(df_solvers["solver"])
    solver_domain.sort(key=lambda x: x.lower())

    if True:
        # Two provers can have no benchmars in common, their pairs is not in df_corrs
        corrs: DefaultDict[Tuple[str, str], float] = defaultdict(lambda: 0.0)
        for row in df_corr.rows(named=False):
            corrs[row[0], row[1]] = row[2]
        correlation_sorting(solver_domain, corrs, 1000)

    row1 = df_corr.row(min(1, len(df_corr) - 1), named=True)

    # Create heatmap with selection
    solvers = alt.selection_point(
        fields=["solver", "solver2"],
        name="solvers",
        value=[{"solver": row1["solver"], "solver2": row1["solver2"]}],
        toggle=False,
    )
    answer_xy = alt.selection_point(fields=["answer", "answer2"], name="answer")
    logic = alt.selection_point(fields=["logic"], name="logic")
    division = alt.selection_point(fields=["division"], name="division")
    g_select_provers = (
        alt.Chart(df_corr, title="Click a tile to compare solvers", height=250, width=250)
        .mark_rect()
        .encode(
            alt.X("solver", title=None).scale(domain=solver_domain),
            alt.Y("solver2", title=None).scale(domain=list(reversed(solver_domain))),
            alt.Color("corr", scale=alt.Scale(domain=[-1, 1], scheme="blueorange")),
            opacity=alt.when(solvers).then(alt.value(1)).otherwise(alt.value(0.4)),
        )
        .add_params(solvers)
    )

    # Number of results by time
    title = alt.Title(
        alt.expr(f'{solvers.name}.solver + " vs " + {solvers.name}.solver2'), subtitle="comparison of cpu time"
    )
    g_results_base = (
        alt.Chart(df_results, title=title, height=250, width=250)
        .transform_filter(solvers, answer_xy, logic, division)
        .transform_aggregate(benchs="sum(len)", groupby=["bucket", "bucket2"])
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

    g_results_rect = g_results_base.mark_rect().encode(alt.Color("benchs:Q", scale=alt.Scale(scheme="yellowgreenblue")))

    g_results_text = g_results_base.mark_text(baseline="middle")

    g_results = g_results_rect + g_results_text

    opacity = alt.when(solvers, answer_xy, logic, division).then(alt.value(1)).otherwise(alt.value(0.01))

    opacity_answer = alt.when(answer_xy).then(alt.value(1)).otherwise(alt.value(0.5))

    # Number of results by answers
    g_answer_base = (
        alt.Chart(df_results, title="Comparison of the answers", height=250, width=250)
        .transform_filter(solvers, logic, division)
        .transform_aggregate(benchs="sum(len)", groupby=["answer", "answer2"])
        .add_params(answer_xy)
        .encode(
            alt.X("answer:N").axis(title="solver1", bandPosition=0.5)
            # align should move the center of the cell, it does not
            .scale(type="band", align=0, domain=answer_domain),
            alt.Y("answer2:N")
            .axis(title="solver2", bandPosition=0.5)
            .scale(type="band", align=0, domain=list(reversed(answer_domain))),
            text="benchs:Q",
            opacity=opacity_answer,
        )
    )

    g_answer_rect = g_answer_base.mark_rect().encode(alt.Color("benchs:Q", scale=alt.Scale(scheme="yellowgreenblue")))

    g_answer_text = g_answer_base.mark_text(baseline="middle")

    g_answer = g_answer_rect + g_answer_text

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

    graph: alt.api.ChartType = (g_select_provers | g_results).resolve_scale(color="independent")

    graph = alt.vconcat(graph, g_answer | (legend_logic | legend_division))

    graph = graph.resolve_scale(color="independent")

    return graph


def save_output(
    config: defs.Config,
    results: pl.LazyFrame,
    output: Path,
    logics: list[defs.Logic] = [],
    divisions: list[defs.Division] = [],
) -> None:

    create_output(config, results, logics, divisions).save(output)


def save_hugo_output(chart: alt.api.ChartType, output: Path, title: str) -> None:

    with alt.data_transformers.disable_max_rows():
        content = chart.to_html(
            fullhtml=False,
        )
    post = frontmatter.Post(content=content, title=title, layout="chart")
    output.write_text(frontmatter.dumps(post))


def generate_pages(config: defs.Config, results: pl.LazyFrame, track: defs.Track) -> None:
    page_suffix = smtcomp.generate_website_page.page_track_suffix(track)
    dst = config.web_results
    dst.mkdir(parents=True, exist_ok=True)

    df_results = results.filter(c_run == True).collect()
    results = df_results.lazy()

    divisions = list(df_results["division"].unique())
    for div in rich_track(list(map(defs.Division.of_int, divisions)), description="Generating chart for divisions"):
        chart = create_output(config, results, divisions=[div])
        save_hugo_output(
            chart,
            output=dst / f"{div.name.lower()}-{page_suffix}-chart.html",
            title=f"Chart for division {div.name}",
        )

    logics = list(df_results["logic"].unique())
    for logic in rich_track(list(map(defs.Logic.of_int, logics)), description="Generating chart for logics"):
        chart = create_output(config, results, logics=[logic])
        save_hugo_output(
            chart,
            output=dst / f"{logic.name.lower()}-{page_suffix}-chart.html",
            title=f"Chart for logic {logic.name}",
        )
