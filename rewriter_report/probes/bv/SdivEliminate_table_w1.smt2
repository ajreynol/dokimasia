; differential: exhaustive bvsdiv table at width 1 vs SMT-LIB semantics
; EXPECT: unsat
(set-logic QF_BV)
(assert (or
  (not (= (bvsdiv #b0 #b0) #b1))
  (not (= (bvsdiv #b0 #b1) #b0))
  (not (= (bvsdiv #b1 #b0) #b1))
  (not (= (bvsdiv #b1 #b1) #b1))))
(check-sat)
