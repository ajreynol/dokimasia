; UltOnes: width 1 (bvult #b1 b) -> false
; EXPECT: unsat
(set-logic QF_BV)
(declare-const b (_ BitVec 1))
(assert (not (= (bvult #b1 b) false)))
(check-sat)
