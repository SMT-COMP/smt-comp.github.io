## Participants

These solvers have been submitted to SMT-COMP 2019 or were entered as
non-competing solvers by the organizers for comparison.

<table>
    <tr>
        <th>Solver</th>
        <th>Competing</th>
        <th>Single Problem Track</th>
        <th>Incremental Track</th>
        <th>Unsat-Core Track</th>
        <th>Challenge Track</th>
        <th>Model Validation Track</th>
        <th>Preliminary Version Solver ID</th>
        <th>Final Version Solver ID</th>
        <th>Seed</th>
        <th>System Description</th>
        <th>Solver Homepage</th>
        <th>Contact</th>
    </tr>
    {% for solver in site.participants %}
    {% assign sqt = "" %}
    {% assign it = "" %}
    {% assign uct = "" %}
    {% assign ct = "" %}
    {% assign mvt = "" %}

    {% for logic in solver.logics %}
        {% for track in logic.tracks %}
            {% if track == "track_single_query" %} {% assign sqt = "X" %} {% endif %}
            {% if track == "track_incremental" %} {% assign it = "X" %} {% endif %}
            {% if track == "track_unsat_core" %} {% assign uct = "X" %} {% endif %}
            {% if track == "track_challenge" %} {% assign ct = "X" %} {% endif %}
            {% if track == "track_model_validation" %} {% assign mvt = "X" %} {% endif %}
        {% endfor %}
    {% endfor %}


    <tr>
        <td><a href="{{ solver.url }}">{{ solver.name }}</a></td>
        <td>{{ solver.competing }}</td>
        <td>{{ sqt }} </td>
        <td>{{ it }} </td>
        <td>{{ uct }}</td>
        <td>{{ ct }}</td>
        <td>{{ mvt }}</td>
        <td>{{ solver.preliminaryID }}</td>
        <td>{{ solver.finalID }}</td>
        <td>{{ solver.seed }}</td>
        <td><a href="/2019/system-descriptions/{{ solver.sysDescrUrl }}">{{ solver.sysDescrName }}</a></td>
        <td><a href="{{ solver.solverHomePage }}">{{ solver.solverHomePage }}</a></td>
        <td>{{ solver.contactName }} <a href="mailto:{{ solver.contactEmail }}"> ({{ solver.contactEmail }})</a></td>
    </tr>
    {% endfor %}
</table>
