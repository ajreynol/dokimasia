; AshrByConst: amount = width -> repeat 4 sign
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvashr x #x4) ((_ repeat 4) ((_ extract 3 3) x)))))
(check-sat)
