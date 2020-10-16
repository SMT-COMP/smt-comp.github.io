## SMT-COMP 2018

The *13th International Satisfiability Modulo Theories Competition
(SMT-COMP 2018)* is part of the
[SMT Workshop 2018](http://smt-workshop.cs.uiowa.edu/2018/),
affiliated with [FLoC 2018](http://www.floc2018.org/).
The SMT Workshop will include a block of time to present
the competitors and results of the competition.

### News
{% assign newsList = site.news_2018 | reverse %}
{% for news in newsList %}
- <span class="date">{{ news.newsdate | date_to_string }}</span> [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key Dates
 - **April 8**    &nbsp; Deadline for new benchmark contributions
 - **May 19**     &nbsp; Deadline for first versions of solvers
 - **June 10**    &nbsp; Deadline for final versions of solvers
 - **July 12-13** &nbsp; SMT Workshop (presentation of results)

### Organizers

- [Matthias Heizmann](https://swt.informatik.uni-freiburg.de/staff/heizmann) - Universit&auml;t Freiburg, Germany
- [Aina Niemetz](https://cs.stanford.edu/people/niemetz) - Stanford University, USA
- [Giles Reger](http://www.cs.man.ac.uk/~regerg/) - University of Manchester, UK
- [Tjark Weber](http://user.it.uu.se/~tjawe125/) (chair) - Uppsala University, Sweden

SMT-COMP 2018 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.
