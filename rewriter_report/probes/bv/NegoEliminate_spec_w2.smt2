; proof+differential: (bvnego x) iff x = INT_MIN at width 2
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 2))
(assert (not (= (bvnego x) (= x #b10))))
(check-sat)
