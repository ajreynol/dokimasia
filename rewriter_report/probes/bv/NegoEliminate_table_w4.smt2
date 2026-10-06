; differential: exhaustive bvnego table at width 4
; EXPECT: unsat
(set-logic QF_BV)
(assert (or (bvnego #b0000) (bvnego #b0001) (bvnego #b0010) (bvnego #b0011) (bvnego #b0100) (bvnego #b0101) (bvnego #b0110) (bvnego #b0111) (not (bvnego #b1000)) (bvnego #b1001) (bvnego #b1010) (bvnego #b1011) (bvnego #b1100) (bvnego #b1101) (bvnego #b1110) (bvnego #b1111)))
(check-sat)
