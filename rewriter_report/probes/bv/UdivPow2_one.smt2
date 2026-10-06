; UdivPow2: x udiv 1 -> x (power 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvudiv x #x1) x)))
(check-sat)
