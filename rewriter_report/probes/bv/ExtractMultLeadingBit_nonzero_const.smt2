; ExtractMultLeadingBit: leading const 1 (39 leading zeros) => k=65, extract [71:65] -> 0
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 32))
(declare-const y (_ BitVec 32))
(assert (not (= ((_ extract 71 65) (bvmul (concat #x0000000001 x) (concat (_ bv0 40) y))) #b0000000)))
(check-sat)
