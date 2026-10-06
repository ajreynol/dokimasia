; proof+differential: (bvsdivo x y) vs an independent BV spec at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvsdivo x y) (and (= x #b1000) (= y #b1111)))))
(check-sat)
