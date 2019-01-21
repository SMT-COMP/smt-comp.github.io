## Participants

These solvers have been submitted to SMT-COMP 2019 or were entered as
non-competing solvers by the organizers for comparison.

<table>
    <tr>
        <th>Solver</th>
        <th>Single Problem Track</th>
        <th>Incremental Track</th>
        <th>Unsat-Core Track</th>
        <th>Challenge Track</th>
        <th>Preliminary Version Solver ID</th>
        <th>Final Version Solver ID</th>
        <th>Seed</th>
        <th>System Description</th>
        <th>Solver Homepage</th>
        <th>Contact</th>
    </tr>
    {% for solver in site.participants %}
    {% assign spt = "" %}
    {% assign it = "" %}
    {% assign uct = "" %}
    {% assign ct = "" %}

    {% for logic in solver.logics %}
        {% for track in logic.tracks %}
            {% if track == "Single Problem Track" %} {% assign spt = "X" %} {% endif %}
            {% if track == "Incremental Track" %} {% assign it = "X" %} {% endif %}
            {% if track == "Unsat Core Track" %} {% assign uct = "X" %} {% endif %}
            {% if track == "Challenge Track" %} {% assign ct = "X" %} {% endif %}
        {% endfor %}
    {% endfor %}


    <tr>
        <td><a href="{{ solver.url }}">{{ solver.name }}</a></td>
        <td>{{ spt }} </td>
        <td>{{ it }} </td>
        <td>{{ uct }}</td>
        <td>{{ ct }}</td>
        <td>{{ solver.preliminaryID }}</td>
        <td>{{ solver.finalID }}</td>
        <td>{{ solver.seed }}</td>
        <td><a href="{{ solver.sysDescUrl }}">{{ solver.sysDescName }}</a></td>
        <td><a href="{{ solver.solverHomePage }}">{{ solver.solverHomePage }}</a></td>
        <td>{{ solver.contactName }} <a href="mailto:{{ solver.contactEmail }}"> ({{ solver.contactEmail }})</a></td>
    </tr>
    {% endfor %}
</table>
