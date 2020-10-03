---
layout: default
---
{%- include tablesorter.html -%}

##  ALIA (Main Track)

Competition results for the ALIA division as of Thu Jul 7 07:24:34 GMT

**Benchmarks in this division: 42**
<br/>
**Time Limit: 1200s**


### Winners
<table>
<tr>
<th class="center">Sequential Performance</th>
<th class="center">Parallel Performance</th>
</tr>
<tr class="center">
<td>CVC4</td>
<td>CVC4</td>
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
<td class="right">42.000</td>
<td class="right">0.055</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">38.000</td>
<td class="right">100.025</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">38.000</td>
<td class="right">232.315</td>
</tr>
<tr>
<td>veriT-dev</td>
<td class="right">0.000</td>
<td class="right">27.000</td>
<td class="right">857.150</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">42.000</td>
<td class="right">0.045</td>
</tr>
</table>

#### Parallel Performance
<table id="parallel" class="result sorted">
<thead>
<tr>
<th class="center">Solver</th>
<th class="center">Error Score</th>
<th class="center">Correct Score</th>
<th class="center">avg. CPU time </th>
<th class="center">avg. WALL time </th>
<th class="center">Unsolved</th>
</tr>
</thead>
<tr>
<td>CVC4</td>
<td class="right">0.000</td>
<td class="right">42.000</td>
<td class="right">0.055</td>
<td class="right">0.057</td>
<td class="right">0</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">38.000</td>
<td class="right">100.025</td>
<td class="right">99.566</td>
<td class="right">4</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">39.000</td>
<td class="right">359.011</td>
<td class="right">91.960</td>
<td class="right">3</td>
</tr>
<tr>
<td>veriT-dev</td>
<td class="right">0.000</td>
<td class="right">27.000</td>
<td class="right">857.611</td>
<td class="right">857.158</td>
<td class="right">15</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">42.000</td>
<td class="right">0.045</td>
<td class="right">0.046</td>
<td class="right">0</td>
</tr>
</table>

<span id="fn"> n. Non-competitive.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


