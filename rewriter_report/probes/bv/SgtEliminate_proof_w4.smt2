; proof: (bvsgt x y) = (bvslt y x) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsgt x y) (bvslt y x))))
(check-sat)
