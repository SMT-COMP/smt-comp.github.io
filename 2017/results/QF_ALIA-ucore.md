---
layout: default
---
{%- include tablesorter.html -%}

##  QF_ALIA (Unsat Core Track)

Competition results for the QF_ALIA division as of Tue Jul 18 22:06:21 GMT

**Benchmarks in this division : 80** 
<br/>
**Time Limit: 2400s**

### Winners
<table>
<tr>
<th class="center">Sequential Performance</th>
<th class="center">Parallel Performance</th>
</tr>
<tr class="center">
<td>SMTInterpol</td>
<td>SMTInterpol</td>
</tr>
</table>

### Result table<sup><a href="#fn1">1</a></sup>


#### Sequential Performance
<table id="sequential" class="result sorted">
<thead>
<tr>
<th class="center">Solver</th>
<th class="center">Error Score</th>
<th class="center">Reduction Score</th>
<th class="center">avg. CPU time </th>
</tr>
</thead>
<tr>
<td>CVC4</td>
<td class="right">0.000</td>
<td class="right">2615.592</td>
<td class="right">54.144</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td class="right">0.000</td>
<td class="right">3214.438</td>
<td class="right">11.525</td>
</tr>
<tr>
<td>mathsat-5.4.1<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">3035.314</td>
<td class="right">20.284</td>
</tr>
<tr>
<td>z3-4.5.0<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">3511.599</td>
<td class="right">18.017</td>
</tr>
</table>

#### Parallel Performance
<table id="parallel" class="result sorted">
<thead>
<tr>
<th class="center">Solver</th>
<th class="center">Error Score</th>
<th class="center">Reduction Score</th>
<th class="center">avg. CPU time </th>
<th class="center">avg. WALL time </th>
</tr>
</thead>
<tr>
<td>CVC4</td>
<td class="right">0.000</td>
<td class="right">2615.592</td>
<td class="right">155.501</td>
<td class="right">155.535</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td class="right">0.000</td>
<td class="right">3214.438</td>
<td class="right">11.525</td>
<td class="right">7.849</td>
</tr>
<tr>
<td>mathsat-5.4.1<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">3035.314</td>
<td class="right">52.996</td>
<td class="right">53.007</td>
</tr>
<tr>
<td>z3-4.5.0<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">3511.599</td>
<td class="right">30.201</td>
<td class="right">30.205</td>
</tr>
</table>
<span id="fn"> n. Non-competing.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


