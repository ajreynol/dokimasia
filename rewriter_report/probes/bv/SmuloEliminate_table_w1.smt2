; differential: exhaustive bvsmulo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvsmulo #b0 #b0)
  (bvsmulo #b0 #b1)
  (bvsmulo #b1 #b0)
  (not (bvsmulo #b1 #b1))))
(check-sat)
