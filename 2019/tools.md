---
layout: default
---
## Tools

{%- assign year = site.data.tools |where: "year", "2019" |first -%}
{% for tool in year.tools %}
### {{ tool.name }}

[**GitHub Repository**]({{ tool.repo }})  
[**Sources**]({{ tool.sources }})

  {% if tool.tracks %}
**SMT-COMP 2019 {{ tool.name }} Releases**
    {% for track in tool.tracks %}
      {% assign track_data = site.data.tracks |where: "raw_name", track.name |first %}
- [{{ track_data.pretty_name }}]({{ track.release.url }})
    {% endfor %}
  {% endif %}
{% endfor %}
