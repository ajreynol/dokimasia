; differential: exhaustive bvuaddo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvuaddo #b0 #b0)
  (bvuaddo #b0 #b1)
  (bvuaddo #b1 #b0)
  (not (bvuaddo #b1 #b1))))
(check-sat)
