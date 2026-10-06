; AndSimplify with two constants and a duplicate: (bvand x #b1100 y #b1010 x) = (bvand #b1000 x y); reaches the macro elaborator's const-grouping path.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvand x #b1100 y #b1010 x) (bvand #b1000 x y))))
(check-sat)
