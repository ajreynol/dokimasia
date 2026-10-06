; differential: exhaustive bvsrem table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (not (= (bvsrem #b0 #b0) #b0))
  (not (= (bvsrem #b0 #b1) #b0))
  (not (= (bvsrem #b1 #b0) #b1))
  (not (= (bvsrem #b1 #b1) #b0))))
(check-sat)
