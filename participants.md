## Participants

These solvers have been submitted to SMT-COMP 2019 or were entered as
non-competing solvers by the organizers for comparison.

<table>
    <tr>
        <th>Solver</th>
        <th>Single Problem Track</th>
        <th>Incremental Track</th>
        <th>Unsat-Core Track</th>
<!--
        <th>Preliminary Version Solver ID</th>
        <th>Final Version Solver ID</th>
        <th>Seed</th>
-->
        <th>System Description</th>
        <th>Contact</th>
    </tr>
    {% for solver in site.participants %}
    <tr>
        <td><a href="{{ solver.url }}">{{ solver.name}}</a></td>
        <td>{% if solver.nonIncrementalTrack %}X{% endif %}</td>
        <td>{% if solver.incrementalTrack %}X{% endif %}</td>
        <td>{% if solver.unsatCoreTrack %}X{% endif %}</td>
<!--        <td>{{ solver.preliminaryID }}</td>
        <td>{{ solver.finalID }}</td>
        <td>{{ solver.seed }}</td>
-->
        <td><a href="{{ solver.sysDescUrl }}">{{ solver.sysDescName }}</a></td>
        <td>{{ solver.contactName }} <a href="mailto:{{ solver.contactEmail }}"> ({{ solver.contactEmail }})</a></td>
    </tr>
    {% endfor %}
</table>
