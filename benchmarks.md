## Benchmarks
SMT-COMP 2019 will use a large subset of the benchmarks available within
the 2019-05-20 release of SMT-LIB, as described in the competition
rules.

{% for track_descr in site.data.tracks %}

    {% assign n_divisions = 0 %}
    {%-for benchmark in site.benchmarks %}
        {%- for track in benchmark.tracks -%}
            {%- if track.name == track_descr.raw_name -%}
                {%- if track.n_insts > 0 -%}
                    {%- assign n_divisions = n_divisions | plus:1 -%}
                {%- endif -%}
            {%- endif -%}
        {%- endfor -%}
    {% endfor %}

### {{ track_descr.pretty_name }}

    {% if n_divisions == 0 %}
The {{ track_descr.pretty_name }} divisions are not yet available.
        {% continue %}
    {% endif %}


In total there are
{{ n_divisions }} divisions in the {{ track_descr.pretty_name }}.

{% for sel_bm in site.data.selected_benchmarks %}
    {%- if sel_bm.raw_name == track_descr.raw_name -%}
The list of selected benchmarks is available [here]({{ sel_bm.url }}).
        {%- break -%}
    {%- endif -%}
{% endfor %}

<table>
<tr>
<th>Division</th>
<th>Number of Included Benchmarks</th>
</tr>
    {% assign total = 0 %}
    {%- for benchmark in site.benchmarks -%}
        {%- for track in benchmark.tracks -%}
            {%- if track.name == track_descr.raw_name -%}
                {%- if track.n_insts > 0 -%}
<tr {% if track.status == "non-competitive" %} class = "noncompeting" {% endif %}>
<td><a href="{{ benchmark.url }}">{{ benchmark.division }}</a>{%- if
track.status == "non-competitive" -%}<sup><a href="#nc">n</a></sup>{%-
endif -%}</td>
<td>{{ track.n_insts }}
                    {%- assign total = total | plus: track.n_insts -%}
                    {% if track.n_excluded > 0 %}
({{ track.n_excluded }} excluded)
                    {% endif %}
</td>
</tr>
                {%- endif -%}
            {%- endif -%}
        {%- endfor -%}
    {%- endfor -%}
<tr>
<td>
<b>Total</b>
</td>
<td>
<b>{{ total }}</b>
</td>
</tr>
</table>

{% endfor %}

<p>
  <span id="nc">
    n Non-competing.
  </span><br/>
</p>

