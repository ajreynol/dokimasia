; AndSimplify: two constants plus x and (bvnot x) collapse to zero.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvand x #b1110 y (bvnot x) #b0111) #b0000)))
(check-sat)
