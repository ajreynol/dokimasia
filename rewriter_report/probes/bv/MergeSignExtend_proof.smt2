; Proof probe: sext(i, sext(j,x)) -> sext(i+j,x); sext(i, zext(j,x)) -> zext(i+j,x) (MergeSignExtend / bv-merge-sign-extend-1/2).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (or (not (= ((_ sign_extend 2) ((_ sign_extend 1) x)) ((_ sign_extend 3) x)))
            (not (= ((_ sign_extend 2) ((_ zero_extend 1) x)) ((_ zero_extend 3) x)))))
(check-sat)
