; proof+differential: (bvnego x) iff x = INT_MIN at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvnego x) (= x #b1000))))
(check-sat)
