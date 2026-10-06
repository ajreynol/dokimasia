; ZeroUle: (bvule 0 x) -> true
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(assert (not (= (bvule #x0 x) true)))
(check-sat)
