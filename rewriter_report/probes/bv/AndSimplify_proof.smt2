; AndSimplify: constant merge + duplicate removal (MACRO_BV_AND_SIMPLIFY)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(declare-const z (_ BitVec 4))
(assert (not (= (bvand x #b0111 y x #b1101) (bvand #b0101 x y))))
(check-sat)
