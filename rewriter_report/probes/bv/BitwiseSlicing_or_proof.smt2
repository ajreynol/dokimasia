; BitwiseSlicing on bvor, constant with leading/trailing runs
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvor x #b1001) (concat #b1 ((_ extract 2 1) x) #b1))))
(check-sat)
