; ExtractMultLeadingBit: 3-child concat (RARE pattern is binary concat)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 16))
(declare-const w (_ BitVec 16))
(declare-const y (_ BitVec 32))
(assert (not (= ((_ extract 71 64) (bvmul (concat (_ bv0 40) x w) (concat (_ bv0 40) y))) #x00)))
(check-sat)
