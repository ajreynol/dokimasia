; ExtractMultLeadingBit: low = k-1 = 63 must not fold (bit 63 can be 1)
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 32))
(declare-const y (_ BitVec 32))
(assert (= ((_ extract 63 63) (bvmul (concat (_ bv0 40) x) (concat (_ bv0 40) y))) #b1))
(check-sat)
