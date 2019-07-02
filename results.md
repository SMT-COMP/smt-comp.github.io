---
layout: default
---
## SMT-COMP 2019 Results

{% for logic in site.data.results_index %}
- {{ logic.name }} ({% for track in logic.tracks %}[{{ track.name }}]({{track.results}}) {% endfor %})
{% endfor %}
