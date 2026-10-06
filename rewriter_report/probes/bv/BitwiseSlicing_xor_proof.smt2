; BitwiseSlicing on bvxor, alternating constant #b0101
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvxor x #b0101) (concat ((_ extract 3 3) x) (bvnot ((_ extract 2 2) x)) ((_ extract 1 1) x) (bvnot ((_ extract 0 0) x))))))
(check-sat)
