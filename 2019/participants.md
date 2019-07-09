{%- assign sum_of_seeds = 0 -%}
{%- for solver in site.participants_2019 -%}
    {%- assign sum_of_seeds = sum_of_seeds | plus: solver.seed -%}
{%- endfor -%}
{%- assign sum_of_seeds = sum_of_seeds | modulo: 1073741824 -%}

{%- assign nyse_info = site.data.nyse_composite_index -%}
{%- assign nyse_date = nyse_info.date -%}
{%- assign nyse_value = nyse_info.value -%}
{%- assign nyse_round = nyse_value | round -%}
{%- assign comp_seed = sum_of_seeds | plus: nyse_round %}

## Participants

The following solvers have been submitted to SMT-COMP 2019 or were entered as
non-competing solvers by the organizers for comparison.

<table>
<tr>
<th>Solver</th>
{% for track in site.data.tracks %}
<th>{{ track.pretty_name }}</th>
{% endfor %}
<th>Preliminary Solver ID</th>
<th>Final Solver ID</th>
<th>Seed</th>
<th>System Description</th>
</tr>
{%- for solver in site.participants_2019 -%}
<tr {% if solver.competing == "no" %}class = "noncompeting" {% endif %}>
<td>
<a href="{{ solver.url }}">{{ solver.name }}</a>{%- if solver.competing == "no" -%}<sup><a href="#nc">n</a></sup>{%- endif -%}
</td>
{%- for track in site.data.tracks -%}
<td class="center">
  {%- assign in_track = solver.logics |where: "tracks", track.raw_name |first -%}
  {% if in_track %}
  X
  {% endif %}
</td>
{%- endfor -%}
<td class="right">{{- solver.preliminaryID -}}</td>
<td class="right">{{- solver.finalID -}}</td>
<td class="right">{{- solver.seed -}}</td>
<td class="right"><a href="/2019/system-descriptions/{{ solver.sysDescrUrl }}">{{ solver.sysDescrName }}</a></td>
</tr>
{% endfor %}

{%- assign num_solvers_list = "" -%}
{%- assign num_solvers_comp_list = "" -%}
{%- assign num_solvers_non_comp_list = "" -%}
{%- for track in site.data.tracks -%}
    {%- assign num_solvers = 0 -%}
    {%- assign num_solvers_comp = 0 -%}
    {%- assign num_solvers_non_comp = 0 -%}
    {%- for solver in site.participants_2019 -%}
        {%- assign in_track = solver.logics |where: "tracks", track.raw_name |first -%}
        {% if in_track %}
          {%- assign num_solvers = num_solvers |plus: 1 -%}
          {% if solver.competing == "yes" %}
            {% assign num_solvers_comp = num_solvers_comp |plus: 1 -%}
          {% else %}
            {% assign num_solvers_non_comp = num_solvers_non_comp |plus: 1 -%}
          {% endif %}
        {%- endif -%}
    {%- endfor -%}
    {%- assign num_solvers_list = num_solvers_list
                                  |append: num_solvers
                                  |append: ":" -%}
    {%- assign num_solvers_comp_list = num_solvers_comp_list
                                      |append: num_solvers_comp
                                      |append: ":" -%}
    {%- assign num_solvers_non_comp_list = num_solvers_non_comp_list
                                      |append: num_solvers_non_comp
                                      |append: ":" -%}
{%- endfor -%}
{%- assign num_solvers_list = num_solvers_list |split: ":" -%}
{%- assign num_solvers_comp_list = num_solvers_comp_list |split: ":" -%}
{%- assign num_solvers_non_comp_list = num_solvers_non_comp_list |split: ":" -%}

<tr class="total">
<td>Total - competing</td>
{% for num in num_solvers_comp_list %}
<td class="center">{{ num }}</td>
{% endfor %}
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>Total - non-competing</td>
{% for num in num_solvers_non_comp_list %}
<td class="center">{{ num }}</td>
{% endfor %}
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td><b>Total</b></td>
{% for num in num_solvers_list %}
<td class="center"><b>{{ num }}</b></td>
{% endfor %}
<td></td>
<td></td>
<td><b>{{ sum_of_seeds }} </b> (mod 2<sup>30</sup>)</td>
<td></td>
</tr>
</table>
<p>
  <span id="nc">
    n Non-competing.
  </span><br/>
</p>

The opening value of the NYSE Composite Index on {{ nyse_date }} was
{{ nyse_value }}, resulting in a competition seed of {{ sum_of_seeds }} + {{
nyse_round }} = <b>{{ comp_seed }}</b>.

## Divisions

These are the logic divisions in which each solver is participating.

{% for logic in site.data.logics %}
### {{ logic.name }}
<table>
<tr>
<th>Solver</th>
  {%- for track in logic.tracks -%}
<th class="center">
    {% assign tt = site.data.tracks |where: "raw_name", track  |first %}
    {{ tt.pretty_name }}
</th>
  {%- endfor -%}
</tr>
  {%- for solver in site.participants_2019 -%}
    {%- assign in_logic = solver.logics |where: "name", logic.name |first -%}
    {% unless in_logic %}{% continue %}{% endunless %}
<tr {% if solver.competing == "no" %} class = "noncompeting" {%- endif -%}>
<td>
<a href="{{ solver.url }}">{{ solver.name }}</a>
    {%- if solver.competing == "no" -%}
<sup><a href="#nc">n</a></sup>
    {%- endif -%}
</td>
    {%- for track in logic.tracks -%}
<td class="center">
          {%- assign in_logic = solver.logics |where: "name", logic.name |where: "tracks", track.raw_name |first -%}
          {% if in_logic %}
X
          {%- endif -%}
</td>
    {%- endfor -%}
</tr>
  {%- endfor -%}


  {%- assign num_solvers_list = "" -%}
  {%- assign num_solvers_comp_list = "" -%}
  {%- assign num_solvers_non_comp_list = "" -%}
  {%- for track in site.data.tracks -%}
      {%- assign num_solvers = 0 -%}
      {%- assign num_solvers_comp = 0 -%}
      {%- assign num_solvers_non_comp = 0 -%}
      {%- for solver in site.participants_2019 -%}
          {%- assign in_logic = solver.logics |where: "name", logic.name |where: "tracks", track.raw_name |first -%}
          {% if in_logic %}
            {%- assign num_solvers = num_solvers |plus: 1 -%}
            {% if solver.competing == "yes" %}
              {% assign num_solvers_comp = num_solvers_comp |plus: 1 -%}
            {% else %}
              {% assign num_solvers_non_comp = num_solvers_non_comp |plus: 1 -%}
            {% endif %}
          {%- endif -%}
      {%- endfor -%}
      {%- if num_solvers > 0 -%}
        {%- assign num_solvers_list = num_solvers_list
                                      |append: num_solvers
                                      |append: ":" -%}
        {%- assign num_solvers_comp_list = num_solvers_comp_list
                                          |append: num_solvers_comp
                                          |append: ":" -%}
        {%- assign num_solvers_non_comp_list = num_solvers_non_comp_list
                                          |append: num_solvers_non_comp
                                          |append: ":" -%}
      {%- endif -%}
  {%- endfor -%}
  {%- assign num_solvers_list = num_solvers_list |split: ":" -%}
  {%- assign num_solvers_comp_list = num_solvers_comp_list |split: ":" -%}
  {%- assign num_solvers_non_comp_list = num_solvers_non_comp_list |split: ":" -%}
<tr class="total">
<td>Total - competing</td>
  {% for num in num_solvers_comp_list %}
<td class="center">{{ num }}</td>
  {% endfor %}
</tr>
<tr>
<td>Total - non-competing</td>
  {% for num in num_solvers_non_comp_list %}
<td class="center">{{ num }}</td>
  {% endfor %}
</tr>
<tr>
<td><b>Total</b></td>
  {% for num in num_solvers_list %}
<td class="center"><b>{{ num }}</b></td>
  {% endfor %}
</tr>
</table>
{% endfor %}

