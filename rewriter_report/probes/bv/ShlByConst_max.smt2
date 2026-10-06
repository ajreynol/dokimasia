; ShlByConst: amount = 2^w-1 (max) -> 0
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvshl x #xF) #x0)))
(check-sat)
