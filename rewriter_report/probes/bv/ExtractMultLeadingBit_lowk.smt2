; ExtractMultLeadingBit: boundary low = k = 64, extract [64:64] -> 0
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 32))
(declare-const y (_ BitVec 32))
(assert (not (= ((_ extract 64 64) (bvmul (concat (_ bv0 40) x) (concat (_ bv0 40) y))) #b0)))
(check-sat)
