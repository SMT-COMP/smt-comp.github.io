---
layout: default
title: SMT-COMP 2017
---

## SMT-COMP 2017

The *12th International Satisfiability Modulo Theories Competition
(SMT-COMP 2017)* is part of the
[SMT Workshop 2017](http://smt-workshop.cs.uiowa.edu/2017/),
affiliated with [CAV 2017](http://cavconference.org/2017/).
The SMT Workshop will include a block of time to present
the competitors and results of the competition.

### News
{% assign newsList = site.news_2017 | reverse %}
{% for news in newsList %}
- <span class="date">{{ news.newsdate | date_to_string }}</span> [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key Dates
- **May 1** &nbsp; Deadline for new benchmark contributions
- **June 4** &nbsp; Deadline for first versions of solvers
- **June 19** &nbsp; Deadline for final versions of solvers
- **July 22-23** &nbsp; SMT Workshop (presentation of results)

### Organizers

- [Matthias Heizmann](https://swt.informatik.uni-freiburg.de/staff/heizmann) - Universit&auml;t Freiburg, Germany
- [Giles Reger](http://www.cs.man.ac.uk/~regerg/) - University of Manchester, UK
- [Tjark Weber](http://user.it.uu.se/~tjawe125/) (chair) - Uppsala University, Sweden

SMT-COMP 2017 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.
