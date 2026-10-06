; UdivPow2: x udiv 4 -> concat(00, extract 3 2 x)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvudiv x #x4) (concat #b00 ((_ extract 3 2) x)))))
(check-sat)
