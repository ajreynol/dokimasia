; differential: exhaustive bvnego table at width 2
; EXPECT: unsat
(set-logic QF_BV)
(assert (or (bvnego #b00) (bvnego #b01) (not (bvnego #b10)) (bvnego #b11)))
(check-sat)
