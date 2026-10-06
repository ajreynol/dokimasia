; ExtractMultLeadingBit: leading const 1 => bit 64 can be 1
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 32))
(declare-const y (_ BitVec 32))
(assert (= ((_ extract 64 64) (bvmul (concat #x0000000001 x) (concat (_ bv0 40) y))) #b1))
(check-sat)
