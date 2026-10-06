; differential: exhaustive bvssubo table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (bvssubo #b0 #b0)
  (not (bvssubo #b0 #b1))
  (bvssubo #b1 #b0)
  (bvssubo #b1 #b1)))
(check-sat)
