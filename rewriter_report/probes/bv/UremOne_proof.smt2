; Proof probe: (bvurem x 1) -> 0 (UremOne / bv-urem-one; shadowed by UremPow2 power 0 in RewriteUrem).
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 5))
(assert (not (= (bvurem x #b00001) #b00000)))
(check-sat)
