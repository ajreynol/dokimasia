; (= (bvadd x #x01) (bvadd x #x02)): difference normalizes to a nonzero constant.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(declare-const y (_ BitVec 8))
(assert (= (bvadd x y #x01) (bvadd y #x02 x)))
(check-sat)
