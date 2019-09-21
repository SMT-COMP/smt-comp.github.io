---
layout: default
---
{%- include tablesorter.html -%}

##  QF_UFBV (Unsat Core Track)

Competition results for the QF_UFBV division as of Thu Jul 12 23:54:00 GMT

**Benchmarks in this division : 575  
Time limit: 2400s** 

### Winners<table class="result">
<tr>
                           <th class="center">Sequential Performance</th>
                           <th class="center">Parallel Performance</th>
                           </tr><tr class="center"><td>Yices 2.6.0</td><td>Yices 2.6.0</td></tr></table>
### Result table<sup><a href="#fn1">1</a></sup>

#### Sequential Performance

<table id="sequential" class="result sorted">
<thead><tr class="center">
  <th>Solver</th>
  <th>Error Score</th>
  <th>Reduction Score</th>
  <th>avg. CPU time</th>
</tr></thead><tr>
<td>Yices 2.6.0</td>
<td>0.000</td><td>723326.837</td><td>125.240</td><tr>
<td>CVC4</td>
<td>323.419</td><td>46.167</td><td>576.433</td><tr>
<td>mathsat-5.5.2<SUP><a href="#fn">n</a></SUP></td>
<td>0.000</td><td>723189.550</td><td>329.217</td><tr>
<td>z3-4.7.1<SUP><a href="#fn">n</a></SUP></td>
<td>0.000</td><td>725283.479</td><td>308.021</td></tr></table>

#### Parallel Performance

<table id="parallel" class="result sorted">
<thead><tr class="center">
  <th>Solver</th>
  <th>Error Score</th>
  <th>Reduction Score</th>
  <th>avg. CPU time</th>
  <th>avg. WALL time</th>
</tr></thead><tr>
<td>Yices 2.6.0</td>
<td>0.000</td><td>723326.837</td><td>125.240</td><td>125.245</td></tr><tr>
<td>CVC4</td>
<td>323.419</td><td>46.167</td><td>576.451</td><td>576.578</td></tr><tr>
<td>mathsat-5.5.2<SUP><a href="#fn">n</a></SUP></td>
<td>0.000</td><td>723189.550</td><td>329.217</td><td>329.131</td></tr><tr>
<td>z3-4.7.1<SUP><a href="#fn">n</a></SUP></td>
<td>0.000</td><td>725283.479</td><td>308.021</td><td>308.051</td></tr></table>
 <span id="fn"> n. Non-competing. </span>

 <span id="fn1"> 1. Scores are computed according to Section 7 of the rules. </span>


