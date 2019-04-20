## SMT-COMP 2019

The 14th International Satisfiability Modulo Theories Competition
(SMT-COMP 2019) is part of the SMT Workshop 2019, affiliated with
[SAT 2019](http://sat2019.tecnico.ulisboa.pt).
The SMT Workshop will include a block of time to present the competitors
and results of the competition.

### News
{% for news in site.news  %}
- {{ news.newsdate | date_to_string }} [{{news.title}}]({{ news.url }})
{% endfor %}

### Key dates
**March 1**  &nbsp; Deadline for new benchmark contributions  
**May 1**    &nbsp; Final versions of competition tools  
**May 19**   &nbsp; Deadline for first versions of solvers (for all tracks)  
**June 2**   &nbsp; Deadline for final versions of solvers, including system descriptions  
**July 7-8** &nbsp; SMT Workshop (presentation of results)

### Organizers
- Liana Hadarean - Amazon, USA
- [Antti Hyvarinen](https://www.inf.usi.ch/postdoc/hyvarinen/) - Universita della Svizzera italiana, CH
- [Aina Niemetz](https://cs.stanford.edu/people/niemetz) (co-chair) - Stanford University, USA
- [Giles Reger](http://www.cs.man.ac.uk/~regerg/) (co-chair) - University of Manchester, UK
