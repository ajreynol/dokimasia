; BvComp: (bvcomp #b0 c) -> (bvnot c)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(assert (not (= (bvcomp #b0 c) (bvnot c))))
(check-sat)
