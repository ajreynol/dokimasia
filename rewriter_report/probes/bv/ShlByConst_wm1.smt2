; ShlByConst: amount w-1 -> concat(extract 0 0 x, 000)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvshl x #x3) (concat ((_ extract 0 0) x) #b000))))
(check-sat)
