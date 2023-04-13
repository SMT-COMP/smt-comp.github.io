## Experimental model validation track

The format for the model output of some theories is not yet defined by the
SMTLIB. The following document describe the format that will be used by the
model validator of the SMTLIB for the experimental model validation track of the
SMTCOMP.

## Partial functions

## Algebraic numbers

Representation of (algebraic
numbers)[https://en.wikipedia.org/wiki/Algebraic_number] are needed for
representing models of `QF_NRA`. Their representation consists ususally in two
parts, one polynomial and a way to specify which root of the polynomial is the
represented algebraic numbers.

For the polynomial there are two main choices:

* Any polynomial with rational coefficients
* The unique reduced minimal polynomial with integer coefficients

For specifying the roots:

* An enclosure where that contains a unique root of the polynomial
* A rational which is the closest to a unique root
* The number of the roots in a specific ordering

The ordering smallest to greatest. Nothing about the complex values.

TODO

## Array values

It currently exists two propositions of representation of array values:

1. By building a value using `const`, and  `store`:
`(define-fun b () (Array Int Real) (store ((as const (Array Int Real)) 0.0) 0 (/ (- 1) 2)))`

2. By using an additional uninterpreted function:
```
(define-fun b () (Array Int Real)
  (_ as-array k!1))
(define-fun k!1 ((x!0 Int)) Real
  (ite (= x!0 1) 3.0
  (ite (= x!0 0) 1.0
   2.0)))
```

The first propositions gives directly a constant term (that use the symbol const
that is not defined by the SMTlib format) when the second propositions requires
to define an additional function. However the second proposition is more general
and can handle models for problems with quantifications. Since Smtlib3 should
introduce anonymous functions we propose to backport the feature just for the
definition of model of arrays. Moreover we propose to add the function `as-array` to convert from a function `(-> A B)` to an array `(Array A B)`.

```
(define-fun b () (Array Int Real)
  (as-array (lambda ((x!0 Int))
   (ite (= x!0 1) 3.0
   (ite (= x!0 0) 1.0
    2.0)))))
```
