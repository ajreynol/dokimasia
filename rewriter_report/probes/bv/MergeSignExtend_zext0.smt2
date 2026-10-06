; Edge: sext(i, zext(0,x)) -> sext(i,x) (amount2==0 branch; RARE -2 requires j>0) and sext(0, sext(0,x)).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (or (not (= ((_ sign_extend 2) ((_ zero_extend 0) x)) ((_ sign_extend 2) x)))
            (not (= ((_ sign_extend 0) ((_ sign_extend 0) x)) x))))
(check-sat)
