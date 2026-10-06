; BvComp: (bvcomp c #b0) -> (bvnot c)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const c (_ BitVec 1))
(assert (not (= (bvcomp c #b0) (bvnot c))))
(check-sat)
