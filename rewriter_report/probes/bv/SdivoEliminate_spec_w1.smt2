; proof+differential: (bvsdivo x y) vs an independent BV spec at width 1
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 1))
(declare-const y (_ BitVec 1))
(assert (not (= (bvsdivo x y) (and (= x #b1) (= y #b1)))))
(check-sat)
