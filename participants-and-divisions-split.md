---
tracks:
  - raw_name: track_single_query
    pretty_name: Single Query Track
    footnote: fn1
    abbr: sq
  - raw_name: track_incremental
    pretty_name: Incremental Track
    footnote: fn2
    abbr: i
  - raw_name: track_challenge
    pretty_name: Challenge Track
    footnote: fn3
    abbr: c
  - raw_name: track_unsat_core
    pretty_name: Unsat Core Track
    footnote: fn4
    abbr: uc
  - raw_name: track_model_validation
    pretty_name: Model Validation Track
    footnote: fn5
    abbr: mv
---
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
    {%- for solver in site.participants -%}
    {%- assign sqt = "" -%}
    {%- assign it = "" -%}
    {%- assign uct = "" -%}
    {%- assign ct = "" -%}
    {%- assign mvt = "" -%}

    {%- for logic in solver.logics -%}
        {%- for track in logic.tracks -%}
            {%- if track == "track_single_query" -%} {%- assign sqt = "X" -%} {%- endif -%}
            {%- if track == "track_incremental" -%} {%- assign it = "X" -%} {%- endif -%}
            {%- if track == "track_unsat_core" -%} {%- assign uct = "X" -%} {%- endif -%}
            {%- if track == "track_challenge" -%} {%- assign ct = "X" -%} {%- endif -%}
            {%- if track == "track_model_validation" -%} {%- assign mvt = "X" -%} {%- endif -%}
        {%- endfor -%}
    {%- endfor -%}

    <tr {% if solver.competing == "no" %}class = "noncompeting" {% endif %}>
        <td>
          <a href="{{ solver.url }}">{{ solver.name }}</a>{%- if solver.competing == "no" -%}<sup><a href="#nc">n</a></sup>{%- endif -%}
        </td>
        <td>{{- sqt -}} </td>
        <td>{{- it -}} </td>
        <td>{{- uct -}}</td>
        <td>{{- ct -}}</td>
        <td>{{- mvt -}}</td>
        <td>{{- solver.preliminaryID -}}</td>
        <td>{{- solver.finalID -}}</td>
        <td>{{- solver.seed -}}</td>
        <td><a href="/2019/system-descriptions/{{ solver.sysDescrUrl }}">{{ solver.sysDescrName }}</a></td>
        <td><a href="{{ solver.solverHomePage }}">{{ solver.solverHomePage }}</a></td>
        <td><a href="mailto:{{ solver.contact }}"> {{ solver.contact }}</a></td>
    </tr>
    {% endfor %}
    <tr>
      <td><b>Total</b></td>
      <td><b>41</b></td>
      <td><b>17</b></td>
      <td><b>9</b></td>
      <td><b>20</b></td>
      <td><b>11</b></td>
      <td></td>
      <td></td>
      <td><b>933722448</b> (mod 2<sup>30</sup>)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
</table>
<p>
  <span id="nc">
    n Non-competing.
  </span><br/>
</p>

The opening value of the NYSE Composite Index on 2019-06-03 was 12888.51, resulting in a competition seed of 933722448 + 12889 = <b>933735337</b>.

## Divisions

These are the logic divisions in which each solver is participating.

{% for logic in site.data.logics %}
### {{ logic.name }}
<table>
<tr>
<th>Solver</th>
    {%- for track in logic.tracks -%}
<th>
        {%- for track_descr in page.tracks -%}
            {%- if track == track_descr.raw_name -%}
                {{- track_descr.pretty_name -}}
                {%- break -%}
            {%- endif -%}
        {%- endfor -%}
</th>
    {%- endfor -%}
</tr>
    {%- for solver in site.participants -%}
        {%- assign participates_in_logic = false -%}
        {%- for s_logic in solver.logics -%}
            {%- if s_logic.name == logic.name -%}
                {%- assign participates_in_logic = true -%}
                {%- break -%}
            {%- endif -%}
        {%- endfor -%}
        {%- if participates_in_logic == false -%}
            {%- continue -%}
        {%- endif -%}
<tr {% if solver.competing == "no" %} class = "noncompeting" {%- endif -%}>
<td>
<a href="{{ solver.url }}">{{ solver.name }}</a>
        {%- if solver.competing == "no" -%}
<sup><a href="#nc">n</a></sup>
        {%- endif -%}
</td>
        {%- for track_descr in page.tracks -%}
            {%- for track in logic.tracks -%}
                {%- if track == track_descr.raw_name -%}
<td>
                    {%- for s_logic in solver.logics -%}
                        {%- if s_logic.name == logic.name -%}
                            {%- for s_track in s_logic.tracks -%}
                                {%- if track == s_track -%}
X
                                    {%- break -%}
                                {%- endif -%}
                            {%- endfor -%}
                            {%- break -%}
                        {%- endif -%}
                    {%- endfor -%}
</td>
                {%- endif -%}
            {%- endfor -%}
        {%- endfor -%}
</tr>
    {%- endfor -%}
</table>
{% endfor %}

