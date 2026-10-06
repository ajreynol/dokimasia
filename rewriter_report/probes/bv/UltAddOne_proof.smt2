; Proof probe: x <u y+1 (ppRewrite UltAddOne) -> y != ~0 and not (y <u x); both const positions.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 4))
(declare-const y (_ BitVec 4))
(assert (bvult x (bvadd y #x1)))
(assert (or (= y #xf) (bvult y x)))
(check-sat)
