---
layout: default
title: SMT-COMP 2019
---

## SMT-COMP 2019

The *14th International Satisfiability Modulo Theories Competition
(SMT-COMP 2019)* is part of the [SMT Workshop 2019](http://smt2019.galois.com/),
affiliated with [SAT 2019](http://sat2019.tecnico.ulisboa.pt).
The SMT Workshop will include a block of time to present the competitors
and results of the competition.

### News
{% assign newsList = site.news_2019 | reverse %}
{% for news in newsList %}
- <span class="date">{{ news.newsdate | date_to_string }}</span> [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key Dates
 - **March 1**  &nbsp; Deadline for new benchmark contributions
 - **May 1**    &nbsp; Final versions of competition tools
 - **May 19**   &nbsp; Deadline for first versions of solvers (for all tracks)
 - **June 2**   &nbsp; Deadline for final versions of solvers, including system descriptions
 - **July 7-8** &nbsp; SMT Workshop (presentation of results)

### Organizers
- Liana Hadarean - Amazon, USA
- [Antti Hyvarinen](https://www.inf.usi.ch/postdoc/hyvarinen/) - Universita della Svizzera italiana, Switzerland
- [Aina Niemetz](https://cs.stanford.edu/people/niemetz) (co-chair) - Stanford University, USA
- [Giles Reger](http://www.cs.man.ac.uk/~regerg/) (co-chair) - University of Manchester, UK

SMT-COMP 2019 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.

### Acknowledgment
- [Mathias Preiner](https://cs.stanford.edu/people/preiner) (benchmark selection and scoring scripts)
- [Aaron Stump](http://homepage.divms.uiowa.edu/~astump/) (StarExec)
- [Andres N&ouml;tzli](https://cs.stanford.edu/people/noetzli/) (trace executor extension)
- Marco Gario and Andrea Micheli ([pySMT](https://github.com/pysmt/pysmt))
- [Martin Riener](https://www.logic.at/staff/riener/) (logistics for certificates and trophies)
