; MultPow2 (after MultSimplify): x*2*2 -> concat(extract 1 0 x, 00)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvmul x #x2 #x2) (concat ((_ extract 1 0) x) #b00))))
(check-sat)
