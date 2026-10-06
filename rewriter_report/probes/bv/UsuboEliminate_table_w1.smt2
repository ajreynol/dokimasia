; differential: exhaustive bvusubo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvusubo #b0 #b0)
  (not (bvusubo #b0 #b1))
  (bvusubo #b1 #b0)
  (bvusubo #b1 #b1)))
(check-sat)
