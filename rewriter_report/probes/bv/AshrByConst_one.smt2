; AshrByConst: amount 1 -> concat(repeat 1 sign, extract 3 1 x)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvashr x #x1) (concat ((_ extract 3 3) x) ((_ extract 3 1) x)))))
(check-sat)
