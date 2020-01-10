## SMT-COMP 2020

The *15th International Satisfiability Modulo Theories Competition
(SMT-COMP 2020)* is part of the SMT Workshop 2020,
affiliated with [IJCAR 2020](https://ijcar2020.org/).
The SMT Workshop will include a block of time to present the competitors
and results of the competition.

### News
{% assign newsList = site.news_2020 | reverse %}
{% for news in newsList %}
- {{ news.newsdate | date_to_string }} [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key dates
 - **TBA**  &nbsp; Deadline for new benchmark contributions
 - **TBA**    &nbsp; Final versions of competition tools
 - **TBA**   &nbsp; Deadline for first versions of solvers (for all tracks)
 - **TBA**   &nbsp; Deadline for final versions of solvers, including system descriptions
 - **July 4-5** &nbsp; SMT Workshop (presentation of results)

### Organizers
- [Haniel Barbosa](http://homepages.dcc.ufmg.br/~hbarbosa/) - Universidade Federal de Minas Gerais, Brazil
- [Antti Hyvarinen](https://www.inf.usi.ch/postdoc/hyvarinen/) (chair) - Universita della Svizzera italiana, Switzerland
- [Jochen Hoenicke](https://jochen-hoenicke.de/) - Albert-Ludwigs-Universität Freiburg, Germany

SMT-COMP 2020 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.

<!-- ### Acknowledgment -->
<!-- - [Mathias Preiner](https://cs.stanford.edu/people/preiner) (benchmark selection and scoring scripts) -->
<!-- - [Aaron Stump](http://homepage.divms.uiowa.edu/~astump/) (StarExec) -->
<!-- - [Andres N&ouml;tzli](https://cs.stanford.edu/people/noetzli/) (trace executor extension) -->
<!-- - Marco Gario and Andrea Micheli ([pySMT](https://github.com/pysmt/pysmt)) -->
<!-- - [Martin Riener](https://www.logic.at/staff/riener/) (logistics for certificates and trophies) -->
