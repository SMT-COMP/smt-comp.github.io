## SMT-COMP 2019

The 14th International Satisfiability Modulo Theories Competition
(SMT-COMP 2019) is part of the SMT Workshop 2019, affiliated with
[SAT 2019](http://sat2019.tecnico.ulisboa.pt).

The SMT Workshop will include a block of time to present the competitors
and results of the competition.

### News
{% for news in site.news  %}
- {{ news.date | date_to_string }} [{{news.title}}]({{ news.url }})
{% endfor %}
### Key dates
See the [rules]() for the complete timeline
- July 7-9: SMT Workshop (presentation of results)

### Organizers
SMT-COMP 2019 is organized by:
{% for organizer in site.organizers %}
- [{{ organizer.name }}](mailto:{{ organizer.email }}) {% if organizer.chair %} (competition co-chair)
  {% endif %}
{% endfor %}

