{%- assign sum_of_seeds = 0 -%}
{%- for solver in site.participants_split -%}
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
{% for track in site.data.tracks_split %}
<th>{{ track.pretty_name }}</th>
{% endfor %}
<th>Preliminary Solver ID</th>
<th>Final Solver ID</th>
<th>Seed</th>
<th>System Description</th>
<th>Solver Homepage</th>
<th>Contact</th>
</tr>
{%- for solver in site.participants_split -%}
<tr {% if solver.competing == "no" %}class = "noncompeting" {% endif %}>
<td>
<a href="{{ solver.url }}">{{ solver.name }}</a>{%- if solver.competing == "no" -%}<sup><a href="#nc">n</a></sup>{%- endif -%}
</td>
    {%- for track_descr in site.data.tracks_split -%}
<td>
        {%- assign this_track_found = false -%}
        {%- for slogic in solver.logics -%}
            {% if this_track_found == true -%}
                {%- break -%}
            {% endif %}
            {%- for strack in slogic.tracks -%}
                {%- if strack == track_descr.raw_name -%}
X
                    {%- assign this_track_found = true -%}
                    {%- break -%}
                {%- endif -%}
            {%- endfor -%}
        {%- endfor -%}
</td>
    {%- endfor -%}
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
{%- for track_descr in site.data.tracks_split -%}
    {%- assign num_p = 0 -%}
    {%- for solver in site.participants_split -%}
        {%- assign this_track_found = false -%}
        {%- for slogic in solver.logics -%}
            {%- if this_track_found == true -%}
                {%- break -%}
            {%- endif -%}
            {%- for strack in slogic.tracks -%}
                {%- if strack == track_descr.raw_name -%}
                    {%- assign num_p = num_p |plus: 1 -%}
                    {%- assign this_track_found = true -%}
                    {%- break -%}
                {%- endif -%}
            {%- endfor -%}
        {%- endfor -%}
    {%- endfor -%}
<td><b>{{num_p}}</b></td>
{%- endfor -%}
<td></td>
<td></td>
<td><b>{{ sum_of_seeds }} </b> (mod 2<sup>30</sup>)</td>
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

The opening value of the NYSE Composite Index on {{ nyse_date }} was
{{ nyse_value }}, resulting in a competition seed of {{ sum_of_seeds }} + {{
nyse_round }} = <b>{{ comp_seed }}</b>.

## Divisions

These are the logic divisions in which each solver is participating.

{% for logic in site.data.logics_split %}
### {{ logic.name }}
<table>
<tr>
<th>Solver</th>
    {%- for track in logic.tracks -%}
<th>
        {%- for track_descr in site.data.tracks_split -%}
            {%- if track == track_descr.raw_name -%}
                {{- track_descr.pretty_name -}}
                {%- break -%}
            {%- endif -%}
        {%- endfor -%}
</th>
    {%- endfor -%}
</tr>
    {%- for solver in site.participants_split -%}
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
        {%- for track_descr in site.data.tracks_split -%}
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

