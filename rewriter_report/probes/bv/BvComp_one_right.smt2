; BvComp: (bvcomp c #b1) -> c
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(assert (not (= (bvcomp c #b1) c)))
(check-sat)
