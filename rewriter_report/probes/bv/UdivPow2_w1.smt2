; UdivPow2: width 1, b udiv #b1 -> b
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvudiv b #b1) b)))
(check-sat)
