; Proof probe: (bvult (int2bv 3 i) c) / (bvule ...) -> arith (< (mod i 8) c) (IneqElimConversion; no dedicated RARE rule).
; EXPECT: unsat
(set-logic ALL)
(declare-const i Int)
(assert (bvult ((_ int2bv 3) i) #b011))
(assert (>= (mod i 8) 3))
(check-sat)
