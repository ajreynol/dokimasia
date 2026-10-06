; differential: exhaustive bvsdivo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvsdivo #b0 #b0)
  (bvsdivo #b0 #b1)
  (bvsdivo #b1 #b0)
  (not (bvsdivo #b1 #b1))))
(check-sat)
