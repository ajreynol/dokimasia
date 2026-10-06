; MultPow2: x*8 (=min signed) -> concat(extract 0 0 x, 000)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvmul x #x8) (concat ((_ extract 0 0) x) #b000))))
(check-sat)
