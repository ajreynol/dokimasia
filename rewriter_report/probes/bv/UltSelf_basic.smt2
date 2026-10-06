; UltSelf: (bvult x x) -> false
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvult x x) false)))
(check-sat)
