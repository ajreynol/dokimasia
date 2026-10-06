; AshrByConst: amount w-1 -> repeat 3 sign ++ sign
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvashr x #x3) ((_ repeat 4) ((_ extract 3 3) x)))))
(check-sat)
