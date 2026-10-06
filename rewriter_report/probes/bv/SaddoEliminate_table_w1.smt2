; differential: exhaustive bvsaddo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvsaddo #b0 #b0)
  (bvsaddo #b0 #b1)
  (bvsaddo #b1 #b0)
  (not (bvsaddo #b1 #b1))))
(check-sat)
