; ExtractConstant: extract of a constant at edge indices (top bit, low bit, middle).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (and (= ((_ extract 7 7) #b10110110) #b1) (= ((_ extract 0 0) #b10110110) #b0)
  (= ((_ extract 5 2) #b10110110) #b1101))))
(check-sat)
