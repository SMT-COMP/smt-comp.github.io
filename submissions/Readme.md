[//]: # "Generated from submissions/template/template.md"

## Submissions directory

The creation of new submission is done through the creation of a new json file
in this directory and the submission of a Pull Request.

It could be done directly from the web-interface and starting with a template:
[create a new submission](https://github.com/SMT-COMP/smt-comp.github.io/new/new_submission/submissions?value=%7B%0A%20%20%20%20%22name%22%3A%20%22%3Csolver%20name%3E%22%2C%0A%20%20%20%20%22authors%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%22First%20Smith%22%2C%0A%20%20%20%20%20%20%20%20%7B%20%22name%22%3A%20%22Second%20Baker%22%2C%20%22website%22%3A%20%22http%3A%2F%2Fbaker.com%2F%22%20%7D%0A%20%20%20%20%5D%2C%0A%20%20%20%20%22contacts%22%3A%20%5B%22contact%20name%20%3Ccontact%20email%3E%22%5D%2C%0A%20%20%20%20%22solver%22%3A%20%22http%3A%2F%2Fexample.com%2Fsolver.tar.gz%22%2C%0A%20%20%20%20%22solver_hash%22%3A%20%7B%20%22sha256%22%3A%20%22012345%22%20%7D%2C%0A%20%20%20%20%22website%22%3A%20%22http%3A%2F%2Fexample.com%2F%22%2C%0A%20%20%20%20%22system_description%22%3A%20%22http%3A%2F%2Fexample.com%2Fsystem.pdf%22%2C%0A%20%20%20%20%22command%22%3A%20%5B%22cmd%22%2C%20%22default_command_line%22%5D%2C%0A%20%20%20%20%22solver_type%22%3A%20%22Standalone%22%2C%0A%20%20%20%20%22participations%22%3A%20%5B%0A%20%20%20%20%20%20%20%20%7B%20%22tracks%22%3A%20%5B%22SingleQuery%22%5D%2C%20%22divisions%22%3A%20%5B%22Equality%22%5D%20%7D%2C%0A%20%20%20%20%20%20%20%20%7B%20%22tracks%22%3A%20%5B%22SingleQuery%22%5D%2C%20%22logics%22%3A%20%22QF_.%2ALRA.%2A%22%20%7D%2C%0A%20%20%20%20%20%20%20%20%7B%20%22tracks%22%3A%20%5B%22SingleQuery%22%5D%2C%20%22logics%22%3A%20%5B%22LIA%22%5D%20%7D%0A%20%20%20%20%5D%0A%7D%0A)

- The filename should start with the name of your solver and end with `.json`
- The continuous integration will check the format

### Fields

- `name`: The solver name should respect the guidelines in the given in the
  rules of the SMT-competition (derived solver, wrapper solver, ...)
- `authors`: (utf8 can be used? It should be checked. tuple with latin1?)
- `url`: The url should be valid at the time of submission and during all the
  competition. Do we require zenodo for final version?
