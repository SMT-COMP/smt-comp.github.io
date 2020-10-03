---
layout: default
---
{%- include tablesorter.html -%}

##  AUFNIRA (Main Track)

Competition results for the AUFNIRA division as of Thu Jul 7 07:24:34 GMT

**Benchmarks in this division : 1050** 

### Winners
#### Sequential Performance
<table>
<tr>
<th class="center">Sequential Performance</th>
<th class="center">Parallel Performance</th>
</tr>
<tr class="center">
<td>vampire_smt_4.1_parallel</td>
<td>vampire_smt_4.1_parallel</td>
</tr>
</table>
### Result table<sup><a href="#fn1">1</a></sup>
 




#### Sequential Performance
<table id="sequential" class="result sorted">
<thead>
<tr>
<th class="center">Solver</th>
<th class="center">Error Score</th>
<th class="center">Correct Score</th>
<th class="center">avg. CPU time </th>
</tr>
</thead>
<tr>
<td>CVC4</td>
<td class="right">0.000</td>
<td class="right">985.468</td>
<td class="right">144.671</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">1009.983</td>
<td class="right">35.728</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">1013.318</td>
<td class="right">90.368</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">992.125</td>
<td class="right">40.797</td>
</tr>
</table>


#### Parallel Performance
<table id="parallel" class="result sorted">
<thead>
<tr>
<th class="center">Solver</th><th class="center">Error Score</th>
<th class="center">Correct Score</th>
<th class="center">avg. CPU time </th>
<th class="center">avg. WALL time </th>

<th class="center">Unsolved</th>
</tr>
</thead>
<tr>
<td>CVC4</td>
<td class="right">0.000</td>
<td class="right">985.468</td>
<td class="right">144.674</td>
<td class="right">147.344</td>
<td class="right">21</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">1009.983</td>
<td class="right">35.728</td>
<td class="right">35.553</td>
<td class="right">24</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">1013.318</td>
<td class="right">136.951</td>
<td class="right">35.144</td>
<td class="right">22</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">992.125</td>
<td class="right">40.805</td>
<td class="right">46.872</td>
<td class="right">27</td>
</tr>
</table>
<span id="fn"> n. Non-competitive.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


