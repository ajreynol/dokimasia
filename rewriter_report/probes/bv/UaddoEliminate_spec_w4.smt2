; proof+differential: (bvuaddo x y) vs an independent BV spec at width 4
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvuaddo x y) (bvult (bvadd x y) x))))
(check-sat)
