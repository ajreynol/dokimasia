; differential: exhaustive bvumulo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvumulo #b0 #b0)
  (bvumulo #b0 #b1)
  (bvumulo #b1 #b0)
  (bvumulo #b1 #b1)))
(check-sat)
