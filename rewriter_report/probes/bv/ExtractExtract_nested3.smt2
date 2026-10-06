; ExtractExtract: three nested extracts; low offsets accumulate (1+2) -> x[4:3].
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 8))
(assert (not (= ((_ extract 1 0) ((_ extract 4 2) ((_ extract 6 1) x))) ((_ extract 4 3) x))))
(check-sat)
