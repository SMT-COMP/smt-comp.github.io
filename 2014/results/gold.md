---
layout: default
---
{%- include tablesorter.html -%}

## Medal Standings



Competition results for the Medal standings division as of Fri Jun 27 16:49:23 EDT 2014
### Gold/Silver medal current standings
The gold and silver medal winners are the first and second place measured by
absence of errors and the most solved problems, measured by a weighted,
non-linear metric across divisions.



<table>
<tr>
<th class="center">Solver</th>
<th class="center">% Complete</th>
<th class="center">Weighted<br>Errors</th>
<th class="center">Weighted<br>Solved</th>
</tr>
<tr>
<td>veriT</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">  25.325</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">  22.831</td>
</tr>
<tr>
<td>CVC3</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   9.618</td>
</tr>
<tr>
<td>SONOLAR</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   5.978</td>
</tr>
<tr>
<td>AProVE</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   3.776</td>
</tr>
<tr>
<td>Boolector (justification)</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   3.758</td>
</tr>
<tr>
<td>Boolector (dual propagation)</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   3.755</td>
</tr>
<tr>
<td>OpenSMT2</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   3.582</td>
</tr>
<tr>
<td>Boolector</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   3.058</td>
</tr>
<tr>
<td>STP-CryptoMiniSat4</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   2.859</td>
</tr>
<tr>
<td class="right">4Simp</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   2.468</td>
</tr>
<tr>
<td>raSAT</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
<td align="right">   0.000</td>
</tr>
<tr>
<td>Yices2</td>
<td align="right">100%</td>
<td align="right">   3.810</td>
<td align="right">  38.624</td>
</tr>
<tr>
<td>CVC4</td>
<td align="right">100%</td>
<td align="right">   7.283</td>
<td align="right">  54.152</td>
</tr>
<tr>
<td>abziz_min_features</td>
<td align="right">100%</td>
<td align="right">  30.563</td>
<td align="right">   2.548</td>
</tr>
<tr>
<td>abziz_all_features</td>
<td align="right">100%</td>
<td align="right">  30.563</td>
<td align="right">   2.403</td>
</tr>
<tr>
<td>Kleaver-STP</td>
<td align="right">100%</td>
<td align="right"> 213.362</td>
<td align="right">   3.103</td>
</tr>
<tr>
<td>Kleaver-portfolio</td>
<td align="right">100%</td>
<td align="right"> 346.713</td>
<td align="right">   3.073</td>
</tr>
</table>
<h2>Bronze medal</h2>
The bronze medal is awarded to the winner of the<a href="results-QF_BV.shtml">QF_BV</a> division.
<h2>An alternate scoring metric</h2>
The organizers also considered a different metric for gold/silver medals. We officially adopted the one above, as expressed in the competition rules, since it emphasizes soundness of solvers (a solver with an error in any division scores lower than solvers with no errors, even when they compete in fewer divisions). In the alternate metric, a division without errors contributes the squared fraction of solved instances weighted by the log10 of the number of benchmarks in the division; a division with errors contributes the negative of the division's weight times the number of errors. For comparative information only, the table below shows rankings using this metric.


<table id="sequential" class="result sorted">
<thead>
<tr>
<th class="center">Solver</th>
<td>% Complete</td>
<td>Alternate<br>Metric</td>
</tr>
<tr>
<td>CVC4</td>
<td align="right">100%</td>
<td align="right">  43.509</td>
</tr>
<tr>
<td>Yices2</td>
<td align="right">100%</td>
<td align="right">  31.059</td>
</tr>
<tr>
<td>veriT</td>
<td align="right">100%</td>
<td align="right">  25.325</td>
</tr>
<tr>
<td>SMTInterpol</td>
<td align="right">100%</td>
<td align="right">  22.831</td>
</tr>
<tr>
<td>CVC3</td>
<td align="right">100%</td>
<td align="right">   9.618</td>
</tr>
<tr>
<td>SONOLAR</td>
<td align="right">100%</td>
<td align="right">   5.978</td>
</tr>
<tr>
<td>AProVE</td>
<td align="right">100%</td>
<td align="right">   3.776</td>
</tr>
<tr>
<td>Boolector (justification)</td>
<td align="right">100%</td>
<td align="right">   3.758</td>
</tr>
<tr>
<td>Boolector (dual propagation)</td>
<td align="right">100%</td>
<td align="right">   3.755</td>
</tr>
<tr>
<td>OpenSMT2</td>
<td align="right">100%</td>
<td align="right">   3.582</td>
</tr>
<tr>
<td>Boolector</td>
<td align="right">100%</td>
<td align="right">   3.058</td>
</tr>
<tr>
<td>STP-CryptoMiniSat4</td>
<td align="right">100%</td>
<td align="right">   2.859</td>
</tr>
<tr>
<td class="right">4Simp</td>
<td align="right">100%</td>
<td align="right">   2.468</td>
</tr>
<tr>
<td>raSAT</td>
<td align="right">100%</td>
<td align="right">   0.000</td>
</tr>
<tr>
<td>abziz_min_features</td>
<td align="right">100%</td>
<td align="right"> -30.563</td>
</tr>
<tr>
<td>abziz_all_features</td>
<td align="right">100%</td>
<td align="right"> -30.563</td>
</tr>
<tr>
<td>Kleaver-STP</td>
<td align="right">100%</td>
<td align="right">-213.362</td>
</tr>
<tr>
<td>Kleaver-portfolio</td>
<td align="right">100%</td>
<td align="right">-346.713</td>
</tr>
</table>

