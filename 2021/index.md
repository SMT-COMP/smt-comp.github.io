## SMT-COMP 2021

The *16th International Satisfiability Modulo Theories Competition (SMT-COMP
2021)* is part of the [SMT Workshop
2021](https://smt-workshop.cs.uiowa.edu/2021/), affiliated with [CAV
2021](http://i-cav.org/2021/).  The SMT Workshop will include a block of time to
present the competitors and results of the competition.

### News
{% assign newsList = site.news_2021 | reverse %}
{% for news in newsList %}
- {{ news.newsdate | date_to_string }} [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key dates
 - **March 15**  &nbsp; Deadline for new benchmark contributions
 - **May 7** &nbsp; Final versions of competition tools
 - **May 30**    &nbsp; Deadline for first versions of solvers (for all tracks)
 - **June 13**   &nbsp; Deadline for final versions of solvers, including system descriptions
 - **July 18/19** &nbsp; SMT Workshop (presentation of results)

### Organizers
- [Haniel Barbosa](http://homepages.dcc.ufmg.br/~hbarbosa/) - Universidade Federal de Minas Gerais, Brazil
- [Jochen Hoenicke](https://jochen-hoenicke.de/) (chair) - Albert-Ludwigs-Universität Freiburg, Germany
- [Antti Hyvarinen](https://www.inf.usi.ch/postdoc/hyvarinen/) - Universita della Svizzera italiana, Switzerland

SMT-COMP 2021 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.
