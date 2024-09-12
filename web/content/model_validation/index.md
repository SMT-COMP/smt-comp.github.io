+++
title = 'Discussion on Model Validation'
date = 2024-08-09T13:05:31+02:00
draft = false
+++

Globally the solvers that participated in the model validation track produced models that have been successfully checked by Dolmen.

However, mainly for experimental tracks, some models are not checked for different reasons. All the models not verified will be available in the artifacts of the competition. But let's see some examples of them.

The examples are the scrambled benchmarks, for `dolmen` the version of the competition is used. The following prefix and suffix are remove in the example for conciseness.

```
(set-option :print-success false)
(set-option :produce-models true)


(get-model)
(exit)
```

### Unsatisfiable Model

<!-- Yices2.0/scrambled327966.smt2 -->

Scrambled SMTLIB2 file:

```
(set-logic QF_NRA)
(declare-fun x2 () Real)
(declare-fun x1 () Real)
(assert (= (* x2 x2) 2))
(assert (< x1 x2))
(assert (= 1 (* x1 2)))
(check-sat)
```

Model returned by a solver:

```
sat
(model
  (define-fun x2 () Real 1.414214)
  (define-fun x1 () Real (/ 1 2)))
```

The model is false, but in such case the error is often just in the printer used for constant values. For example in another example the same solver prints `-1.414214` which should be written as `(- 1.414214)`.

### Parsing error for algebraic numbers

<!-- cvc5.0/scrambled307203.smt2 -->

Indeed, printing non-rational algebraic number is hard. Some solvers have not yet adopted the proposed way to [print such numbers](../model/).

```
(set-logic QF_NRA)
(declare-fun x1 () Real)
(assert (= 2 (* x1 x1)))
(check-sat)
```

```
sat
(
(define-fun x1 () Real (_ real_algebraic_number <1*x^2 + (-2), (5/4, 3/2)>))
)
```

It would be hard to make Dolmen support this syntax, because it does not follow the SMT2.6 grammar for terms.

With the proposed syntax it would be:

```
sat
(
(define-fun x1 () Real `(root-of-with-interval (coeffs (- 2) 0 1) (/ 5 4) (/ 3 2))`
))
```

### Division by zero

<!-- cvc5.0/scrambled38173.smt2 -->

```
(set-logic QF_UFNIA)
(declare-fun x3 (Int Int Int) Int)
(declare-fun x32 (Int Int Int) Int)
(declare-fun x25 (Int) Int)
(declare-fun x27 (Int Int Int) Int)
(define-fun x11 ((x10 Int) (x8 Int) (x16 Int)) Int (mod (div x16 (x25 x8)) 2))
(define-fun x38 ((x10 Int) (x16 Int)) Int (mod x16 (x25 (- x10 1))))
(define-fun x13 ((x10 Int)) Int (- (x25 x10) 1))
(define-fun x36 ((x10 Int)) Int 0)
(define-fun x34 ((x10 Int) (x30 Int)) Bool (and (>= (x13 x10) x30) (>= x30 0)))
(define-fun x24 ((x10 Int) (x16 Int) (x22 Int)) Int (ite (= x22 0) (- (x25 x10) 1) (div x16 x22)))
(define-fun x17 ((x10 Int) (x16 Int) (x22 Int)) Int (ite (= 0 x22) x16 (mod x16 x22)))
(define-fun x19 ((x10 Int) (x16 Int)) Int (x17 x10 (- (x25 x10) x16) (x25 x10)))
(define-fun x4 ((x10 Int) (x16 Int)) Int (- (x13 x10) x16))
(define-fun x23 ((x10 Int)) Int (x25 (- x10 1)))
(define-fun x6 ((x10 Int)) Int (x4 x10 (x23 x10)))
(define-fun x21 ((x10 Int) (x16 Int) (x22 Int)) Int (x17 x10 (* x16 (x25 x22)) (x25 x10)))
(define-fun x29 ((x10 Int) (x16 Int) (x22 Int)) Int (x17 x10 (x24 x10 x16 (x25 x22)) (x25 x10)))
(define-fun x28 ((x10 Int) (x16 Int) (x22 Int)) Int (ite (= 0 (x11 x10 (- x10 1) x16)) (x29 x10 x16 x22) (x4 x10 (x29 x10 (x4 x10 x16) x22))))
(define-fun x9 ((x10 Int) (x7 Int) (x16 Int) (x22 Int)) Int (+ (* x16 (x25 x7)) x22))
(define-fun x18 ((x10 Int) (x16 Int) (x22 Int)) Int (x17 x10 (+ x16 x22) (x25 x10)))
(define-fun x20 ((x10 Int) (x16 Int) (x22 Int)) Int (x17 x10 (* x22 x16) (x25 x10)))
(define-fun x2 ((x10 Int) (x16 Int) (x22 Int)) Int (x18 x10 x16 (x19 x10 x22)))
(define-fun x40 ((x10 Int) (x30 Int)) Int (- (* (x38 x10 x30) 2) x30))
(define-fun x39 ((x10 Int) (x16 Int) (x22 Int)) Bool (< (x40 x10 x16) (x40 x10 x22)))
(define-fun x5 ((x10 Int) (x16 Int) (x22 Int)) Bool (> (x40 x10 x16) (x40 x10 x22)))
(define-fun x15 ((x10 Int) (x16 Int) (x22 Int)) Bool (<= (x40 x10 x16) (x40 x10 x22)))
(define-fun x26 ((x10 Int) (x16 Int) (x22 Int)) Bool (>= (x40 x10 x16) (x40 x10 x22)))
(define-fun x37 () Bool (and (= 2 (x25 1)) (= 8 (x25 3)) (= (x25 0) 1) (= (x25 2) 4)))
(define-fun x31 () Bool x37)
(define-fun x12 ((x10 Int)) Bool true)
(define-fun x35 ((x10 Int)) Bool true)
(define-fun x33 ((x10 Int)) Bool true)
(declare-fun x10 () Int)
(assert x31)
(assert (< 0 x10))
(assert (x33 x10))
(assert (x35 x10))
(assert (x12 x10))
(declare-fun x14 () Int)
(assert (x34 x10 x14))
(declare-fun x1 () Int)
(assert (x34 x10 x1))
(assert true)
(assert (and (< x14 x10) (= (x2 x10 x10 1) x14) (not (= (x28 x10 x1 x14) (x2 x10 0 (x29 x10 x1 x14))))))
(check-sat)
```

```
sat
(
(define-fun x3 ((BOUND_VARIABLE_9367 Int) (BOUND_VARIABLE_9368 Int) (BOUND_VARIABLE_9369 Int)) Int 0)
(define-fun x32 ((BOUND_VARIABLE_9372 Int) (BOUND_VARIABLE_9373 Int) (BOUND_VARIABLE_9374 Int)) Int 0)
(define-fun x25 ((_arg_1 Int)) Int (ite (= _arg_1 2) 4 (ite (= _arg_1 0) 1 (ite (= _arg_1 1) 2 (ite (= _arg_1 3) 8 (ite (= _arg_1 5) 0 5))))))
(define-fun x27 ((BOUND_VARIABLE_9377 Int) (BOUND_VARIABLE_9378 Int) (BOUND_VARIABLE_9379 Int)) Int 0)
(define-fun x10 () Int 6)
(define-fun x14 () Int 0)
(define-fun x1 () Int 2)
)
```

The output of Dolmen:

```
47 | (assert (and (< x14 x10) (= (x2 x10 x10 1) x14) (not (= (x28 x10 x1 x14) (x2 x10 0 (x29 x10 x1 x14))))))
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Error The symbol `div` is only partially interpreted/defined,
      and the following application does not have an intepretation: (div 2 0)
```

The division is in fact guarded by an `ite` in this example: `(ite (= x22 0) (- (x25 x10) 1) (div x16 x22))`. Dolmen could special-case the interpretation of ite in order to be lazy, but it could not do it for implications.

### Datatype projections

<!-- cvc5.0/scrambled2263.smt2 -->

In the following example `x8` is the projection for the first argument of the constructor `x12` of the datatype `x6`. It is not defined when applied on the constructor `x15`.

```
(set-logic QF_DT)
(declare-datatypes ((x7 0) (x6 0) (x4 0)) (((x14) (x1 (x13 x7))) ((x15) (x12 (x8 x4) (x17 x6))) ((x16 (x10 x7)) (x11 (x9 x6)))))
(declare-fun x5 () x7)
(declare-fun x2 () x6)
(declare-fun x3 () x4)
(assert (and (= x5 (x13 (x1 x14))) (= x3 (x8 (x9 (x11 x2))))))
(check-sat)
```

```
sat
(
(define-fun x5 () x7 x14)
(define-fun x2 () x6 x15)
(define-fun x3 () x4 (x8 x2))
)
```

```
File "tmp/pb_models/cvc5.0/scrambled2263.rsmt2", line 5, character 0-29:
5 | (define-fun x3 () x4 (x8 x2))
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Error The symbol `x8` is only partially interpreted/defined,
      and the following application does not have an intepretation:
      (x8 {x15})
```

This example is clearly trivial, the assertions just defines `x5`, `x3` which
appears once. So any values are acceptable for `x2`. We can hypothesize the
solver chose the first value in its type. Still since the solver has not provided a value for the application of `x8` on `x15` the assertions can't be interpreted using the model.

### Other partially defined functions

- `fp.to_sbv`

<!-- cvc5.2/scrambled343818.rsmt2 -->

```
(set-logic QF_BVFPLRA)
(declare-fun x3 () (_ FloatingPoint 11 53))
(declare-fun x10 () Bool)
(declare-fun x6 () RoundingMode)
(declare-fun x4 () (_ FloatingPoint 11 53))
(declare-fun x2 () (_ FloatingPoint 11 53))
(declare-fun x5 () (_ FloatingPoint 11 53))
(declare-fun x11 () (_ FloatingPoint 11 53))
(declare-fun x8 () (_ FloatingPoint 11 53))
(declare-fun x9 () (_ FloatingPoint 11 53))
(declare-fun x1 () (_ BitVec 32))
(declare-fun x13 () (_ FloatingPoint 11 53))
(declare-fun x12 () (_ FloatingPoint 11 53))
(assert (and (= ((_ to_fp 11 53) x6 x1) x2) (= ((_ fp.to_sbv 32) roundTowardZero (fp.add x6 x11 (fp.mul x6 x9 x8))) x1) (= x13 x9) (let ((x7 (bvslt x1 (_ bv32 32)))) (or (and (not x10) (not x7)) (and x7 x10))) (= (fp.sub x6 x9 (fp.mul x6 x2 x12)) x5) (= (fp.mul x6 x3 x2) x4)))
(check-sat)
```

```
sat
(
(define-fun x3 () (_ FloatingPoint 11 53) (fp #b0 #b00000000000 #b0000000000000000000000000000000000000000000000000000))
(define-fun x10 () Bool false)
(define-fun x6 () RoundingMode roundTowardNegative)
(define-fun x4 () (_ FloatingPoint 11 53) (fp.mul roundTowardNegative (fp #b0 #b00000000000 #b0000000000000000000000000000000000000000000000000000) ((_ to_fp 11 53) roundTowardNegative ((_ fp.to_sbv 32) roundTowardZero (fp #b0 #b11111111111 #b1000000000000000000000000000000000000000000000000000)))))
(define-fun x2 () (_ FloatingPoint 11 53) ((_ to_fp 11 53) roundTowardNegative ((_ fp.to_sbv 32) roundTowardZero (fp #b0 #b11111111111 #b1000000000000000000000000000000000000000000000000000))))
(define-fun x5 () (_ FloatingPoint 11 53) (fp.add roundTowardNegative (fp #b1 #b00000000000 #b0001000000000001111111111111111111111111111111111111) (fp.neg (fp.mul roundTowardNegative (fp #b0 #b00000000000 #b0000000000000000000000000000000000000000000000000000) ((_ to_fp 11 53) roundTowardNegative ((_ fp.to_sbv 32) roundTowardZero (fp #b0 #b11111111111 #b1000000000000000000000000000000000000000000000000000)))))))
(define-fun x11 () (_ FloatingPoint 11 53) (fp #b1 #b00000000000 #b0000000000000000000000000000000000000000000000000000))
(define-fun x8 () (_ FloatingPoint 11 53) (fp #b0 #b11111111111 #b1000000000000000000000000000000000000000000000000000))
(define-fun x9 () (_ FloatingPoint 11 53) (fp #b1 #b00000000000 #b0001000000000001111111111111111111111111111111111111))
(define-fun x1 () (_ BitVec 32) ((_ fp.to_sbv 32) roundTowardZero (fp #b0 #b11111111111 #b1000000000000000000000000000000000000000000000000000)))
(define-fun x13 () (_ FloatingPoint 11 53) (fp #b1 #b00000000000 #b0001000000000001111111111111111111111111111111111111))
(define-fun x12 () (_ FloatingPoint 11 53) (fp #b0 #b00000000000 #b0000000000000000000000000000000000000000000000000000))
)
```

```
Error The symbol `fp.to_sbv` is only partially interpreted/defined,
      and the following application does not have an intepretation:
      (fp.to_sbv Farith_Big.ZR NaN)
```

### Variable multiply defined

Some solver returns into the model variables that are defined in the problem.
Only declared variable should be returned.

### Model validator timeout

The Dolmen version used for the competition (with support for algebraic numbers)
timeouts on a small number of benchmarks. A quick test showed that the last version of dolmen (without support) doesn't timeout. So some additional investigation are needed.

### Parsing errors of the benchmarks

Some benchmarks in the SMTLIB are not respecting the definition of their specified logic according to Dolmen. So it refuses the benchmark. Dolmen has option to be less strict and to force the `ALL` logic, but it is not yet enough in some cases. One possibility would be to use the new feature of dolmen for selecting the minimal logic of a benchmark, or a future feature of simplifying benchmarks to fit some logic.