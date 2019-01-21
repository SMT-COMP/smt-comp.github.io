## Benchmarks
SMT-COMP 2019 will use a large subset of the benchmarks available within
the 2019-05-20 release of SMT-LIB, as described in the competition
rules.

The SMT-LIB benchmarks are available in space [root/SMT/SMT-LIB benchmarks/2018-05-20](https://www.starexec.org/starexec/secure/explore/spaces.jsp?id=294532) on StarExec.

### Single Problem Track

{% assign n_benchmarks = 0 %}
{% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
        {% if track.name == "Single Problem Track" %}
            {% assign n_benchmarks = n_benchmarks | plus:1 %}

        {% endif %}
    {% endfor %}
{% endfor %}

All non-incremental SMT-LIB benchmarks are eligible for the Single
Problem Track.  In total there are {{ n_benchmarks }} Single Problem
Track divisions.

<table>
    <tr>
        <th>Logic</th>
        <th>Benchmarks eligible for SMT-COMP</th>
    </tr>
    {% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
    {% if track.name == "Single Problem Track" %}
    <tr>
        <td><a href="{{ benchmark.url }}">{{ benchmark.logicname }}</a></td>
        <td>{{ track.n_insts }} {% if track.n_excluded > 0 %}
({{ track.n_excluded }} excluded) {% endif %}</td>
    </tr>
    {% endif %}
    {% endfor %}
    {% endfor %}
</table>

### Incremental Track

{% assign n_benchmarks = 0 %}
{% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
        {% if track.name == "Incremental Track" %}
            {% assign n_benchmarks = n_benchmarks | plus:1 %}

        {% endif %}
    {% endfor %}
{% endfor %}

All incremental SMT-LIB benchmarks are eligible for the Incremental
Track.  In total there are {{ n_benchmarks }} Incremental
Track divisions.

<table>
    <tr>
        <th>Logic</th>
        <th>Benchmarks eligible for SMT-COMP</th>
    </tr>
    {% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
    {% if track.name == "Incremental Track" %}
    <tr>
        <td><a href="{{ benchmark.url }}">{{ benchmark.logicname }}</a></td>
        <td>{{ track.n_insts }} {% if track.n_excluded > 0 %}
({{ track.n_excluded }} excluded) {% endif %}</td>
    </tr>
    {% endif %}
    {% endfor %}
    {% endfor %}
</table>

### Unsat Core Track

{% assign n_benchmarks = 0 %}
{% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
        {% if track.name == "Unsat Core Track" %}
            {% assign n_benchmarks = n_benchmarks | plus:1 %}

        {% endif %}
    {% endfor %}
{% endfor %}

All unsatisfiable Single Core Track SMT-LIB benchmarks are eligible for the Unsat Core Track.  In total there are {{ n_benchmarks }} Unsat Core
Track divisions.

<table>
    <tr>
        <th>Logic</th>
        <th>Benchmarks eligible for SMT-COMP</th>
    </tr>
    {% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
    {% if track.name == "Unsat Core Track" %}
    <tr>
        <td><a href="{{ benchmark.url }}">{{ benchmark.logicname }}</a></td>
        <td>{{ track.n_insts }} {% if track.n_excluded > 0 %}
({{ track.n_excluded }} excluded) {% endif %}</td>
    </tr>
    {% endif %}
    {% endfor %}
    {% endfor %}
</table>

### Challenge Track

{% assign n_benchmarks = 0 %}
{% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
        {% if track.name == "Challenge Track" %}
            {% assign n_benchmarks = n_benchmarks | plus:1 %}

        {% endif %}
    {% endfor %}
{% endfor %}

A selection of hard SMT-LIB benchmarks were chosen to the Challenge
Track.  In total there are {{ n_benchmarks }} Challenge Track
divisions.

<table>
    <tr>
        <th>Logic</th>
        <th>Benchmarks eligible for SMT-COMP</th>
    </tr>
    {% for benchmark in site.benchmarks %}
    {% for track in benchmark.tracks %}
    {% if track.name == "Challenge Track" %}
    <tr>
        <td><a href="{{ benchmark.url }}">{{ benchmark.logicname }}</a></td>
        <td>{{ track.n_insts }} {% if track.n_excluded > 0 %}
({{ track.n_excluded }} excluded) {% endif %}</td>
    </tr>
    {% endif %}
    {% endfor %}
    {% endfor %}
</table>

