; MultPow2: x*4 -> concat(extract 1 0 x, 00)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvmul x #x4) (concat ((_ extract 1 0) x) #b00))))
(check-sat)
