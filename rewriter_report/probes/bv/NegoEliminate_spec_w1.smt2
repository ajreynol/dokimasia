; proof+differential: (bvnego x) iff x = INT_MIN at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(assert (not (= (bvnego x) (= x #b1))))
(check-sat)
