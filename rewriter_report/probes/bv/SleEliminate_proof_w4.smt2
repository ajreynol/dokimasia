; proof: (bvsle x y) = (not (bvslt y x)) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsle x y) (not (bvslt y x)))))
(check-sat)
