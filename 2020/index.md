## SMT-COMP 2020

The *15th International Satisfiability Modulo Theories Competition (SMT-COMP
2020)* is part of the [SMT Workshop
2020](http://smt-workshop.cs.uiowa.edu/2020/), affiliated with [IJCAR
2020](https://ijcar2020.org/).  The SMT Workshop will include a block of time to
present the competitors and results of the competition.

### News
{% assign newsList = site.news_2020 | reverse %}
{% for news in newsList %}
- <span class="date">{{ news.newsdate | date_to_string }}</span> [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key dates
 - **March 1**  &nbsp; Deadline for new benchmark contributions
 - **April 20** &nbsp; Final versions of competition tools
 - **May 4**    &nbsp; Deadline for first versions of solvers (for all tracks)
 - **May 26**   &nbsp; Deadline for final versions of solvers, including system descriptions
 - **July 5-6** &nbsp; SMT Workshop (presentation of results)

### Organizers
- [Haniel Barbosa](http://homepages.dcc.ufmg.br/~hbarbosa/) - Universidade Federal de Minas Gerais, Brazil
- [Jochen Hoenicke](https://jochen-hoenicke.de/) - Albert-Ludwigs-Universität Freiburg, Germany
- [Antti Hyvarinen](https://www.inf.usi.ch/postdoc/hyvarinen/) (chair) - Universita della Svizzera italiana, Switzerland

SMT-COMP 2020 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.

### Acknowledgment
- [Aina Niemetz](https://cs.stanford.edu/people/niemetz) (Insights and support)
- [Andres N&ouml;tzli](https://cs.stanford.edu/people/noetzli/) (String benchmarks)
- [Mathias Preiner](https://cs.stanford.edu/people/preiner) (StarExec benchmark uploading, insights and support)
- [Aaron Stump](http://homepage.divms.uiowa.edu/~astump/) (StarExec)
