; MultPow2: x*-4 (#xC) -> concat(extract 1 0 (bvneg x), 00)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvmul x #xC) (concat ((_ extract 1 0) (bvneg x)) #b00))))
(check-sat)
