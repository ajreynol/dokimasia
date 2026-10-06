; proof: (bvsge x y) = (bvsle y x) at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsge x y) (bvsle y x))))
(check-sat)
