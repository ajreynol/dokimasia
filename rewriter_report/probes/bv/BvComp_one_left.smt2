; BvComp: (bvcomp #b1 c) -> c
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(assert (not (= (bvcomp #b1 c) c)))
(check-sat)
