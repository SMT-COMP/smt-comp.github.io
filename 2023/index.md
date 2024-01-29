---
layout: default
title: SMT-COMP 2023
---

## SMT-COMP 2023

The *18th International Satisfiability Modulo Theories Competition (SMT-COMP
2023)* is part of the
[SMT Workshop 2023](https://smt-workshop.cs.uiowa.edu/2023),
affiliated with [CADE-29](https://easyconferences.eu/cade2023/).
The SMT Workshop will include a block of time to
present the competitors and results of the competition.

### News
{% assign newsList = site.news_2023 | reverse %}
{% for news in newsList %}
- {{ news.newsdate | date_to_string }} [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key dates
 - **Mar 31** &nbsp; Deadline for new benchmark contributions
 - **April 29** &nbsp; Final versions of competition tools
 - **May 13**    &nbsp; Deadline for first versions of solvers (for all tracks)
 - **May 27**   &nbsp; Deadline for final versions of solvers, including system descriptions
 - **July 5&ndash;6** &nbsp; SMT Workshop (presentation of results)

### Organizers
- [François Bobot](https://github.com/bobot) (chair) - CEA List, France
- [Martin Bromberger](https://www.mpi-inf.mpg.de/departments/automation-of-logic/people/martin-bromberger) - MPI für Informatik, Germany
- [Jochen Hoenicke](https://jochen-hoenicke.de/) - Certora, Israel

SMT-COMP 2023 is organized under the direction of the SMT Steering
Committee.
<br/>
The competition is run on [StarExec](https://www.starexec.org),
a service that is hosted at the University of Iowa.  The parallel and
cloud tracks are run on AWS.

### Acknowledgment
- [Aaron Stump](http://homepage.divms.uiowa.edu/~astump/) (StarExec)
- [Clark Barrett](http://theory.stanford.edu/~barrett/), [Pascal
  Fontaine](https://members.loria.fr/PFontaine/), [Aina
Niemetz](https://cs.stanford.edu/~niemetz/), [Mathias
Preiner](https://cs.stanford.edu/~preiner/), and [Hans-Jörg
Schurr](https://team.inria.fr/veridis/schurr/)
([smt-lib](http://smtlib.cs.uiowa.edu/index.shtml) maintenance)
- Jonathan Eidelman and Mike Whalen (Cloud and Parallel Tracks AWS Support)
