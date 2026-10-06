; differential: exhaustive bvsmod table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (not (= (bvsmod #b0 #b0) #b0))
  (not (= (bvsmod #b0 #b1) #b0))
  (not (= (bvsmod #b1 #b0) #b1))
  (not (= (bvsmod #b1 #b1) #b0))))
(check-sat)
