; AndSimplify where constants fold to all-ones and vanish: (bvand #b1111 x #b1111 y x) = (bvand x y).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvand #b1111 x #b1111 y x) (bvand x y))))
(check-sat)
