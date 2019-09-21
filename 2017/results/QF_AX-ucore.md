---
layout: default
---
{%- include tablesorter.html -%}

##  QF_AX (Unsat Core Track)

Competition results for the QF_AX division as of Tue Jul 18 22:06:21 GMT

**Benchmarks in this division: 279**
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
<td class="right">1.801</td>
<td class="right">23328.383</td>
<td class="right">2.753</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td class="right">0.000</td>
<td class="right">367.720</td>
<td class="right">1.947</td>
</tr>
<tr>
<td>mathsat-5.4.1<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">30.076</td>
<td class="right">31098.351</td>
<td class="right">0.127</td>
</tr>
<tr>
<td>z3-4.5.0<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">34432.957</td>
<td class="right">0.174</td>
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
<td class="right">1.801</td>
<td class="right">23328.383</td>
<td class="right">3.612</td>
<td class="right">3.616</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td class="right">0.000</td>
<td class="right">367.720</td>
<td class="right">1.947</td>
<td class="right">0.770</td>
</tr>
<tr>
<td>mathsat-5.4.1<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">30.076</td>
<td class="right">31098.351</td>
<td class="right">0.127</td>
<td class="right">0.134</td>
</tr>
<tr>
<td>z3-4.5.0<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">34432.957</td>
<td class="right">0.174</td>
<td class="right">0.177</td>
</tr>
</table>
<span id="fn"> n. Non-competing.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


