; ExtractExtract differential: off-by-one alternative x[5:4] must be distinguishable (sat).
; EXPECT: sat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(assert (not (= ((_ extract 1 0) ((_ extract 4 2) ((_ extract 6 1) x))) ((_ extract 5 4) x))))
(check-sat)
