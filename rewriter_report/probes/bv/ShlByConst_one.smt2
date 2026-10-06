; ShlByConst: amount 1 -> concat(extract 2 0 x, 0)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvshl x #x1) (concat ((_ extract 2 0) x) #b0))))
(check-sat)
