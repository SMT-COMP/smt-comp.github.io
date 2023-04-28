## Experimental model validation track

The format for the model output of some theories is not yet defined by the
SMTLIB. The following document describe proposition of such definitions. The format will be used by the
model validator of the SMTLIB for the experimental model validation track of the
SMTCOMP 2023.

## Partial functions

Some theory functions are only partially defined, e.g., division by
zero.  The SMT semantics states that a benchmark is sat if there is an
extension of these partial functions to a total function, i.e., the
value of the function can be chosen by the solver.  This begs the
questions how a solver should describe the model it chose.

We propose that solvers should give the values similar as for
uninterpreted functions using `define-fun`.  The given function definition
must coincide on the defined inputs with the values given by the
theory.  To achieve this, the function definition may call the original theory
function using the same name as the function that is defined.

In the model validation track require that solvers give the values for
an undefined input, if it affects the satisfiability of the benchmark.
A solver should give a concrete value for all undefined inputs.  A
simple way to achieve this is with an `ite` expression that checks if
the input leads to undefinedness and provides a concrete expression in
that case and calls the original theory function in the other case.
Here are some examples, given that the following definition of an algebraic datatype is present in the input problem:

```smt2
(declare-datatypes ((list 1)) ((par (alpha) (
  (nil)
  (cons (car alpha) (cdr (list alpha)))
))))
```

The model with valid definitions of theory functions:

```smt2
(define-fun div ((a Int) (b Int)) Int
   (ite (= b 0) (ite (= a 0) 5 0) (div a b)))
(define-fun car ((a (List Int))) (List Int)
   (match a
      ((cons hd tl) hd)
      (nil  42)))
(define-fun cdr ((a (List Int))) Int
   (ite ((_ is cons) a) (cdr a) a))
```

It is not a recursive function, more like shadowing. The model checker is lenient, it will complain only if it needs a value in the uninterpreted domain of a partial function. For example for `assert (= 0.5 (div 1.0 x))`, the definition of `div` can be omitted if the value of `x` is `2.0` is the model, but it can't be omitted if it is `0.0`.

## Algebraic numbers

Representation of (algebraic
numbers)[https://en.wikipedia.org/wiki/Algebraic_number] are needed for
representing models of `QF_NRA`. Their representation usually consists in two
parts, one polynomial and a way to specify which root of the polynomial is the
represented algebraic numbers.

For the polynomial there are two main choices:

* Any polynomial with rational coefficients
* The unique reduced minimal polynomial with integer coefficients

For specifying the roots:

* An enclosure where that contains a unique root of the polynomial
* A rational which is the closest to a unique root
* The number of the root in a specific ordering.

The ordering can be smallest to greatest however it doesn't extend to complex
values. Moreover, multiplicities must be taken into account. However, it offers
the possibility to have a unique representation for an algebraic number.

We identified two opposing objectives:
- Uniqueness of the representation
- Human readability

The first objective allows knowing syntactically which values are equal in a model. The human readability means that a human can get an understanding of the value of the number just by reading the value. We propose two ways to write values of algebraic numbers that corresponding to one objective each `root-of-with-ordering` and `root-of-with-interval`. In both case the polynomial with integer coefficient is represented by the list of coefficient from the smallest degree to the greatest $x^2-2$ is `((- 2) 0 1)`.


* `(root-of-with-ordering (p_0 p_1 ... p_n) i)` represents the `i` nth root ordered with multiplicity from the smallest to greatest of the polynomial `(p_0 p_1 ... p_n)`. `i` is a numeral (positive integer). The polynomial must be the unique reduced minimal polynomial.
* `(root-of-with-interval (p_0 p_1 ... p_n) (min max))` represents the unique root between `min` and `max` of the polynomial `(p_0 p_1 ... p_n)`. `i` is an integer. `min` and `max` are decimal, with negative number written as `(- 1.0)`.

The constraint on the uniqueness of the polynomial in `root-of-with-ordering` could perhaps be removed.

## Array values

It currently exists two propositions of representation of array values:

1. By building a value using `const`, and `store`:
   ```smt2
   (define-fun b () (Array Int Real)
      (store (store ((as const (Array Int Real)) 2.0) 0 1.0) 1 3.0))
   ```
2. By using an additional uninterpreted function:
   ```smt2
   (define-fun b () (Array Int Real)
     (_ as-array k!1))
   (define-fun k!1 ((x!0 Int)) Real
     (ite (= x!0 1) 3.0
     (ite (= x!0 0) 1.0
      2.0)))
   ```

The first propositions gives directly a constant term (that use the symbol `const`
that is not defined by the SMTLIB format) when the second proposition requires
to define an additional function.

 The second proposition is more general
and can handle models for problems with quantifications. Since Smtlib3 should
introduce anonymous functions we though proposing to backport the feature just for the
definition of model of arrays with the addition of the function `as-array` to convert from a function `(-> A B)` to an array `(Array A B)`. We would have

```smt2
(define-fun b () (Array Int Real)
  (as-array (lambda ((x!0 Int))
   (ite (= x!0 1) 3.0
   (ite (= x!0 0) 1.0
    2.0)))))
```

However using generic functions for defining arrays makes the valuation of equalities between arrays complicated. So in order to keep the ability to compute the interpretation of quantifier free formulas, we propose to require the first propositions for array models in quantifier free logic. That do not mandate the `const` function to be builtin in the theory, it could appear only in the model even if disallow to put back the models as assertions.


To sum up, in quantifier free logic, model for arrays should be represented using `store` and `const` function.
