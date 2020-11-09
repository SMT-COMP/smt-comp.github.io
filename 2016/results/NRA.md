---
layout: default
---
{%- include tablesorter.html -%}

##  NRA (Main Track)

Competition results for the NRA division as of Thu Jul 7 07:24:34 GMT

**Benchmarks in this division: 3788**
<br/>
**Time Limit: 1200s**


### Winners
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
<td class="right">3728.000</td>
<td class="right">0.251</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">3777.000</td>
<td class="right">3.389</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">3778.000</td>
<td class="right">6.481</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">3740.000</td>
<td class="right">2.796</td>
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
<td class="right">3728.000</td>
<td class="right">0.251</td>
<td class="right">0.253</td>
<td class="right">60</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">3777.000</td>
<td class="right">3.389</td>
<td class="right">3.374</td>
<td class="right">11</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">3778.000</td>
<td class="right">10.818</td>
<td class="right">2.959</td>
<td class="right">10</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">3740.000</td>
<td class="right">2.796</td>
<td class="right">2.791</td>
<td class="right">48</td>
</tr>
</table>
<span id="fn"> n. Non-competitive.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


