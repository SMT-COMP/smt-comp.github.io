---
layout: default
---
## SMT-COMP 2019 Results

{% for logic in site.data.results_index %}
  {%- assign logic_str = "" -%}
  {% for track in logic.tracks %}
        {%- assign logic_str = logic_str |append: "[" |append: track.name |append: "](" |append: track.results |append: ")" |append: ":" -%}
  {% endfor %}
  {%- assign logic_str = logic_str | split: ":" -%}
  - {{ logic.name }} ({{ logic_str |join: ", " }})
{% endfor %}
