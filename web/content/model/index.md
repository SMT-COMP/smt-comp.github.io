+++
title = 'Model Validation Track'
date = 2023-12-11T21:09:02+01:00
draft = false
aliases = ['/model.html']
+++

## Experimental model validation track

The format for the model output of some theories is not yet defined by the
SMT-LIB. The following document describes our proposal of such definitions.
This format will be used by the model validator for the experimental model
validation track of the SMTCOMP 2025.

## Partial functions

Some theory functions are only partially defined, e.g., division by
zero. The SMT semantics states that a benchmark is sat if there is an
extension of these partial functions to a total function, i.e., the
value of the function can be chosen by the solver. This begs the
questions how a solver should describe the model it chose.

We propose that solvers should give the values similar as for
uninterpreted functions using `refine-fun`. It should be soon the official choice. The formerly proposed command `define-fun` is kept for compatibility at least in 2025. The given function definition
must coincide on the defined inputs with the values given by the
theory. To achieve this, the function definition may call the original theory
function using the same name as the function that is defined.

In the model validation track, solvers MUST give the values for
an undefined input, if it affects the satisfiability of the benchmark.
A solver SHOULD give a concrete value for all undefined inputs. A
simple way to achieve this is with an `ite` expression that checks if
the input leads to undefinedness and provides a concrete expression in
that case and calls the original theory function in the other case.

As an example, consider the theories of non-linear arithmetic and data
types and the following definition of an algebraic data type for lists
in the input problem:

```smt2
(declare-datatypes ((list 1)) ((par (alpha) (
  (nil)
  (cons (car alpha) (cdr (list alpha)))
))))
```

The partially defined theory functions may be defined using the following
definitions in the model:

```smt2
(refine-fun div ((a Int) (b Int)) Int
   (ite (= b 0) (ite (= a 0) 5 0) (div a b)))
(refine-fun car ((a (List Int))) (List Int)
   (match a
      ((cons hd tl) hd)
      (nil  42)))
(refine-fun cdr ((a (List Int))) Int
   (ite ((_ is cons) a) (cdr a) a))
```

The functions `div`/`car`/`cdr` should not be considered to be recursive function.
Instead the definition shadows the (partially defined) theory function and
the definition calls the original theory function in the function body.
The model checker conforms to the MUST/SHOULD requirements above. It will complain only if it needs a value in the uninterpreted domain of a partial function. For example for `(assert (= 0.5 (div 1.0 x)))`,
the definition of `div` can be omitted if the solver chose `2.0` as the
value for `x` in the model, but it can't be omitted if it chose `0.0`.

## Algebraic numbers

Representations of (algebraic
numbers)[https://en.wikipedia.org/wiki/Algebraic_number] are needed for
representing models of `QF_NRA`. Their representation usually consists of two
parts, one polynomial and a way to specify which root of the polynomial is the
represented algebraic numbers.

For the polynomial there are two main choices:

- Any polynomial with rational coefficients
- The unique reduced minimal polynomial with integer coefficients

For specifying the roots:

- An enclosure where that contains a unique root of the polynomial
- A rational which is the closest to a unique root
- The number of the root in a specific ordering.

The ordering can be smallest to greatest however it doesn't extend to complex
values. Moreover, multiplicities must be taken into account. However, it offers
the possibility to have a unique representation for an algebraic number.

We identified two opposing objectives:

- Uniqueness of the representation
- Human readability

The first objective allows checking syntactically which values are equal in a model. The human readability means that a human can get an understanding of the value of the number just by reading the value. We propose two ways to write values of algebraic numbers that corresponding to one objective each `root-of-with-ordering` and `root-of-with-interval`. In both case the polynomial with integer coefficient is represented by the list of coefficients in ascending order, i.e., from the coefficient of the constant term to the leading coefficient. For example, $x^2 - 2$ is represented as `((- 2) 0 1)`. For uniqueness, the coefficients should be coprime integers and the leading coefficient should be positive.

- `(root-of-with-ordering (coeffs p_0 p_1 ... p_n) i)` represents the `i`-th root ordered with multiplicity from the smallest to greatest of the polynomial `(p_0 p_1 ... p_n)`. Here, `i` is a numeral (non-negative integer) and is `0` for the smallest root of the polynomial. The polynomial must be the unique reduced minimal polynomial, in particular, it must only have simple roots.
- `(root-of-with-interval (coeffs p_0 p_1 ... p_n) min max)` represents the unique root between `min` and `max` of the polynomial `(p_0 p_1 ... p_n)`. `i` is an integer. `min` and `max` are rational model values, e.g. `(0.0 (/ 1.0 2.0))` for the interval `[0, .5]` or `((- 1.0) (/ (- 1.0) 2.0))` for the interval [-1, -.5].

The constraint on the uniqueness of the polynomial in `root-of-with-ordering` could perhaps be removed.

(EDIT:

- a previous version did not require `coeffs`, but it is necessary in order to be an SMTLIB term.
- a previous version used `(min max)` instead of `min max`, but it is necessary in order to be an SMTLIB term.
- Because of a typo, the model validator will accept this year both `root-of-with-ordering` and `root-of-with-order` and both `root-of-with-interval` and `root-of-with-enclosure`.
  )

## Array values

Models for arrays should be represented using the `store` and `const` functions:

```smt2
(define-fun b () (Array Int Real)
   (store (store ((as const (Array Int Real)) 2.0) 0 1.0) 1 3.0))
```

There were two alternative suggestions but we rejected them for various reasons at least for this years conference. We will still outline them here to explain our reasoning. The alternatives are:

1. By using an additional uninterpreted function:
   ```smt2
   (define-fun b () (Array Int Real)
     (_ as-array k!1))
   (define-fun k!1 ((x!0 Int)) Real
     (ite (= x!0 1) 3.0
     (ite (= x!0 0) 1.0
      2.0)))
   ```
2. By building an array from model values and `store`:
   ```smt2
   (define-fun b () (Array Int Real)
      (store (store (as @array0 (Array Int Real)) 0 1.0) 1 3.0))
   ```
   Note that here the value is not uniquely defined. For our purpose,
   the array values must explicitly use store to define values for all
   indices that are read by any `select` in the benchmark.
   Different model values for arrays are considered
   to be not equal like in the UF logic.

The const/store representation gives directly a constant term (that use the symbol `const` that is not defined by the SMTLIB format) when the first alternative requires to define an additional function.

The first alternative is more general
and can handle models for problems with quantifiers. Since SMT-LIB 3 should
introduce anonymous functions we could backport the feature for the
definition of model of arrays with the addition of the function `as-array` to convert from a function `(-> A B)` to an array `(Array A B)`. We would have

```smt2
(define-fun b () (Array Int Real)
  (as-array (lambda ((x!0 Int))
   (ite (= x!0 1) 3.0
   (ite (= x!0 0) 1.0
    2.0)))))
```

However, using generic functions for defining arrays makes it harder for
the model validator to evaluate array equality (extensionality).
So in order to keep the validator simple for quantifier free formulas,
we require the first way of defining array models in quantifier free logic.
The `const` function is only visible in the array models and not part of the
theory. A benchmark problem must not contain the `const` function in an
assertion.

To sum up, in quantifier free logic, models for arrays should be represented using `store` and `const` function.
