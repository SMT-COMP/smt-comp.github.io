---
layout: default
---
## SMT-COMP 2019 Results

### Summary
{% for summary in site.results_summary_2019 %}
{% assign track = site.data.tracks |where: "raw_name", summary.track  |first %}
{% assign track = track.pretty_name %}
- [{{ track }}]({{ summary.url }})
{% endfor %}

### Divisions
{% assign results = site.results_2019 |group_by: 'division' %}
{% for result in results %}
  {%- assign track_str = "" -%}
  {% for item in result.items %}
    {% assign track = site.data.tracks |where: "raw_name", item.track  |first %}
    {% assign track = track.pretty_name %}
    {%- assign track_str = track_str |append: "["
                                     |append: track
                                     |append: "]("
                                     |append: item.url
                                     |append: ")"
                                     |append: ":" -%}
  {% endfor %}
  {%- assign track_str = track_str | split: ":" -%}
  - **{{ result.name }}**
    {% for ts in track_str %}
    - {{ ts -}}
    {% endfor %}
{% endfor %}
