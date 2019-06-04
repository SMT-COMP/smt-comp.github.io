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

<table>
<tr>
<th>Solver</th>
{% for logic in site.data.logics %}
<th>{{- logic.name -}}{%- assign first=true -%}<sup>
{%- for track in logic.tracks -%}
{%- for track_descr in page.tracks -%}
{%- if track == track_descr.raw_name -%}
{%- if first == true -%}
<a href="#{{- track_descr.footnote -}}">{{ track_descr.abbr }}</a>
{%- assign first=false -%}
{%- else -%}
,<a href="#{{- track_descr.footnote -}}">{{ track_descr.abbr }}</a>
{%- endif -%}
{%- endif -%}
{%- endfor -%}
{%- endfor -%}
</sup>
</th>
{% endfor %}
</tr>
{% for solver in site.participants %}
<tr {% if solver.competing == "no" %} class = "noncompeting" {%- endif -%}>
<td>
<a href="{{ solver.url }}">{{ solver.name }}</a>
<sup>
{%- assign first_sup=true -%}
{%- for track_descr in page.tracks -%}
    {%- assign this_track_found=false -%}
    {%- for logic in solver.logics -%}
        {%- if this_track_found == true -%}
            {%- break -%}
        {%- endif -%}
        {%- for strack in logic.tracks -%}
            {%- if track_descr.raw_name == strack -%}
                {%- assign this_track_found=true -%}
                {%- if first_sup == true -%}
<a href="#{{- track_descr.footnote -}}">{{ track_descr.abbr }}</a>
                    {%- assign first_sup = false -%}
                {%- else -%}
,<a href="#{{- track_descr.footnote -}}">{{ track_descr.abbr }}</a>
                {%- endif -%}
                {%- continue -%}
            {%- endif -%}
        {%- endfor -%}
    {%- endfor -%}
{%- endfor -%}
</sup>
{%- if solver.competing == "no" -%}
<sup>,<a href="#nc">n</a></sup>
{%- endif -%}
</td>
{%- for logic in site.data.logics -%}
<td>
{%- for slogic in solver.logics -%}
{%- if slogic.name == logic.name -%}X{%- endif -%}
{%- endfor -%}
</td>
{%- endfor -%}
</tr>
{%- endfor -%}
</table>

<p>
  {%- for track_descr in page.tracks -%}
  <span id="{{ track_descr.footnote }}">
    {{ track_descr.abbr }} {{ track_descr.pretty_name }}
  </span><br/>
  {%- endfor -%}
</p>
