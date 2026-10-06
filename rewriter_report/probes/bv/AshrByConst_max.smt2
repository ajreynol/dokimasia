; AshrByConst: amount = 2^w-1 (max) -> repeat 4 sign
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvashr x #xF) ((_ repeat 4) ((_ extract 3 3) x)))))
(check-sat)
