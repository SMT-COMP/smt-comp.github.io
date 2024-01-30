<h2>Benchmarks</h2>

<p>
SMT-COMP 2015 will use a subset of the benchmarks available within the
2015-06-01 release
of <a href="http://smtlib.cs.uiowa.edu/">SMT-LIB</a>, as described in
the competition rules.  Specifically, benchmarks with unknown status,
bit-vector benchmarks that contain partial operations (e.g.,
bit-vector division), and floating-point benchmarks that contain
underspecified operations (e.g., <tt>fp.min</tt>) will not be used.
</p>

<p>
The SMT-LIB benchmarks are available in space
<a href="https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=73907"><tt>root/SMT/SMT-LIB
benchmarks/2015-06-01</tt></a> on StarExec.  They may also be
downloaded
from <a href="http://www.cs.nyu.edu/~barrett/smtlib/">http://www.cs.nyu.edu/~barrett/smtlib/</a>.
</p>

<p>
The subset of benchmarks eligible for SMT-COMP 2015 is available in
StarExec spaces
<a href="https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=85819"><tt>root/SMT/Competitions
and evaluations/SMT-COMP 2015/Benchmarks - Application Track</tt></a>
and <a href="https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=86692"><tt>root/SMT/Competitions
and evaluations/SMT-COMP 2015/Benchmarks - Main Track</tt></a> for the
application and main track, respectively.
</p>

<h2>Main Track</h2>

<table>
  <tr>
    <th>Logic</th>
    <th>Benchmarks eligible for SMT-COMP</th>
    <th>Benchmarks with unknown status</th>
    <th>Benchmarks in SMT-LIB</th>
  </tr>
  <tr>
    <td>ALIA</td>
    <td>42</td>
    <td>0</td>
    <td>42</td>
  </tr>
  <tr>
    <td>AUFLIA</td>
    <td>4</td>
    <td>0</td>
    <td>4</td>
  </tr>
  <tr>
    <td>AUFLIRA</td>
    <td>19849</td>
    <td>165</td>
    <td>20014</td>
  </tr>
  <tr>
    <td>AUFNIRA</td>
    <td>1050</td>
    <td>445</td>
    <td>1495</td>
  </tr>
  <tr>
    <td>BV</td>
    <td>85</td>
    <td>106</td>
    <td>191</td>
  </tr>
  <tr>
    <td>LIA</td>
    <td>201</td>
    <td>189</td>
    <td>390</td>
  </tr>
  <tr>
    <td>LRA</td>
    <td>339</td>
    <td>282</td>
    <td>621</td>
  </tr>
  <tr>
    <td>NIA</td>
    <td>9</td>
    <td>5</td>
    <td>14</td>
  </tr>
  <tr>
    <td>NRA</td>
    <td>3788</td>
    <td>25</td>
    <td>3813</td>
  </tr>
  <tr>
    <td>QF_ABV</td>
    <td>14720 (197 excluded<sup><a href="#fn1">1</a></sup>)</td>
    <td>174</td>
    <td>15091</td>
  </tr>
  <tr>
    <td>QF_ALIA</td>
    <td>134</td>
    <td>0</td>
    <td>134</td>
  </tr>
  <tr>
    <td>QF_ANIA</td>
    <td>6</td>
    <td>0</td>
    <td>6</td>
  </tr>
  <tr>
    <td>QF_AUFBV</td>
    <td>37</td>
    <td>0</td>
    <td>37</td>
  </tr>
  <tr>
    <td>QF_AUFLIA</td>
    <td>1009</td>
    <td>0</td>
    <td>1009</td>
  </tr>
  <tr>
    <td>QF_AUFNIA</td>
    <td>21</td>
    <td>0</td>
    <td>21</td>
  </tr>
  <tr>
    <td>QF_AX</td>
    <td>551</td>
    <td>0</td>
    <td>551</td>
  </tr>
  <tr>
    <td>QF_BV</td>
    <td>26414 (6062 excluded<sup><a href="#fn1">1</a></sup>)</td>
    <td>17953</td>
    <td>50429</td>
  </tr>
  <tr>
    <td>QF_BVFP<sup><a href="#fn2">2</a></sup></td>
    <td>7 (1 excluded<sup><a href="#fn1">1</a></sup>)</td>
    <td>0</td>
    <td>8</td>
  </tr>
  <tr>
    <td>QF_FP<sup><a href="#fn2">2</a></sup></td>
    <td>34413 (5706 excluded<sup><a href="#fn1">1</a></sup>)</td>
    <td>215</td>
    <td>40334</td>
  </tr>
  <tr>
    <td>QF_IDL</td>
    <td>2094</td>
    <td>104</td>
    <td>2198</td>
  </tr>
  <tr>
    <td>QF_LIA</td>
    <td>5839</td>
    <td>302</td>
    <td>6141</td>
  </tr>
  <tr>
    <td>QF_LIRA</td>
    <td>6</td>
    <td>1</td>
    <td>7</td>
  </tr>
  <tr>
    <td>QF_LRA</td>
    <td>1626</td>
    <td>56</td>
    <td>1682</td>
  </tr>
  <tr>
    <td>QF_NIA</td>
    <td>8475</td>
    <td>925</td>
    <td>9400</td>
  </tr>
  <tr>
    <td>QF_NIRA</td>
    <td>2</td>
    <td>1</td>
    <td>3</td>
  </tr>
  <tr>
    <td>QF_NRA</td>
    <td>10184</td>
    <td>1356</td>
    <td>11540</td>
  </tr>
  <tr>
    <td>QF_RDL</td>
    <td>220</td>
    <td>35</td>
    <td>255</td>
  </tr>
  <tr>
    <td>QF_UF</td>
    <td>6649</td>
    <td>1</td>
    <td>6650</td>
  </tr>
  <tr>
    <td>QF_UFBV</td>
    <td>31</td>
    <td>0</td>
    <td>31</td>
  </tr>
  <tr>
    <td>QF_UFIDL</td>
    <td>441</td>
    <td>0</td>
    <td>441</td>
  </tr>
  <tr>
    <td>QF_UFLIA</td>
    <td>598</td>
    <td>0</td>
    <td>598</td>
  </tr>
  <tr>
    <td>QF_UFLRA</td>
    <td>1627</td>
    <td>3</td>
    <td>1630</td>
  </tr>
  <tr>
    <td>QF_UFNIA</td>
    <td>7</td>
    <td>0</td>
    <td>7</td>
  </tr>
  <tr>
    <td>QF_UFNRA</td>
    <td>34</td>
    <td>9</td>
    <td>43</td>
  </tr>
  <tr>
    <td>UF</td>
    <td>2839</td>
    <td>2909</td>
    <td>5748</td>
  </tr>
  <tr>
    <td>UFBV</td>
    <td>71</td>
    <td>129</td>
    <td>200</td>
  </tr>
  <tr>
    <td>UFIDL</td>
    <td>68</td>
    <td>12</td>
    <td>80</td>
  </tr>
  <tr>
    <td>UFLIA</td>
    <td>8404</td>
    <td>3736</td>
    <td>12140</td>
  </tr>
  <tr>
    <td>UFLRA</td>
    <td>25</td>
    <td>0</td>
    <td>25</td>
  </tr>
  <tr>
    <td>UFNIA</td>
    <td>2319</td>
    <td>1033</td>
    <td>3352</td>
  </tr>
  <tr>
    <td><b>Total</b></td>
    <td><b>154238 (11966 excluded<sup><a href="#fn1">1</a></sup>)</b></td>
    <td><b>30171</b></td>
    <td><b>196375</b></td>
  </tr>
</table>

<p>
  <span id="fn1">
    1. Excluded because they contain partial or underspecified
    operations (e.g., bit-vector division, <tt>fp.min</tt>).
  </span><br/>
  <span id="fn2">
    2. Floating-point divisions are considered experimental in 2015.
  </span>
</p>

<h2>Application Track</h2>

<table>
  <tr>
    <th>Logic</th>
    <th>Benchmarks eligible for SMT-COMP</th>
    <th>Benchmarks with unknown status<sup><a href="#fn3">3</a></sup></th>
    <th>Benchmarks in SMT-LIB</th>
  </tr>
  <tr>
    <td>ALIA</td>
    <td>24</td>
    <td>0</td>
    <td>24</td>
  </tr>
  <tr>
    <td>ANIA</td>
    <td>3</td>
    <td>0</td>
    <td>3</td>
  </tr>
  <tr>
    <td>AUFNIRA<sup><a href="#fn4">4</a></sup></td>
    <td>0</td>
    <td>165</td>
    <td>165</td>
  </tr>
  <tr>
    <td>LIA</td>
    <td>6</td>
    <td>0</td>
    <td>6</td>
  </tr>
  <tr>
    <td>QF_ALIA</td>
    <td>44</td>
    <td>0</td>
    <td>44</td>
  </tr>
  <tr>
    <td>QF_ANIA</td>
    <td>5</td>
    <td>0</td>
    <td>5</td>
  </tr>
  <tr>
    <td>QF_AUFLIA</td>
    <td>72</td>
    <td>0</td>
    <td>72</td>
  </tr>
  <tr>
    <td>QF_BV</td>
    <td>18</td>
    <td>0</td>
    <td>18</td>
  </tr>
  <tr>
    <td>QF_LIA</td>
    <td>65</td>
    <td>0</td>
    <td>65</td>
  </tr>
  <tr>
    <td>QF_LRA</td>
    <td>10</td>
    <td>0</td>
    <td>10</td>
  </tr>
  <tr>
    <td>QF_NIA</td>
    <td>10</td>
    <td>0</td>
    <td>10</td>
  </tr>
  <tr>
    <td>QF_UFLIA</td>
    <td>905</td>
    <td>0</td>
    <td>905</td>
  </tr>
  <tr>
    <td>QF_UFLRA</td>
    <td>3331</td>
    <td>2</td>
    <td>3333</td>
  </tr>
  <tr>
    <td>QF_UFNIA</td>
    <td>1</td>
    <td>0</td>
    <td>1</td>
  </tr>
  <tr>
    <td>UFLRA</td>
    <td>5358</td>
    <td>0</td>
    <td>5358</td>
  </tr>
  <tr>
    <td><b>Total</b></td>
    <td><b>9852</b></td>
    <td><b>167</b></td>
    <td><b>10019</b></td>
  </tr>
</table>

<p>
  <span id="fn3">
    3. For the application track, a benchmark is ineligible if its
    <u>first</u> <tt>check-sat</tt> command has unknown status.
    Otherwise, (some non-empty prefix of) the benchmark is eligible.
  </span><br/>
  <span id="fn4">
    4. As there are no eligible benchmarks in SMT-LIB, AUFNIRA is not
    actually an application track division in SMT-COMP 2015.
  </span>
</p>
