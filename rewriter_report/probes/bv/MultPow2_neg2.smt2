; MultPow2: x*-2 (#xE) -> concat(extract 2 0 (bvneg x), 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvmul x #xE) (concat ((_ extract 2 0) (bvneg x)) #b0))))
(check-sat)
