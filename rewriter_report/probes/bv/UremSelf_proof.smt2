; Proof probe: (bvurem t t) -> 0 (UremSelf / bv-urem-self), with a compound t.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (not (= (bvurem (bvand x y) (bvand x y)) #b0000)))
(check-sat)
