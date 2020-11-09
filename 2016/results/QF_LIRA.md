---
layout: default
---
{%- include tablesorter.html -%}

##  QF_LIRA (Main Track)

Competition results for the QF_LIRA division as of Thu Jul 7 07:24:34 GMT

**Benchmarks in this division: 6**
<br/>
**Time Limit: 1200s**


### Winners
<table>
<tr>
<th class="center">Sequential Performance</th>
<th class="center">Parallel Performance</th>
</tr>
<tr class="center">
<td>Yices2</td>
<td>Yices2</td>
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
<td class="right">6.000</td>
<td class="right">164.039</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td class="right">0.000</td>
<td class="right">3.000</td>
<td class="right">1203.021</td>
</tr>
<tr>
<td>Yices2</td>
<td class="right">0.000</td>
<td class="right">6.000</td>
<td class="right">19.110</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">5.000</td>
<td class="right">11.183</td>
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
<td class="right">6.000</td>
<td class="right">164.039</td>
<td class="right">164.086</td>
<td class="right">0</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td class="right">0.000</td>
<td class="right">3.000</td>
<td class="right">1215.079</td>
<td class="right">1200.937</td>
<td class="right">3</td>
</tr>
<tr>
<td>Yices2</td>
<td class="right">0.000</td>
<td class="right">6.000</td>
<td class="right">19.110</td>
<td class="right">19.099</td>
<td class="right">0</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">5.000</td>
<td class="right">11.183</td>
<td class="right">11.175</td>
<td class="right">1</td>
</tr>
</table>
<span id="fn"> n. Non-competitive.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


