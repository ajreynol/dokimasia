; UdivPow2: not applied to -4 (#xC); x udiv #xC = #x1 sat (x>=12)
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (= (bvudiv x #xC) #x1))
(check-sat)
