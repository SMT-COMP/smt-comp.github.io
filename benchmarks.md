## Benchmarks
SMT-COMP 2019 will use a large subset of the benchmarks available within
the 2019-05-20 release of SMT-LIB, as described in the competition
rules.

The SMT-LIB benchmarks are available in space [root/SMT/SMT-LIB benchmarks/2018-05-20](https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=294532) on StarExec.

### Single Problem Track

{% assign n_benchmarks = 0 %}
{% for benchmark in site.main-benchmarks %}
  {% assign n_benchmarks = n_benchmarks | plus:1 %}
{% endfor %}

All non-incremental SMT-LIB benchmarks are eligible for the Single
Problem Track.  In total there are {{ n_benchmarks }} Single Problem
Track divisions.

<table>
    <tr>
        <th>Logic</th>
        <th>Benchmarks eligible for SMT-COMP</th>
    </tr>
    {% for benchmark in site.main-benchmarks %}
    <tr>
        <td><a href="{{ benchmark.url }}">{{ benchmark.name }}</a></td>
        <td>{{ benchmark.number }} {% if benchmark.excluded > 0 %}
({{ benchmark.excluded }} excluded) {% endif %}</td>
    </tr>
    {% endfor %}
</table>

