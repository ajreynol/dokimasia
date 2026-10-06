; UltOnes: (bvult ones x) -> false (no RARE rule for this direction)
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvult #xF x) false)))
(check-sat)
