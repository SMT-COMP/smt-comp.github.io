---
layout: default
---
{%- include tablesorter.html -%}

##  AUFLIRA (Main Track)

Competition results for the AUFLIRA division as of Thu Jul 7 07:24:34 GMT

**Benchmarks in this division: 19849**
<br/>
**Time Limit: 1200s**


### Winners
<table>
<tr>
<th class="center">Sequential Performance</th>
<th class="center">Parallel Performance</th>
</tr>
<tr class="center">
<td>vampire_smt_4.1</td>
<td>vampire_smt_4.1</td>
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
<td class="right">18277.495</td>
<td class="right">204.701</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">18334.103</td>
<td class="right">78.879</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">18334.103</td>
<td class="right">184.743</td>
</tr>
<tr>
<td>veriT-dev</td>
<td class="right">0.000</td>
<td class="right">16478.894</td>
<td class="right">351.783</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">19378.300</td>
<td class="right">57.075</td>
</tr>
</table>

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
<td class="right">18277.495</td>
<td class="right">204.856</td>
<td class="right">205.508</td>
<td class="right">110</td>
</tr>
<tr>
<td>vampire_smt_4.1</td>
<td class="right">0.000</td>
<td class="right">18334.103</td>
<td class="right">78.879</td>
<td class="right">78.457</td>
<td class="right">104</td>
</tr>
<tr>
<td>vampire_smt_4.1_parallel</td>
<td class="right">0.000</td>
<td class="right">18334.103</td>
<td class="right">283.255</td>
<td class="right">78.627</td>
<td class="right">104</td>
</tr>
<tr>
<td>veriT-dev</td>
<td class="right">0.000</td>
<td class="right">16478.894</td>
<td class="right">352.055</td>
<td class="right">351.785</td>
<td class="right">536</td>
</tr>
<tr>
<td>z3<SUP><a href="#fn">n</a></SUP>
</td>
<td class="right">0.000</td>
<td class="right">19378.300</td>
<td class="right">57.106</td>
<td class="right">57.074</td>
<td class="right">3</td>
</tr>
</table>
<span id="fn"> n. Non-competitive.</span>

<span id="fn1"> 1. Scores are computed according to Section 7 of the rules.</span>


