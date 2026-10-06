; differential: exhaustive bvnego table at width 1
; EXPECT: unsat
(set-logic QF_BV)
(assert (or (bvnego #b0) (not (bvnego #b1))))
(check-sat)
