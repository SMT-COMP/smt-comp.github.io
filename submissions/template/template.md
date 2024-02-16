## Submissions directory

The creation of new submission is done through the creation of a new json file
in this directory and the submission of a Pull Request.

It could be done directly from the web-interface and starting with a template:
[create a new submission](https://github.com/SMT-COMP/smt-comp.github.io/new/new_submission/submissions?value=$value)

- The filename should start with the name of your solver and end with `.json`
- The continuous integration will check the format

### Fields

- `name`: The solver name should respect the guidelines in the given in the
  rules of the SMT-competition (derived solver, wrapper solver, ...)
- `authors`: (utf8 can be used? It should be checked. tuple with latin1?)
- `url`: The url should be valid at the time of submission and during all the
  competition. Do we require zenodo for final version?
