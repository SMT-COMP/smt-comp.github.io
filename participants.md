## Participants

The following solvers have been submitted to SMT-COMP 2019 or were entered as
non-competing solvers by the organizers for comparison.

<table>
    <tr>
        <th>Solver</th>
        <th>Single Query Track</th>
        <th>Incremental Track</th>
        <th>Unsat-Core Track</th>
        <th>Challenge Track</th>
        <th>Model Validation Track</th>
        <th>Preliminary Solver ID</th>
        <th>Final Solver ID</th>
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

    <tr {% if solver.competing == "no" %}class = "noncompeting" {% endif %}>
        <td>
          <a href="{{ solver.url }}">
            {{ solver.name }}{% if solver.competing == "no" %}<sup>n</sup>{% endif %}
          </a>
        </td>
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
        <td><a href="mailto:{{ solver.contact }}"> {{ solver.contact }}</a></td>
    </tr>
    {% endfor %}
    <tr>
      <td><b>Total</b></td>
      <td><b>41</b></td>
      <td><b>17</b></td>
      <td><b>10</b></td>
      <td><b>21</b></td>
      <td><b>11</b></td>
      <td></td>
      <td></td>
      <td><b>912668687</b> (mod 2<sup>30</sup>)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
</table>
n. Non-competing.

The opening value of the NYSE Composite Index on 2019-06-03 was 12888.51, resulting in a competition seed of 912668687 + 12889 = <b>912681576</b>.
