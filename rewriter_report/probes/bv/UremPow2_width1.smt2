; Differential edge: width-1 urem by #b1 (pow2 with power 0) must be 0; urem by #b0 is identity.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const y (_ BitVec 1))
(assert (or (not (= (bvurem y #b1) #b0)) (not (= (bvurem y #b0) y))))
(check-sat)
