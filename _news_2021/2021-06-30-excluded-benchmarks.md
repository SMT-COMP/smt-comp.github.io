---
layout: news
author:
title: Wrongly Classified Benchmarks
newsdate: 2021-06-30
---

When analyzing the SMT-COMP results we found benchmarks that do not fit in their corresponding logic in the latest SMT-LIB release.

There are several thousand benchmarks in linear arithmetic using div, mod, or non-linear arithmetic.  We will remove these benchmarks from the scoring, since they do not conform to their logic.  Here are the number of problematic benchmarks by logic:

    AUFBVDTLIA: 7
    AUFDTLIRA: 1096
    AUFFPDTLIRA: 21
    LIA: 191
    QF_SLIA: 65
    UFDTLIRA: 2581
    UFFPDTLIRA: 10

Roughly half of these benchmarks were selected in the competition.

Also there are 168 benchmarks in the logics *FP that use to_fp with a real number as argument, which are only allowed in the *FPLRA logics.  Half of them are in the incremental track.  We plan to remove these from the scoring as well.

There are 44 benchmarks in QF_SLIA that contain quantifiers and that we plan to remove from the scoring.

Moreover, there is a whole new family of benchmarks in NRA (20200911-Pine) that doesn't use quantifiers, but are not classified as quantifier-free.  While this is clearly not intended, we plan to still keep these benchmarks in the scoring, since they are valid benchmarks.

A [full list of excluded benchmarks](/2021/excluded_benchmarks/SMT-LIB_excluded.tar.xz) can be downloaded here.
