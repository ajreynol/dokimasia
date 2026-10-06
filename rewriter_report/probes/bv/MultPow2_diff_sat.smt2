; MultPow2: differential, x*#x8 = #x8 sat (x odd)
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (= (bvmul x #x8) #x8))
(check-sat)
