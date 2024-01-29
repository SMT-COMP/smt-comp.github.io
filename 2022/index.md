---
layout: default
title: SMT-COMP 2022
---

## SMT-COMP 2022

The *17th International Satisfiability Modulo Theories Competition (SMT-COMP
2022)* is part of the
[SMT Workshop 2022](https://smt-workshop.cs.uiowa.edu/2022),
affiliated with [IJCAR 2022](https://easychair.org/smart-program/IJCAR2022/).
The SMT Workshop will include a block of time to
present the competitors and results of the competition.

### News
{% assign newsList = site.news_2022 | reverse %}
{% for news in newsList %}
- {{ news.newsdate | date_to_string }} [{{ news.title }}]({{ news.url }})
{% endfor %}

### Key dates
 - **Mar 15** &nbsp; Deadline for new benchmark contributions
 - **May 28** &nbsp; Final versions of competition tools
 - **June 18**    &nbsp; Deadline for first versions of solvers (for all tracks)
 - **July 2**   &nbsp; Deadline for final versions of solvers, including system descriptions
 - **August 12** &nbsp; SMT Workshop (presentation of results)

### Organizers
- [Haniel Barbosa](http://homepages.dcc.ufmg.br/~hbarbosa/) (chair) - Universidade Federal de Minas Gerais, Brazil
- [François Bobot](https://github.com/bobot) - CEA List, France
- [Jochen Hoenicke](https://jochen-hoenicke.de/) - Albert-Ludwigs-Universität Freiburg, Germany

SMT-COMP 2022 is organized under the direction of the SMT Steering
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
