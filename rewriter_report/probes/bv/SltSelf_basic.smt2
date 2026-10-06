; SltSelf: (bvslt x x) -> false
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvslt x x) false)))
(check-sat)
